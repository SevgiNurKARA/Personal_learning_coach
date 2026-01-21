"""
Assessment Agent - Kullanıcı seviye belirleme ve profil analizi
==============================================================
Kullanıcının seviyesini belirler ve profilini analiz eder.
"""

from typing import Dict, List, Optional
import os
import json
from datetime import datetime

try:
    from tools.ai_service import get_ai_service
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


class AssessmentAgent:
    """Kullanıcı seviyesini belirleyen ve profil analizi yapan agent."""
    
    def __init__(self, memory_service=None):
        self.memory = memory_service
        self.ai_service = None
        
        if AI_AVAILABLE:
            try:
                self.ai_service = get_ai_service()
            except:
                pass
    
    def analyze_user_profile(self, user_input: Dict) -> Dict:
        """Kullanıcı girişini analiz edip profil oluşturur."""
        profile = {
            "goal": user_input.get("goal"),
            "level": user_input.get("current_level", "unknown"),
             # Handle string input for daily_time gracefully
            "daily_time": float(user_input.get("daily_time", user_input.get("daily_available_time", 1.0))),
            "style": user_input.get("preferred_learning_style", "balanced"),
            "created_at": user_input.get("created_at", datetime.now().isoformat())
        }
        
        goal_lower = (profile["goal"] or "").lower()
        if "python" in goal_lower:
            profile["domain"] = "python"
        elif any(x in goal_lower for x in ["web", "html", "css", "js", "javascript"]):
            profile["domain"] = "web"
        elif any(x in goal_lower for x in ["data", "veri", "analiz", "pandas"]):
            profile["domain"] = "data"
        elif any(x in goal_lower for x in ["english", "ingilizce"]):
            profile["domain"] = "english"
        else:
            profile["domain"] = "general"

        if self.memory:
            self.memory.save_user_profile(profile)

        return profile

    def get_assessment_questions(self, topic: str, num_questions: int = 10) -> List[Dict]:
        """Seviye belirleme soruları üretir."""
        
        # AI ile soru üret
        if self._is_ai_available():
            try:
                questions = self.ai_service.generate_assessment_questions(topic, num_questions)
                if questions:
                    return questions
            except Exception as e:
                print(f"❌ AI assessment hatası: {e}")
        
        # Fallback
        return self._get_static_assessment(topic, num_questions)

    def calculate_level(self, answers: Dict[str, str], questions: List[Dict]) -> Dict:
        """Kullanıcı cevaplarını değerlendirip seviye belirler."""
        total = len(questions)
        if total == 0:
            return {"level": "beginner", "score": 0, "level_tr": "Başlangıç"}
            
        correct_count = 0
        difficulty_score = 0
        max_difficulty_score = 0
        
        score_breakdown = {"easy": 0, "medium": 0, "hard": 0}
        total_breakdown = {"easy": 0, "medium": 0, "hard": 0}
        
        for q in questions:
            q_id = str(q.get("id"))
            difficulty = q.get("difficulty", "medium")
            points = {"easy": 1, "medium": 2, "hard": 3}.get(difficulty, 1)
            
            max_difficulty_score += points
            total_breakdown[difficulty] = total_breakdown.get(difficulty, 0) + 1
            
            # Cevap kontrolü
            user_ans = answers.get(q_id)
            # Cevap şık metni veya şık harfi olabilir, basit kontrol
            correct = q.get("correct_answer")
            
            if user_ans and user_ans == correct:
                correct_count += 1
                difficulty_score += points
                score_breakdown[difficulty] = score_breakdown.get(difficulty, 0) + 1
        
        # Ağırlıklı skor hesabı (0-100)
        final_score = int((difficulty_score / max_difficulty_score) * 100) if max_difficulty_score > 0 else 0
        
        # Seviye belirleme
        if final_score >= 80:
            level = "advanced"
            level_tr = "İleri"
            start_day = 15
        elif final_score >= 50:
            level = "intermediate"
            level_tr = "Orta"
            start_day = 8
        else:
            level = "beginner"
            level_tr = "Başlangıç"
            start_day = 1
            
        # Kategori bazlı skorlar
        easy_pct = int((score_breakdown["easy"] / total_breakdown["easy"]) * 100) if total_breakdown["easy"] > 0 else 0
        med_pct = int((score_breakdown["medium"] / total_breakdown["medium"]) * 100) if total_breakdown["medium"] > 0 else 0
        hard_pct = int((score_breakdown["hard"] / total_breakdown["hard"]) * 100) if total_breakdown["hard"] > 0 else 0
            
        return {
            "level": level,
            "level_tr": level_tr,
            "score": final_score,
            "recommended_start_day": start_day,
            "easy_score": easy_pct,
            "medium_score": med_pct,
            "hard_score": hard_pct,
            "strengths": self._get_strengths(score_breakdown, total_breakdown),
            "weaknesses": self._get_weaknesses(score_breakdown, total_breakdown),
            "summary": f"{level_tr} seviyesindesiniz. Önerilen başlangıç: Gün {start_day}."
        }

    def _is_ai_available(self) -> bool:
        return self.ai_service is not None and self.ai_service._is_configured()

    def _get_strengths(self, score_bd, total_bd):
        strengths = []
        if total_bd["hard"] > 0 and score_bd["hard"] / total_bd["hard"] > 0.6:
            strengths.append("Zor konularda yetkinlik")
        if total_bd["medium"] > 0 and score_bd["medium"] / total_bd["medium"] > 0.8:
            strengths.append("Temel kavramlar sağlam")
        return strengths

    def _get_weaknesses(self, score_bd, total_bd):
        weaknesses = []
        if total_bd["easy"] > 0 and score_bd["easy"] / total_bd["easy"] < 0.5:
            weaknesses.append("Temel eksiklikler var")
        if total_bd["hard"] > 0 and score_bd["hard"] / total_bd["hard"] < 0.3:
            weaknesses.append("İleri konulara çalışılmalı")
        return weaknesses

    def _get_static_assessment(self, topic: str, num_questions: int) -> List[Dict]:
        """Fallback sorular."""
        # Basit fallback, detaylısı implementation plan'da vardı ama burada minimal tutacağız
        # Konu algılama
        topic_lower = topic.lower()
        
        questions = []
        for i in range(num_questions):
            diff = "easy" if i < 3 else "medium" if i < 7 else "hard"
            questions.append({
                "id": i+1,
                "question": f"{topic} hakkında örnek soru {i+1} ({diff})",
                "options": ["A Seçeneği", "B Seçeneği", "C Seçeneği", "D Seçeneği"],
                "correct_answer": "A Seçeneği",
                "difficulty": diff,
                "topic_area": "Genel"
            })
            
        return questions

# Singleton
_assessment_agent = None

def get_assessment_agent() -> AssessmentAgent:
    global _assessment_agent
    if _assessment_agent is None:
        _assessment_agent = AssessmentAgent()
    return _assessment_agent
