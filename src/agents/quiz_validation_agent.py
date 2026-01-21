"""
Quiz & Validation Agent - Quiz üretimi ve değerlendirmesi
========================================================
Quiz oluşturur, puanlar ve başarı analizi yapar.
"""

from typing import Dict, List, Optional
import os
import json
from dataclasses import asdict

try:
    from tools.ai_service import get_ai_service
    from tools.quiz_scoring import QuizScorer, QuizResult
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


class QuizValidationAgent:
    """Quiz üretimi ve doğrulama işlemlerini yürüten agent."""
    
    def __init__(self):
        self.ai_service = None
        self.quiz_scorer = QuizScorer()
        
        if AI_AVAILABLE:
            try:
                self.ai_service = get_ai_service()
            except:
                pass
    
    def _is_ai_available(self) -> bool:
        """AI servisinin kullanılabilir olup olmadığını kontrol eder."""
        return self.ai_service is not None and self.ai_service._is_configured()
    
    def generate_quiz(self, topic: str, level: str = "beginner", num_questions: int = 5, goal: str = "") -> List[Dict]:
        """
        Quiz soruları üretir.
        
        Args:
            topic: Konu başlığı
            level: Seviye
            num_questions: Soru sayısı
            goal: Kullanıcı hedefi
        
        Returns:
            Quiz soruları listesi
        """
        # AI ile quiz üret
        if self._is_ai_available():
            try:
                questions = self.ai_service.generate_quiz_questions(topic, level, num_questions, goal)
                if questions and len(questions) > 0:
                    return questions
                else:
                    print(f"⚠️ AI boş sonuç döndürdü: {topic}")
            except Exception as e:
                print(f"❌ AI quiz hatası: {e}")
        else:
            print(f"⚠️ AI servisi kullanılamıyor, fallback quiz oluşturuluyor")
        
        # AI çalışmazsa minimal fallback
        return self._get_minimal_fallback_quiz(topic, num_questions)
    
    def validate_quiz(self, answers: Dict[str, str], questions: List[Dict]) -> Dict:
        """
        Quiz sonuçlarını değerlendirir ve analiz raporu döndürür.
        """
        # QuizScorer için format dönüşümü gerekebilir
        # questions listesi dict listesi, QuizScorer QuizQuestion objesi bekliyor olabilir
        # Ancak QuizScorer.score_quiz basit dict alıyor, analyze_quiz obje alıyor. -> analyze_quiz kullanalım.
        
        from tools.quiz_scoring import QuizQuestion
        
        quiz_questions = []
        for q in questions:
            quiz_questions.append(QuizQuestion(
                question_id=q.get("question_id", str(q.get("id"))),
                question=q.get("question", ""),
                options=q.get("options", []),
                correct_answer=q.get("correct_answer", q.get("correct", "")),
                topic=q.get("topic", ""),
                difficulty=1 # Varsayılan zorluk
            ))
            
        result = self.quiz_scorer.analyze_quiz(answers, quiz_questions)
        suggestions = self.quiz_scorer.get_improvement_suggestions(result)
        
        return {
            "score": result.score_percentage,
            "correct_count": result.correct_count,
            "total_questions": result.total_questions,
            "passed": result.score_percentage >= 70,
            "weak_topics": result.weak_topics,
            "strong_topics": result.strong_topics,
            "suggestions": suggestions,
            "analysis": asdict(result)
        }

    def _get_minimal_fallback_quiz(self, topic: str, num_questions: int) -> List[Dict]:
        """
        Minimal fallback - sadece AI çalışmazsa.
        """
        return [
            {
                "question_id": f"fallback_{i+1}",
                "question": f"⚠️ AI servisi çalışmıyor ({topic}). Lütfen GEMINI_API_KEY'i yapılandırın.",
                "options": [
                    "API key ekleyin",
                    ".env dosyasını kontrol edin",
                    "Gemini API'yi aktifleştirin",
                    "Yöneticiye başvurun"
                ],
                "correct_answer": "API key ekleyin",
                "topic": topic,
                "is_fallback": True
            }
            for i in range(min(num_questions, 3))
        ]

# Singleton
_quiz_agent = None

def get_quiz_validation_agent() -> QuizValidationAgent:
    global _quiz_agent
    if _quiz_agent is None:
        _quiz_agent = QuizValidationAgent()
    return _quiz_agent
