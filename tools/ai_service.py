from typing import Dict, List, Optional
import os
import json

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class AIService:    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model_name = model_name
        self.model = None
        
        if self._is_configured() and GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name)
            except Exception as e:
                print(f"⚠️ Gemini API başlatılamadı: {e}")
                self.model = None
    
    def _is_configured(self) -> bool:
        return bool(self.api_key)
    
    def generate_personalized_plan(
        self, 
        profile: Dict, 
        resources: List[Dict],
        day: int = 1
    ) -> Dict:
        if not self.model:
            return self._mock_plan(profile, resources, day)
        
        prompt = f"""
        Bir öğrenci için kişiselleştirilmiş günlük çalışma planı oluştur.
        
        Öğrenci Profili:
        - Hedef: {profile.get('goal', 'Genel öğrenme')}
        - Seviye: {profile.get('level', 'başlangıç')}
        - Günlük müsait süre: {profile.get('daily_time', 1)} saat
        - Öğrenme stili: {profile.get('style', 'karma')}
        - Alan: {profile.get('domain', 'genel')}
        
        Gün: {day}
        
        Mevcut Kaynaklar:
        {json.dumps(resources[:3], ensure_ascii=False, indent=2)}
        
        Lütfen aşağıdaki JSON formatında bir plan oluştur:
        {{
            "type": "learning_plan",
            "day": {day},
            "theme": "Günün teması",
            "tasks": [
                {{"task": "Görev adı", "duration_min": 20, "type": "theory/practice/quiz", "description": "Açıklama"}}
            ],
            "resources": [...],
            "learning_objectives": ["Hedef 1", "Hedef 2"],
            "tips": "Günün ipucu"
        }}
        
        Sadece JSON döndür, başka açıklama ekleme.
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # JSON'u ayıkla
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            return json.loads(text)
        
        except Exception as e:
            print(f"⚠️ AI plan oluşturma hatası: {e}")
            return self._mock_plan(profile, resources, day)
    
    def generate_quiz_questions(
        self, 
        topic: str, 
        level: str = "beginner",
        num_questions: int = 5
    ) -> List[Dict]:
        if not self.model:
            return self._mock_quiz(topic, num_questions)
        
        prompt = f"""
        "{topic}" konusu için {level} seviyesinde {num_questions} adet çoktan seçmeli quiz sorusu oluştur.
        
        Her soru için:
        - 4 seçenek olmalı
        - Doğru cevap belirtilmeli
        - Türkçe olmalı
        
        JSON formatında döndür:
        [
            {{
                "question_id": "q1",
                "question": "Soru metni?",
                "options": ["A seçeneği", "B seçeneği", "C seçeneği", "D seçeneği"],
                "correct_answer": "Doğru seçenek",
                "topic": "{topic}",
                "difficulty": 1
            }}
        ]
        
        Sadece JSON döndür.
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            return json.loads(text)
        
        except Exception as e:
            print(f"⚠️ Quiz oluşturma hatası: {e}")
            return self._mock_quiz(topic, num_questions)
    
    def analyze_performance(self, performance_history: List[Dict]) -> Dict:
        if not self.model or not performance_history:
            return self._mock_analysis(performance_history)
        
        prompt = f"""
        Bir öğrencinin performans geçmişini analiz et ve öneriler sun.
        
        Performans Geçmişi:
        {json.dumps(performance_history[-7:], ensure_ascii=False, indent=2)}
        
        JSON formatında analiz döndür:
        {{
            "overall_trend": "improving/stable/declining",
            "strengths": ["Güçlü yön 1", "Güçlü yön 2"],
            "areas_to_improve": ["Geliştirilecek alan 1"],
            "recommendations": ["Öneri 1", "Öneri 2"],
            "motivation_message": "Motivasyon mesajı"
        }}
        
        Sadece JSON döndür.
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            return json.loads(text)
        
        except Exception as e:
            print(f"⚠️ Performans analizi hatası: {e}")
            return self._mock_analysis(performance_history)
    
    def explain_topic(self, topic: str, level: str = "beginner") -> str:
        if not self.model:
            return f"📚 {topic} konusu hakkında bilgi: Bu konu {level} seviyesinde öğrenilecektir."
        
        level_desc = {
            "beginner": "yeni başlayan birine basit ve anlaşılır şekilde",
            "intermediate": "temel bilgisi olan birine orta düzeyde detaylı",
            "advanced": "ileri seviye bilgisi olan birine teknik detaylarla"
        }
        
        prompt = f"""
        "{topic}" konusunu {level_desc.get(level, level)} açıkla.
        
        - Türkçe olmalı
        - Örnekler içermeli
        - Maksimum 300 kelime
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"📚 {topic} konusu hakkında bilgi alınamadı: {e}"
    
    def _mock_plan(self, profile: Dict, resources: List[Dict], day: int) -> Dict:
        daily_time = profile.get("daily_time", 1)
        
        return {
            "type": "learning_plan",
            "day": day,
            "theme": f"Gün {day} - Temel Kavramlar",
            "tasks": [
                {
                    "task": "Teori okuma",
                    "duration_min": int(daily_time * 20),
                    "type": "theory",
                    "description": "Günün konusunu oku ve not al"
                },
                {
                    "task": "Mini quiz",
                    "duration_min": int(daily_time * 10),
                    "type": "quiz",
                    "description": "Öğrenilenleri test et"
                },
                {
                    "task": "Pratik egzersiz",
                    "duration_min": int(daily_time * 20),
                    "type": "practice",
                    "description": "Küçük bir uygulama yap"
                }
            ],
            "resources": resources[:3],
            "learning_objectives": [
                "Temel kavramları anlama",
                "Pratik uygulama yapabilme"
            ],
            "tips": "Düzenli molalar verin ve not alın!",
            "source": "mock"
        }
    
    def _mock_quiz(self, topic: str, num_questions: int) -> List[Dict]:
        return [
            {
                "question_id": f"q{i+1}",
                "question": f"{topic} ile ilgili örnek soru {i+1}?",
                "options": ["Seçenek A", "Seçenek B", "Seçenek C", "Seçenek D"],
                "correct_answer": "Seçenek A",
                "topic": topic,
                "difficulty": 1,
                "source": "mock"
            }
            for i in range(num_questions)
        ]
    
    def _mock_analysis(self, performance_history: List[Dict]) -> Dict:
        return {
            "overall_trend": "stable",
            "strengths": ["Düzenli çalışma", "Görevleri tamamlama"],
            "areas_to_improve": ["Quiz performansı"],
            "recommendations": [
                "Günlük çalışma süresini koruyun",
                "Zorlandığınız konuları tekrar edin"
            ],
            "motivation_message": "İyi gidiyorsunuz! Devam edin! 🚀",
            "source": "mock"
        }


# Singleton instance
_ai_service: Optional[AIService] = None


def get_ai_service() -> AIService:
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service

