"""
Research Agent - Gerçek öğrenme kaynakları bulur
================================================
Konuya göre gerçek, kaliteli eğitim kaynaklarını döndürür.
"""

from typing import List, Dict


try:
    from tools.ai_service import get_ai_service
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


class ContentCuratorAgent:
    """Öğrenme kaynakları bulan ve içerik üreten agent."""
    
    def __init__(self, search_tool=None, memory_service=None):
        self.search_tool = search_tool
        self.memory = memory_service
        self.ai_service = None
        
        if AI_AVAILABLE:
            try:
                self.ai_service = get_ai_service()
            except:
                pass
        
        # Konu bazlı gerçek kaynaklar
        self.resources_db = {
            "python": [
                {
                    "title": "Python Resmi Dokümantasyonu",
                    "url": "https://docs.python.org/3/tutorial/",
                    "type": "documentation",
                    "description": "Python'un resmi öğrenme rehberi"
                },
# ... (rest of the file content is skipped for brevity) ...

                {
                    "title": "W3Schools Python Tutorial",
                    "url": "https://www.w3schools.com/python/",
                    "type": "tutorial",
                    "description": "İnteraktif Python dersleri"
                },
                {
                    "title": "Real Python",
                    "url": "https://realpython.com/",
                    "type": "tutorial",
                    "description": "Detaylı Python makaleleri ve projeler"
                },
                {
                    "title": "Python Egzersizleri - HackerRank",
                    "url": "https://www.hackerrank.com/domains/python",
                    "type": "practice",
                    "description": "Python pratik problemleri"
                },
                {
                    "title": "Codecademy Python",
                    "url": "https://www.codecademy.com/learn/learn-python-3",
                    "type": "course",
                    "description": "İnteraktif Python kursu"
                },
                {
                    "title": "Python Türkçe Kaynak - BTK Akademi",
                    "url": "https://www.btkakademi.gov.tr/portal/course/python-ile-programlama-10701",
                    "type": "course",
                    "description": "Ücretsiz Türkçe Python kursu"
                },
                {
                    "title": "YouTube - Python Dersleri (Türkçe)",
                    "url": "https://www.youtube.com/results?search_query=python+dersleri+türkçe",
                    "type": "video",
                    "description": "Türkçe Python video dersleri"
                }
            ],
            "web": [
                {
                    "title": "MDN Web Docs",
                    "url": "https://developer.mozilla.org/tr/",
                    "type": "documentation",
                    "description": "Web teknolojileri için en kapsamlı kaynak"
                },
                {
                    "title": "W3Schools",
                    "url": "https://www.w3schools.com/",
                    "type": "tutorial",
                    "description": "HTML, CSS, JavaScript dersleri"
                },
                {
                    "title": "freeCodeCamp",
                    "url": "https://www.freecodecamp.org/",
                    "type": "course",
                    "description": "Ücretsiz web geliştirme kursu"
                },
                {
                    "title": "CSS-Tricks",
                    "url": "https://css-tricks.com/",
                    "type": "tutorial",
                    "description": "CSS ipuçları ve örnekler"
                },
                {
                    "title": "JavaScript.info",
                    "url": "https://javascript.info/",
                    "type": "tutorial",
                    "description": "Modern JavaScript rehberi"
                },
                {
                    "title": "Frontend Mentor",
                    "url": "https://www.frontendmentor.io/",
                    "type": "practice",
                    "description": "Gerçek projelerle pratik"
                }
            ],
            "veri": [
                {
                    "title": "Kaggle Learn",
                    "url": "https://www.kaggle.com/learn",
                    "type": "course",
                    "description": "Ücretsiz veri bilimi kursları"
                },
                {
                    "title": "Pandas Dokümantasyonu",
                    "url": "https://pandas.pydata.org/docs/getting_started/",
                    "type": "documentation",
                    "description": "Pandas öğrenme rehberi"
                },
                {
                    "title": "DataCamp",
                    "url": "https://www.datacamp.com/",
                    "type": "course",
                    "description": "Veri bilimi kursları"
                },
                {
                    "title": "Towards Data Science",
                    "url": "https://towardsdatascience.com/",
                    "type": "article",
                    "description": "Veri bilimi makaleleri"
                },
                {
                    "title": "NumPy Başlangıç",
                    "url": "https://numpy.org/doc/stable/user/absolute_beginners.html",
                    "type": "documentation",
                    "description": "NumPy başlangıç rehberi"
                }
            ],
            "ingilizce": [
                {
                    "title": "Duolingo",
                    "url": "https://www.duolingo.com/",
                    "type": "app",
                    "description": "Ücretsiz dil öğrenme uygulaması"
                },
                {
                    "title": "BBC Learning English",
                    "url": "https://www.bbc.co.uk/learningenglish/",
                    "type": "course",
                    "description": "BBC İngilizce dersleri"
                },
                {
                    "title": "Cambridge Dictionary",
                    "url": "https://dictionary.cambridge.org/",
                    "type": "tool",
                    "description": "İngilizce sözlük ve telaffuz"
                },
                {
                    "title": "Englishpage",
                    "url": "https://www.englishpage.com/",
                    "type": "tutorial",
                    "description": "İngilizce gramer dersleri"
                },
                {
                    "title": "YouTube - English with Lucy",
                    "url": "https://www.youtube.com/c/EnglishwithLucy",
                    "type": "video",
                    "description": "İngilizce video dersleri"
                }
            ],
            "genel": [
                {
                    "title": "Khan Academy",
                    "url": "https://tr.khanacademy.org/",
                    "type": "course",
                    "description": "Ücretsiz online eğitim platformu"
                },
                {
                    "title": "Coursera",
                    "url": "https://www.coursera.org/",
                    "type": "course",
                    "description": "Üniversite kursları"
                },
                {
                    "title": "edX",
                    "url": "https://www.edx.org/",
                    "type": "course",
                    "description": "Ücretsiz online kurslar"
                },
                {
                    "title": "Udemy",
                    "url": "https://www.udemy.com/",
                    "type": "course",
                    "description": "Çeşitli konularda kurslar"
                }
            ]
        }

    def build_query(self, profile: Dict) -> str:
        """Arama sorgusu oluşturur."""
        domain = profile.get("domain", "programming")
        level = profile.get("level", "beginner")
        goal = profile.get("goal", "")
        return f"{level} {domain} {goal} tutorial"

    def find_resources(self, profile: Dict) -> List[Dict]:
        """Konuya göre gerçek kaynakları döndürür."""
        goal = profile.get("goal", "").lower()
        domain = profile.get("domain", "general").lower()
        
        # Konuyu belirle
        if "python" in goal or "python" in domain:
            resources = self.resources_db["python"]
        elif any(x in goal or x in domain for x in ["web", "html", "css", "javascript", "site"]):
            resources = self.resources_db["web"]
        elif any(x in goal or x in domain for x in ["veri", "data", "analiz", "pandas"]):
            resources = self.resources_db["veri"]
        elif any(x in goal or x in domain for x in ["ingilizce", "english", "dil"]):
            resources = self.resources_db["ingilizce"]
        else:
            resources = self.resources_db["genel"]
        
        # Belleğe kaydet
        if self.memory:
            self.memory.save_recommendations(profile.get("goal"), resources)
        
        return resources[:5]  # İlk 5 kaynak
    
    def get_resources_for_topic(self, topic: str) -> List[Dict]:
        """Belirli bir konu için kaynakları döndürür."""
        topic_lower = topic.lower()
        
        if "python" in topic_lower:
            return self.resources_db["python"][:5]
        elif any(x in topic_lower for x in ["web", "html", "css"]):
            return self.resources_db["web"][:5]
        elif any(x in topic_lower for x in ["veri", "data"]):
            return self.resources_db["veri"][:5]
        elif any(x in topic_lower for x in ["ingilizce", "english"]):
            return self.resources_db["ingilizce"][:5]
        else:
            return self.resources_db["genel"][:5]

    def _is_ai_available(self) -> bool:
        """AI servisinin kullanılabilir olup olmadığını kontrol eder."""
        return self.ai_service is not None and self.ai_service._is_configured()

    def generate_lesson_content(self, topic: str, level: str = "beginner", goal: str = "") -> str:
        """
        Ders içeriği üretir - AI veya Fallback.
        """
        # AI ile içerik üret
        if self._is_ai_available():
            try:
                content = self.ai_service.explain_topic(topic, level, goal)
                if content and len(content) > 50:
                    return content
                else:
                    print(f"⚠️ AI boş içerik döndürdü: {topic}")
            except Exception as e:
                print(f"❌ AI içerik hatası: {e}")
        else:
            print(f"⚠️ AI servisi kullanılamıyor")
        
        # AI çalışmazsa minimal fallback
        return self._get_minimal_fallback_content(topic, level, goal)

    def _get_minimal_fallback_content(self, topic: str, level: str, goal: str) -> str:
        """
        Minimal fallback içerik - sadece AI çalışmazsa.
        """
        return f"""
# ⚠️ AI Servisi Çalışmıyor

## {topic}

Bu ders içeriği AI tarafından oluşturulmalıdır, ancak şu anda AI servisi kullanılamıyor.

### Lütfen şunları kontrol edin:

1. **GEMINI_API_KEY** `.env` dosyasında tanımlı mı?
2. API key geçerli mi?
3. İnternet bağlantınız var mı?

### Geçici Çözüm:

Bu konuyu öğrenmek için:
- Google'da "{topic}" aratın
- YouTube'da "{topic} tutorial" izleyin
- Resmi dokümantasyonları inceleyin

**Hedef:** {goal if goal else 'Belirtilmemiş'}  
**Seviye:** {level}

---

💡 **Not:** AI servisi aktif olduğunda bu sayfa otomatik olarak {topic} hakkında detaylı, kişiselleştirilmiş içerik gösterecektir.
"""


# Singleton
_content_curator_agent = None

def get_content_curator_agent() -> ContentCuratorAgent:
    global _content_curator_agent
    if _content_curator_agent is None:
        _content_curator_agent = ContentCuratorAgent()
    return _content_curator_agent
