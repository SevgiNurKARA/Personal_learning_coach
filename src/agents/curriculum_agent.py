"""
Curriculum Agent - AI ile dinamik müfredat oluşturur
====================================================
Kullanıcının hedefine göre konu haritası ve öğrenme yolu çıkarır.
HER ŞEY AI TARAFINDAN OLUŞTURULUR - statik şablon yok!
"""

from typing import Dict, List, Optional
import json
import os

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class CurriculumAgent:
    """AI ile dinamik müfredat oluşturan agent."""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.model = None
        
        if self.api_key and GEMINI_AVAILABLE:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("gemini-2.5-flash")
            except Exception as e:
                print(f"Gemini başlatılamadı: {e}")
    
    def _is_ai_available(self) -> bool:
        return self.model is not None
    
    def generate_curriculum(self, goal: str, level: str, duration_weeks: int = 4) -> Dict:
        """
        Hedefe göre tam müfredat oluşturur - TAMAMEN AI TABANLI.
        
        Returns:
            {
                "goal": "...",
                "total_days": 14,
                "daily_lessons": [
                    {"day": 1, "theme": "...", "tasks": [...], "quiz": [...]},
                    ...
                ]
            }
        """
        if self._is_ai_available():
            curriculum = self._generate_ai_curriculum(goal, level, duration_weeks)
            if curriculum and curriculum.get("daily_lessons"):
                return curriculum
            else:
                print("⚠️ AI boş müfredat döndürdü, fallback kullanılıyor")
        else:
            print("⚠️ AI servisi kullanılamıyor, fallback kullanılıyor")
        
        # AI çalışmazsa minimal fallback
        return self._generate_minimal_fallback_curriculum(goal, level, duration_weeks)
    
    def _generate_ai_curriculum(self, goal: str, level: str, duration_weeks: int) -> Dict:
        """AI ile müfredat oluşturur - HER ŞEY DINAMIK."""
        
        # Çok uzun müfredat JSON hatası verebilir, maksimum 14 gün (2 hafta) ile sınırla
        total_days = min(duration_weeks * 7, 14)
        actual_weeks = (total_days + 6) // 7  # Yukarı yuvarla
        
        prompt = f"""
Sen bir eğitim uzmanısın. Aşağıdaki hedefe ulaşmak için {total_days} günlük detaylı bir müfredat oluştur.

HEDEF: {goal}
SEVİYE: {level}
SÜRE: {total_days} gün

HER GÜN İÇİN:
- Spesifik bir konu/tema
- 3 görev (teori, pratik, quiz)
- 5 quiz sorusu (çoktan seçmeli)
- Gerçek kaynak linkleri
- Günlük ipucu

JSON FORMATI:

{{
    "goal": "{goal}",
    "summary": "Müfredat özeti",
    "total_days": {total_days},
    "daily_lessons": [
        {{
            "day": 1,
            "theme": "Günün konusu (spesifik)",
            "tasks": [
                {{
                    "task": "Teori: [Konu adı]",
                    "type": "theory",
                    "duration_min": 20,
                    "description": "Ne öğrenilecek, nasıl öğrenilecek"
                }},
                {{
                    "task": "Pratik: [Uygulama]",
                    "type": "practice",
                    "duration_min": 25,
                    "description": "Hangi pratik yapılacak"
                }},
                {{
                    "task": "Quiz: [Konu]",
                    "type": "quiz",
                    "duration_min": 10,
                    "description": "Öğrenilenleri test et"
                }}
            ],
            "quiz": [
                {{
                    "question_id": "q1",
                    "question": "Soru metni?",
                    "options": ["Seçenek A", "Seçenek B", "Seçenek C", "Seçenek D"],
                    "correct_answer": "Doğru seçenek",
                    "topic": "Alt konu"
                }},
                {{
                    "question_id": "q2",
                    "question": "Soru 2?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "Doğru",
                    "topic": "Alt konu"
                }},
                {{
                    "question_id": "q3",
                    "question": "Soru 3?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "Doğru",
                    "topic": "Alt konu"
                }},
                {{
                    "question_id": "q4",
                    "question": "Soru 4?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "Doğru",
                    "topic": "Alt konu"
                }},
                {{
                    "question_id": "q5",
                    "question": "Soru 5?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "Doğru",
                    "topic": "Alt konu"
                }}
            ],
            "resources": [
                {{
                    "title": "Kaynak adı",
                    "url": "https://gerçek-link.com",
                    "type": "article/video/documentation"
                }}
            ],
            "tip": "Günün motivasyon ipucu"
        }}
    ]
}}

ÖNEMLİ KURALLAR:
1. MUTLAKA {total_days} gün için içerik oluştur
2. Her gün için 5 quiz sorusu (question_id: q1-q5)
3. Quiz soruları konuyla alakalı ve değişken olsun
4. Kaynak linkleri gerçek ve çalışan olsun
5. Konular sıralı ve mantıklı ilerlesin
6. Görevler spesifik olsun (örn: "teori okuma" değil, "Python değişken tanımlama kurallarını öğren")
7. Türkçe içerik
8. JSON string'lerinde tırnak işareti kullanma, tek tırnak kullan veya kaç
9. Açıklamalarda satır sonu karakteri kullanma, boşluk kullan

SADECE GEÇERLİ JSON DÖNDÜR, BAŞKA BİR ŞEY YAZMA. JSON SYNTAX HATASIZ OLMALI!
"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # JSON'u ayıkla
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            # JSON'u temizle
            text = text.strip()
            
            # Eğer metin çok uzunsa ve hatalıysa, AI'ya daha kısa müfredat ürettir
            if len(text) > 100000:
                print("⚠️ AI çok uzun yanıt döndürdü, fallback kullanılıyor...")
                return self._generate_minimal_fallback_curriculum(goal, level, duration_weeks)
            
            # JSON'da olası sorunları düzelt
            # Tek tırnak yerine çift tırnak kullan (eğer JSON dışında tek tırnak varsa)
            # NOT: Bu basit bir düzeltme, karmaşık durumlarda çalışmayabilir
            
            # JSON parse et
            curriculum = json.loads(text)
            curriculum["source"] = "ai"
            
            # Validasyon - gerekli alanlar var mı?
            if not curriculum.get("daily_lessons") or len(curriculum.get("daily_lessons", [])) == 0:
                print("⚠️ AI boş müfredat döndürdü")
                return self._generate_minimal_fallback_curriculum(goal, level, duration_weeks)
            
            return curriculum
            
        except json.JSONDecodeError as e:
            print(f"❌ AI JSON parse hatası: {e}")
            print(f"AI'dan gelen metin (ilk 500 karakter): {text[:500] if 'text' in locals() else 'N/A'}")
            return self._generate_minimal_fallback_curriculum(goal, level, duration_weeks)
        except Exception as e:
            print(f"❌ AI müfredat hatası: {e}")
            return self._generate_minimal_fallback_curriculum(goal, level, duration_weeks)
    
    def _generate_minimal_fallback_curriculum(self, goal: str, level: str, duration_weeks: int) -> Dict:
        """
        Minimal fallback müfredat - sadece AI çalışmazsa.
        Kullanıcıya AI'yı yapılandırması gerektiğini gösterir.
        """
        total_days = duration_weeks * 7
        
        daily_lessons = []
        for i in range(total_days):
            day = i + 1
            daily_lessons.append({
                "day": day,
                "week": (day - 1) // 7 + 1,
                "theme": f"⚠️ AI Servisi Gerekli - Gün {day}",
                "tasks": [
                    {
                        "task": "AI Yapılandırması",
                        "type": "theory",
                        "duration_min": 20,
                        "description": "Lütfen GEMINI_API_KEY'i .env dosyasına ekleyin"
                    },
                    {
                        "task": "Dokümantasyon",
                        "type": "practice",
                        "duration_min": 25,
                        "description": "SETUP_GUIDE.md dosyasını okuyun"
                    },
                    {
                        "task": "Test",
                        "type": "quiz",
                        "duration_min": 10,
                        "description": "AI aktif olduğunda otomatik quiz oluşturulacak"
                    }
                ],
                "quiz": [],
                "resources": [
                    {
                        "title": "Gemini API Dokümantasyonu",
                        "url": "https://ai.google.dev/",
                        "type": "documentation"
                    }
                ],
                "tip": "AI servisi olmadan kişiselleştirilmiş müfredat oluşturulamaz. Lütfen API key'inizi yapılandırın."
            })
        
        return {
            "goal": goal,
            "summary": "⚠️ AI servisi gerekli - Lütfen GEMINI_API_KEY yapılandırın",
            "source": "fallback",
            "total_days": total_days,
            "daily_lessons": daily_lessons
        }
    
    def _generate_basic_curriculum_DEPRECATED(self, goal: str, level: str, duration_weeks: int) -> Dict:
        """Temel müfredat (AI yoksa) - ContentAgent ile dinamik."""
        
        try:
            from agents.content_agent import get_content_agent
            content_agent = get_content_agent()
        except:
            content_agent = None
        
        goal_lower = goal.lower()
        total_days = duration_weeks * 7
        
        # Konuya göre konu listesi oluştur
        if "python" in goal_lower:
            topics = self._get_python_topics(total_days)
        elif any(x in goal_lower for x in ["web", "html", "css", "site"]):
            topics = self._get_web_topics(total_days)
        elif any(x in goal_lower for x in ["veri", "data", "analiz"]):
            topics = self._get_data_topics(total_days)
        elif any(x in goal_lower for x in ["ingilizce", "english"]):
            topics = self._get_english_topics(total_days)
        else:
            # Genel konular için AI mühendisliği veya genel öğrenme konuları
            if any(x in goal_lower for x in ["ai", "yapay zeka", "mühendis", "makine öğren"]):
                topics = self._get_ai_topics(total_days)
            else:
                topics = self._get_general_topics(goal, total_days)
        
        # Her gün için ContentAgent ile quiz üret
        daily_lessons = []
        for i, topic in enumerate(topics):
            day = i + 1
            
            # Quiz soruları ContentAgent'tan al (AI tabanlı)
            # NOT: Müfredat oluşturulurken quiz'ler boş bırakılır
            # Quiz'ler kullanıcı o güne geldiğinde dinamik olarak üretilir
            quiz_questions = []
            
            # Quiz yoksa boş bırak (app.py ContentAgent'ı çağıracak)
            daily_lessons.append({
                "day": day,
                "week": (day - 1) // 7 + 1,
                "theme": topic,
                "tasks": [
                    {
                        "task": f"{topic} - Teori",
                        "type": "theory",
                        "duration_min": 20,
                        "description": f"{topic} konusunu öğrenin. Temel kavramları ve örnekleri inceleyin."
                    },
                    {
                        "task": f"{topic} - Pratik",
                        "type": "practice",
                        "duration_min": 25,
                        "description": f"{topic} ile ilgili uygulamalar yapın. Örnekleri kendiniz deneyin."
                    },
                    {
                        "task": f"{topic} - Quiz",
                        "type": "quiz",
                        "duration_min": 10,
                        "description": f"{topic} hakkında quiz çözerek öğrendiklerinizi test edin."
                    }
                ],
                "quiz": quiz_questions,  # ContentAgent'tan gelen sorular veya boş
                "resources": self._get_resources_for_topic(goal_lower),
                "tip": "Her gün düzenli çalışın ve pratik yapmayı ihmal etmeyin!"
            })
        
        return {
            "goal": goal,
            "summary": f"{duration_weeks} haftada {goal} öğrenin",
            "source": "content_agent",
            "total_days": total_days,
            "topics": topics,
            "daily_lessons": daily_lessons
        }
    
    def _get_python_topics(self, total_days: int) -> list:
        """Python konuları listesi."""
        all_topics = [
            "Python Kurulumu ve İlk Program",
            "Değişkenler ve Veri Tipleri",
            "String İşlemleri",
            "Sayılar ve Operatörler",
            "Kullanıcı Girdisi (input)",
            "Koşullu İfadeler (if-else)",
            "Karşılaştırma ve Mantıksal Operatörler",
            "for Döngüsü",
            "while Döngüsü",
            "break ve continue",
            "Listeler",
            "Liste Metodları",
            "Tuple ve Set",
            "Dictionary",
            "Dictionary Metodları",
            "Fonksiyon Tanımlama",
            "Fonksiyon Parametreleri",
            "Lambda Fonksiyonlar",
            "Dosya Okuma",
            "Dosya Yazma",
            "Hata Yönetimi (try-except)",
            "Modüller (import)",
            "Standart Kütüphane",
            "pip ve Paket Yönetimi",
            "List Comprehension",
            "OOP - Sınıflar",
            "OOP - Kalıtım",
            "Mini Proje 1",
            "Mini Proje 2",
            "Tekrar ve İleri Konular"
        ]
        return all_topics[:total_days]
    
    def _get_web_topics(self, total_days: int) -> list:
        """Web geliştirme konuları."""
        all_topics = [
            "HTML'e Giriş", "HTML Etiketleri", "HTML Formlar", "HTML Tablolar",
            "CSS'e Giriş", "CSS Seçiciler", "CSS Box Model", "CSS Flexbox",
            "CSS Grid", "Responsive Tasarım", "JavaScript Temelleri", "JS Değişkenler",
            "JS Fonksiyonlar", "JS DOM", "JS Olaylar", "Mini Proje",
            "Bootstrap", "jQuery", "AJAX", "API Kullanımı"
        ]
        return all_topics[:total_days]
    
    def _get_data_topics(self, total_days: int) -> list:
        """Veri bilimi konuları."""
        all_topics = [
            "Python Temelleri Tekrar", "NumPy Giriş", "NumPy Diziler", "NumPy İşlemler",
            "Pandas Giriş", "DataFrame", "Veri Okuma/Yazma", "Veri Temizleme",
            "Veri Filtreleme", "Gruplama", "Matplotlib Giriş", "Grafikler",
            "Seaborn", "İstatistik Temelleri", "Keşifsel Analiz", "Mini Proje"
        ]
        return all_topics[:total_days]
    
    def _get_english_topics(self, total_days: int) -> list:
        """İngilizce konuları."""
        all_topics = [
            "Alfabe ve Telaffuz", "Temel Kelimeler", "Selamlaşma", "Zamirler",
            "To Be Fiili", "Present Simple", "Sayılar", "Günler ve Aylar",
            "Soru Cümleleri", "Olumsuz Cümleler", "There is/are", "Some/Any",
            "Present Continuous", "Past Simple", "Gelecek Zaman", "Pratik Konuşma"
        ]
        return all_topics[:total_days]
    
    def _get_ai_topics(self, total_days: int) -> list:
        """AI Mühendisliği konuları."""
        all_topics = [
            "AI'ya Giriş ve Temel Kavramlar",
            "Python Programlama Temelleri",
            "NumPy ve Veri İşleme",
            "Pandas ile Veri Analizi",
            "Veri Görselleştirme",
            "İstatistik Temelleri",
            "Makine Öğrenmesine Giriş",
            "Supervised Learning",
            "Unsupervised Learning",
            "Regresyon Modelleri",
            "Sınıflandırma Algoritmaları",
            "Karar Ağaçları",
            "Random Forest",
            "Neural Networks Temelleri",
            "Deep Learning'e Giriş",
            "TensorFlow/Keras Giriş",
            "CNN - Görüntü İşleme",
            "RNN - Zaman Serileri",
            "NLP - Doğal Dil İşleme",
            "Model Değerlendirme",
            "Overfitting ve Underfitting",
            "Hyperparameter Tuning",
            "Transfer Learning",
            "Model Deployment",
            "MLOps Temelleri",
            "AI Etiği",
            "Proje 1: Veri Analizi",
            "Proje 2: Sınıflandırma",
            "Proje 3: Deep Learning",
            "Portfolio ve İş Arama"
        ]
        return all_topics[:total_days]
    
    def _get_general_topics(self, goal: str, total_days: int) -> list:
        """Genel konular için mantıklı başlıklar."""
        base_topics = [
            "Temellere Giriş",
            "Temel Kavramlar",
            "İlk Adımlar",
            "Pratik Uygulamalar",
            "Derinlemesine İnceleme",
            "İleri Konular",
            "Proje Çalışması",
            "Tekrar ve Pekiştirme"
        ]
        
        # Gün sayısına göre konuları çoğalt
        topics = []
        for i in range(total_days):
            week = i // 7 + 1
            day_in_week = i % 7 + 1
            topic_index = i % len(base_topics)
            topics.append(f"Hafta {week} - {base_topics[topic_index]}")
        
        return topics
    
    def _get_resources_for_topic(self, goal_lower: str) -> list:
        """Konuya göre kaynak linkleri."""
        if "python" in goal_lower:
            return [
                {"title": "Python Resmi Dokümantasyonu", "url": "https://docs.python.org/3/tutorial/", "type": "documentation"},
                {"title": "W3Schools Python", "url": "https://www.w3schools.com/python/", "type": "tutorial"}
            ]
        elif any(x in goal_lower for x in ["web", "html", "css"]):
            return [
                {"title": "MDN Web Docs", "url": "https://developer.mozilla.org/", "type": "documentation"},
                {"title": "W3Schools", "url": "https://www.w3schools.com/", "type": "tutorial"}
            ]
        elif any(x in goal_lower for x in ["veri", "data"]):
            return [
                {"title": "Kaggle Learn", "url": "https://www.kaggle.com/learn", "type": "course"},
                {"title": "Pandas Docs", "url": "https://pandas.pydata.org/docs/", "type": "documentation"}
            ]
        elif any(x in goal_lower for x in ["ingilizce", "english"]):
            return [
                {"title": "BBC Learning English", "url": "https://www.bbc.co.uk/learningenglish/", "type": "course"},
                {"title": "Duolingo", "url": "https://www.duolingo.com/", "type": "app"}
            ]
        elif any(x in goal_lower for x in ["ai", "yapay zeka", "mühendis", "makine öğren"]):
            return [
                {"title": "Kaggle Learn - Machine Learning", "url": "https://www.kaggle.com/learn/intro-to-machine-learning", "type": "course"},
                {"title": "TensorFlow Tutorials", "url": "https://www.tensorflow.org/tutorials", "type": "documentation"},
                {"title": "Fast.ai", "url": "https://www.fast.ai/", "type": "course"}
            ]
        else:
            return []


# Singleton
_curriculum_agent = None

def get_curriculum_agent() -> CurriculumAgent:
    global _curriculum_agent
    if _curriculum_agent is None:
        _curriculum_agent = CurriculumAgent()
    return _curriculum_agent
