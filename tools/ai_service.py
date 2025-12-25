from typing import Dict, List, Optional
import os
import json

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class AIService:    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash"):
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
        num_questions: int = 5,
        goal: str = ""
    ) -> List[Dict]:
        if not self.model:
            return self._mock_quiz(topic, num_questions)
        
        level_desc = {
            "beginner": "başlangıç seviyesi - temel kavramlar",
            "intermediate": "orta seviye - uygulama ve pratik bilgi",
            "advanced": "ileri seviye - derinlemesine ve teknik bilgi"
        }
        
        goal_context = f"\nKullanıcının genel hedefi: {goal}" if goal else ""
        
        prompt = f"""
Günlük ders konusu: "{topic}"
Seviye: {level_desc.get(level, level)}{goal_context}

Bu günün dersi için TAMAMEN "{topic}" konusuna odaklanmış {num_questions} adet çoktan seçmeli quiz sorusu oluştur.

ÖNEMLI KURALLAR:
1. Her soru SADECE "{topic}" konusuyla ilgili olmalı
2. Sorular kullanıcının bu günkü derste öğrendiği bilgileri test etmeli
3. Sorular {level} seviyesine uygun olmalı
4. Her sorunun 4 seçeneği olmalı
5. Seçenekler makul ve yanıltıcı olmalı
6. Doğru cevap mutlaka seçeneklerden biri olmalı (birebir eşleşmeli)
7. Sorular Türkçe olmalı

JSON formatında döndür:
[
    {{
        "question_id": "q1",
        "question": "Soru metni?",
        "options": ["A seçeneği", "B seçeneği", "C seçeneği", "D seçeneği"],
        "correct_answer": "Doğru seçenek (tam olarak options'dan biri)",
        "topic": "{topic}"
    }},
    {{
        "question_id": "q2",
        "question": "Soru metni?",
        "options": ["A seçeneği", "B seçeneği", "C seçeneği", "D seçeneği"],
        "correct_answer": "Doğru seçenek",
        "topic": "{topic}"
    }}
]

SADECE JSON döndür, başka açıklama ekleme.
"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # JSON'u ayıkla
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            text = text.strip()
            questions = json.loads(text)
            
            # Validasyon
            if not isinstance(questions, list) or len(questions) == 0:
                print(f"⚠️ AI geçersiz format döndürdü, mock quiz kullanılıyor")
                return self._mock_quiz(topic, num_questions)
            
            # Her sorunun gerekli alanları olduğunu kontrol et
            valid_questions = []
            for q in questions:
                if all(key in q for key in ["question_id", "question", "options", "correct_answer"]):
                    # options listesinde correct_answer var mı kontrol et
                    if q["correct_answer"] in q["options"]:
                        # topic alanı yoksa ekle
                        if "topic" not in q:
                            q["topic"] = topic
                        valid_questions.append(q)
                    else:
                        print(f"⚠️ Soru atlandı: Doğru cevap seçeneklerde yok - {q.get('question', '')[:50]}")
            
            if len(valid_questions) >= num_questions // 2:
                return valid_questions[:num_questions]
            else:
                print(f"⚠️ Yeterli geçerli soru üretilemedi ({len(valid_questions)}/{num_questions}), mock quiz kullanılıyor")
                return self._mock_quiz(topic, num_questions)
        
        except json.JSONDecodeError as e:
            print(f"⚠️ Quiz JSON parse hatası: {e}")
            return self._mock_quiz(topic, num_questions)
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
    
    def explain_topic(self, topic: str, level: str = "beginner", goal: str = "") -> str:
        if not self.model:
            return f"📚 {topic} konusu hakkında bilgi: Bu konu {level} seviyesinde öğrenilecektir."
        
        level_desc = {
            "beginner": "yeni başlayan birine basit ve anlaşılır şekilde",
            "intermediate": "temel bilgisi olan birine orta düzeyde detaylı",
            "advanced": "ileri seviye bilgisi olan birine teknik detaylarla"
        }
        
        goal_context = f"\n\nKullanıcının genel hedefi: {goal}" if goal else ""
        
        prompt = f"""
"{topic}" konusunu {level_desc.get(level, level)} açıkla.{goal_context}

GEREKSINIMLER:
- Türkçe olmalı
- Pratik örnekler içermeli
- Kod örnekleri varsa açıklamalı
- Anlaşılır ve eğitici olmalı
- Markdown formatında
- Minimum 200, maksimum 500 kelime

YAPILANDIRMA:
1. Konuya giriş
2. Temel kavramlar
3. Pratik örnekler (kod varsa)
4. Önemli noktalar
5. Özet

Sadece içeriği döndür, başka açıklama ekleme.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"📚 {topic} konusu hakkında bilgi alınamadı: {e}"
    
    def explain_wrong_answer(
        self, 
        question: str, 
        user_answer: str, 
        correct_answer: str, 
        topic: str = "",
        level: str = "beginner"
    ) -> str:
        """Yanlış cevap için açıklama üretir."""
        if not self.model:
            return f"Doğru cevap: {correct_answer}. Konuyu tekrar gözden geçirin."
        
        prompt = f"""
Bir öğrenci quiz sorusuna yanlış cevap verdi. Ona yardımcı ol.

SORU: {question}
ÖĞRENCİNİN CEVABI: {user_answer}
DOĞRU CEVAP: {correct_answer}
KONU: {topic}
SEVİYE: {level}

Lütfen:
1. Doğru cevabın neden doğru olduğunu açıkla
2. Öğrencinin neden yanlış yaptığını anlat
3. Bu konuyu nasıl öğrenebileceğine dair kısa bir ipucu ver
4. Cesaretlendirici ol

KISA VE NET AÇIKLA (maksimum 3-4 cümle).
Türkçe yaz.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Doğru cevap: {correct_answer}. Bu konuyu tekrar gözden geçirmenizi öneririz."
    
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

