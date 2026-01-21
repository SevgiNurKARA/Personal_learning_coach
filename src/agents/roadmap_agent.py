"""
Roadmap Agent - Müfredat ve Planlama
====================================
Kullanıcının hedefine göre dinamik veya statik müfredat oluşturur.
Hem genel yol haritasını hem de detaylı ders planlarını yönetir.
"""

from typing import Dict, List, Optional
import os
import json

try:
    from tools.ai_service import get_ai_service
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


class RoadmapAgent:
    """Müfredat ve öğrenme yolu oluşturan agent."""
    
    def __init__(self):
        self.ai_service = None
        if AI_AVAILABLE:
            try:
                self.ai_service = get_ai_service()
            except:
                pass
        
        # Statik müfredat verileri (Fallback)
        self.static_curriculums = {
            "python": self._get_python_curriculum(),
            "web": self._get_web_curriculum(),
            "data": self._get_data_curriculum(),
            "english": self._get_english_curriculum(),
            "general": self._get_general_curriculum()
        }
    
    def _is_ai_available(self) -> bool:
        return self.ai_service is not None and self.ai_service._is_configured()
    
    def generate_curriculum(self, goal: str, level: str, duration_weeks: int = 4) -> Dict:
        """Müfredat oluşturur."""
        
        # 1. AI ile dene
        if self._is_ai_available():
            try:
                print(f"🤖 AI ile müfredat oluşturuluyor: {goal}")
                curriculum = self.ai_service.generate_curriculum(goal, level, duration_weeks)
                if curriculum and len(curriculum.get("daily_lessons", [])) > 0:
                    return curriculum
            except Exception as e:
                print(f"❌ AI müfredat hatası: {e}")
        
        # 2. Fallback kullan
        print("⚠️ Fallback müfredat kullanılıyor")
        return self._generate_fallback_curriculum(goal, level, duration_weeks)

    def _generate_fallback_curriculum(self, goal: str, level: str, duration_weeks: int) -> Dict:
        """Hedefe en uygun statik müfredatı döndürür."""
        goal_lower = goal.lower()
        
        if "python" in goal_lower:
            key = "python"
        elif any(x in goal_lower for x in ["web", "html", "css", "js"]):
            key = "web"
        elif any(x in goal_lower for x in ["data", "veri", "analiz"]):
            key = "data"
        elif any(x in goal_lower for x in ["english", "ingilizce"]):
            key = "english"
        else:
            key = "general"
            
        base_lessons = self.static_curriculums.get(key, self.static_curriculums["general"])
        
        # Süreye göre uyarla (döngüsel ekle)
        total_days = duration_weeks * 7
        final_lessons = []
        
        for i in range(total_days):
            # Modulo ile içerik tekrarı ama gün sayısı artar
            template = base_lessons[i % len(base_lessons)]
            lesson = template.copy()
            lesson["day"] = i + 1
            if i >= len(base_lessons):
                lesson["theme"] += " (Tekrar/Pratik)"
            final_lessons.append(lesson)
            
        return {
            "goal": goal,
            "level": level,
            "duration_weeks": duration_weeks,
            "daily_lessons": final_lessons,
            "summary": f"{goal} için {duration_weeks} haftalık hazırlanan program."
        }

    def get_day_plan(self, day: int, goal: str, level: str) -> Dict:
        """Belirli bir gün için plan döndürür (Fallback/Statik)."""
        # Şimdilik hızlı olması için fallback yapısını kullanıyoruz
        curriculum = self._generate_fallback_curriculum(goal, level, 4)
        lessons = curriculum.get("daily_lessons", [])
        
        if 0 < day <= len(lessons):
            return lessons[day-1]
        # Eğer gün kapsam dışıysa son günü döndür veya boş
        if lessons:
             return lessons[-1]
        return {}

    # --- Statik Müfredat Verileri (PlanningAgent'dan alındı) ---
    
    def _get_python_curriculum(self) -> List[Dict]:
        return [
            {
                "theme": "Python'a Giriş ve Kurulum",
                "tasks": [
                    {"task": "Python Kurulumu", "type": "theory", "duration_min": 15, "description": "python.org'dan Python indirip kurun."},
                    {"task": "İlk Program", "type": "practice", "duration_min": 20, "description": "print('Merhaba Dünya') yazın."},
                    {"task": "Quiz: Temeller", "type": "quiz", "duration_min": 10, "description": "Temel kavramları test edin."}
                ],
                "objectives": ["Kurulum", "İlk kod"],
                "tip": "Python'u PATH'e eklemeyi unutmayın."
            },
            {
                "theme": "Değişkenler ve Veri Tipleri",
                "tasks": [
                    {"task": "Değişkenler", "type": "theory", "duration_min": 20, "description": "int, float, str tiplerini öğrenin."},
                    {"task": "Pratik", "type": "practice", "duration_min": 25, "description": "Kendi bilgilerinizi değişkenlerde saklayın."},
                    {"task": "Quiz: Veri Tipleri", "type": "quiz", "duration_min": 10}
                ],
                "objectives": ["Değişken tanımlama"],
                "tip": "type() fonksiyonunu kullanın."
            },
            # ... (Daha fazla gün eklenebilir, şimdilik temel döngü yeterli)
             {
                "theme": "Koşullu İfadeler",
                "tasks": [
                    {"task": "if-else", "type": "theory", "duration_min": 20, "description": "Karar yapılarını öğrenin."},
                    {"task": "Not Hesaplama", "type": "practice", "duration_min": 30, "description": "Girilen nota göre harf notu verin."},
                    {"task": "Quiz: Koşullar", "type": "quiz", "duration_min": 10}
                ],
                "objectives": ["Akış kontrolü"],
                "tip": "Girintilere dikkat."
            },
            {
                "theme": "Döngüler",
                "tasks": [
                    {"task": "for ve while", "type": "theory", "duration_min": 20, "description": "Döngü mantığını kavrayın."},
                    {"task": "Çarpım Tablosu", "type": "practice", "duration_min": 30, "description": "İç içe döngülerle tablo yapın."},
                    {"task": "Quiz: Döngüler", "type": "quiz", "duration_min": 10}
                ],
                "objectives": ["Tekrarlı işlemler"],
                "tip": "Sonsuz döngüden kaçının."
            },
            {
                "theme": "Fonksiyonlar",
                "tasks": [
                    {"task": "Fonksiyon Tanımlama", "type": "theory", "duration_min": 20, "description": "def keyword'ü ve parametreler."},
                    {"task": "Hesap Makinesi", "type": "practice", "duration_min": 30, "description": "Fonksiyonlarla hesap makinesi yapın."},
                    {"task": "Quiz: Fonksiyonlar", "type": "quiz", "duration_min": 10}
                ],
                "objectives": ["Kod tekrarını önleme"],
                "tip": "Fonksiyonlar küçük ve odaklı olsun."
            }
        ]

    def _get_web_curriculum(self) -> List[Dict]:
        return [
            {
                "theme": "HTML Temelleri",
                "tasks": [
                    {"task": "HTML Yapısı", "type": "theory", "duration_min": 20, "description": "Tagler, head, body."},
                    {"task": "İlk Sayfa", "type": "practice", "duration_min": 30, "description": "Basit bir web sayfası yapın."},
                    {"task": "Quiz: HTML", "type": "quiz", "duration_min": 10}
                ],
                "objectives": ["HTML iskeleti"],
                "tip": "<!DOCTYPE html> ile başlayın."
            },
            {
                "theme": "CSS Temelleri",
                "tasks": [
                    {"task": "CSS Seçiciler", "type": "theory", "duration_min": 20, "description": "Class, id, element seçicileri."},
                    {"task": "Stil Verme", "type": "practice", "duration_min": 30, "description": "Sayfanızı renklendirin."},
                    {"task": "Quiz: CSS", "type": "quiz", "duration_min": 10}
                ],
                "objectives": ["Stil temelleri"],
                "tip": "External CSS kullanın."
            }
        ]
        
    def _get_data_curriculum(self) -> List[Dict]:
        return [
            {
                "theme": "Veri Bilimine Giriş",
                "tasks": [
                    {"task": "Kavramlar", "type": "theory", "duration_min": 20, "description": "Veri analitiği nedir?"},
                    {"task": "Pandas Kurulum", "type": "practice", "duration_min": 20, "description": "pip install pandas"},
                    {"task": "Quiz: Veri", "type": "quiz", "duration_min": 10}
                ],
                "objectives": ["Ortam hazırlığı"],
                "tip": "Jupyter Notebook kullanın."
            },
             {
                "theme": "Pandas DataFrame",
                "tasks": [
                    {"task": "DataFrame", "type": "theory", "duration_min": 20, "description": "Satır ve sütunlar."},
                    {"task": "Veri Okuma", "type": "practice", "duration_min": 30, "description": "CSV dosyası okuyun."},
                    {"task": "Quiz: Pandas", "type": "quiz", "duration_min": 10}
                ],
                "objectives": ["Veri manipülasyonu"],
                "tip": "head() ile veriye bakın."
            }
        ]
        
    def _get_english_curriculum(self) -> List[Dict]:
        return [
            {
                "theme": "Temel Tanışma",
                "tasks": [
                    {"task": "Selamlaşma", "type": "theory", "duration_min": 15, "description": "Hello, Hi, Good morning."},
                    {"task": "Kendini Tanıtma", "type": "practice", "duration_min": 20, "description": "I am... sentences."},
                    {"task": "Quiz: Tanışma", "type": "quiz", "duration_min": 10}
                ],
                "objectives": ["İletişim"],
                "tip": "Yüksek sesle tekrar edin."
            }
        ]
        
    def _get_general_curriculum(self) -> List[Dict]:
        return [
            {
                "theme": "Öğrenmeyi Öğrenmek",
                "tasks": [
                    {"task": "Hedef Belirleme", "type": "theory", "duration_min": 15, "description": "SMART hedefler."},
                    {"task": "Plan Yapma", "type": "practice", "duration_min": 20, "description": "Haftalık program çıkarın."},
                    {"task": "Quiz: Planlama", "type": "quiz", "duration_min": 10}
                ],
                "objectives": ["Planlı çalışma"],
                "tip": "Pomodoro tekniği kullanın."
            }
        ]

# Singleton
_roadmap_agent = None

def get_roadmap_agent() -> RoadmapAgent:
    global _roadmap_agent
    if _roadmap_agent is None:
        _roadmap_agent = RoadmapAgent()
    return _roadmap_agent
