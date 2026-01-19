"""
Level Assessment Agent - Kullanıcı seviye belirleme
====================================================
Kullanıcının mevcut bilgi seviyesini test sorularıyla belirler.
"""

from typing import Dict, List, Tuple
import os
import json

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class LevelAssessmentAgent:
    """Kullanıcı seviyesini belirleyen agent."""
    
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
    
    def get_assessment_questions(self, topic: str, num_questions: int = 10) -> List[Dict]:
        """
        Seviye belirleme soruları üretir.
        Kolay, orta ve zor sorular karışık olarak gelir.
        """
        if self._is_ai_available():
            return self._generate_ai_assessment(topic, num_questions)
        else:
            return self._get_static_assessment(topic, num_questions)
    
    def _generate_ai_assessment(self, topic: str, num_questions: int) -> List[Dict]:
        """AI ile seviye belirleme soruları üretir."""
        
        prompt = f"""
Kullanıcının hedefi: "{topic}"

Bu hedefe özel olarak kullanıcının mevcut seviyesini belirlemek için {num_questions} adet seviye belirleme sorusu oluştur.

ÖNEMLI: Sorular tamamen "{topic}" konusuna odaklanmalı ve kullanıcının bu konudaki bilgi seviyesini ölçmelidir.

Sorular şu dağılımda olsun:
- {int(num_questions * 0.4)} soru: Başlangıç seviyesi (temel kavramlar, tanımlar)
- {int(num_questions * 0.4)} soru: Orta seviye (uygulama, pratik bilgi)
- {int(num_questions * 0.2)} soru: İleri seviye (derinlemesine bilgi, ileri konular)

Her soru için:
- Soru metni açık ve net olmalı
- 4 seçenek olmalı
- Seçenekler makul ve yanıltıcı olmalı
- Doğru cevap seçeneklerden biri olmalı
- Zorluk seviyesi belirtilmeli
- Alt konu alanı belirtilmeli

JSON formatında döndür:

[
    {{
        "id": 1,
        "question": "Soru metni?",
        "options": ["A seçeneği", "B seçeneği", "C seçeneği", "D seçeneği"],
        "correct": "Doğru seçenek (tam olarak options'dan biri)",
        "difficulty": "easy",
        "topic_area": "Alt konu adı"
    }},
    {{
        "id": 2,
        "question": "Soru metni?",
        "options": ["A seçeneği", "B seçeneği", "C seçeneği", "D seçeneği"],
        "correct": "Doğru seçenek",
        "difficulty": "medium",
        "topic_area": "Alt konu adı"
    }}
]

Türkçe sorular üret. SADECE JSON döndür, başka açıklama ekleme.
"""
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            # JSON'u çıkar
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            text = text.strip()
            questions = json.loads(text)
            
            # Validasyon
            if not isinstance(questions, list) or len(questions) == 0:
                print("AI geçersiz format döndürdü, statik sorulara geçiliyor")
                return self._get_static_assessment(topic, num_questions)
            
            # Her sorunun gerekli alanları olduğunu kontrol et
            valid_questions = []
            for q in questions:
                if all(key in q for key in ["id", "question", "options", "correct", "difficulty", "topic_area"]):
                    # options listesinde correct var mı kontrol et
                    if q["correct"] in q["options"]:
                        valid_questions.append(q)
            
            if len(valid_questions) >= num_questions // 2:
                return valid_questions[:num_questions]
            else:
                print(f"Yeterli geçerli soru üretilemedi ({len(valid_questions)}/{num_questions}), statik sorulara geçiliyor")
                return self._get_static_assessment(topic, num_questions)
            
        except json.JSONDecodeError as e:
            print(f"AI JSON parse hatası: {e}")
            return self._get_static_assessment(topic, num_questions)
        except Exception as e:
            print(f"AI assessment hatası: {e}")
            return self._get_static_assessment(topic, num_questions)
    
    def _get_static_assessment(self, topic: str, num_questions: int) -> List[Dict]:
        """Statik seviye belirleme soruları."""
        
        topic_lower = topic.lower()
        
        if "python" in topic_lower:
            return self._get_python_assessment()
        elif any(x in topic_lower for x in ["web", "html", "css", "javascript"]):
            return self._get_web_assessment()
        elif any(x in topic_lower for x in ["veri", "data", "analiz"]):
            return self._get_data_assessment()
        elif any(x in topic_lower for x in ["ingilizce", "english"]):
            return self._get_english_assessment()
        else:
            return self._get_generic_assessment(topic)
    
    def calculate_level(self, answers: Dict[int, str], questions: List[Dict]) -> Dict:
        """
        Cevaplara göre seviye hesaplar.
        
        Returns:
            {
                "level": "beginner/intermediate/advanced",
                "level_tr": "Başlangıç/Orta/İleri",
                "score": 75,
                "easy_score": 100,
                "medium_score": 66,
                "hard_score": 33,
                "strengths": ["Temel kavramlar"],
                "weaknesses": ["İleri konular"],
                "recommended_start_day": 1,
                "summary": "Detaylı özet"
            }
        """
        easy_correct = 0
        easy_total = 0
        medium_correct = 0
        medium_total = 0
        hard_correct = 0
        hard_total = 0
        
        topic_scores = {}
        
        for q in questions:
            q_id = q.get("id", 0)
            difficulty = q.get("difficulty", "medium")
            topic_area = q.get("topic_area", "Genel")
            correct_answer = q.get("correct", "")
            user_answer = answers.get(q_id, "")
            
            is_correct = user_answer == correct_answer
            
            # Zorluk bazlı sayım
            if difficulty == "easy":
                easy_total += 1
                if is_correct:
                    easy_correct += 1
            elif difficulty == "medium":
                medium_total += 1
                if is_correct:
                    medium_correct += 1
            else:  # hard
                hard_total += 1
                if is_correct:
                    hard_correct += 1
            
            # Konu bazlı sayım
            if topic_area not in topic_scores:
                topic_scores[topic_area] = {"correct": 0, "total": 0}
            topic_scores[topic_area]["total"] += 1
            if is_correct:
                topic_scores[topic_area]["correct"] += 1
        
        # Yüzde hesapla
        easy_pct = (easy_correct / easy_total * 100) if easy_total > 0 else 0
        medium_pct = (medium_correct / medium_total * 100) if medium_total > 0 else 0
        hard_pct = (hard_correct / hard_total * 100) if hard_total > 0 else 0
        
        total_correct = easy_correct + medium_correct + hard_correct
        total_questions = easy_total + medium_total + hard_total
        overall_score = (total_correct / total_questions * 100) if total_questions > 0 else 0
        
        # Seviye belirleme
        if easy_pct < 50:
            level = "beginner"
            level_tr = "Başlangıç"
            start_day = 1
        elif easy_pct >= 80 and medium_pct >= 60 and hard_pct >= 40:
            level = "advanced"
            level_tr = "İleri"
            start_day = 15  # İleri konulardan başla
        elif easy_pct >= 70 and medium_pct >= 40:
            level = "intermediate"
            level_tr = "Orta"
            start_day = 8  # Orta seviyeden başla
        else:
            level = "beginner"
            level_tr = "Başlangıç"
            start_day = 1
        
        # Güçlü ve zayıf yönler
        strengths = []
        weaknesses = []
        
        for topic, scores in topic_scores.items():
            pct = (scores["correct"] / scores["total"] * 100) if scores["total"] > 0 else 0
            if pct >= 70:
                strengths.append(topic)
            elif pct < 50:
                weaknesses.append(topic)
        
        # Özet oluştur
        summary = f"Genel skorunuz %{int(overall_score)}. "
        if level == "beginner":
            summary += "Temel konulardan başlamanızı öneriyoruz. "
        elif level == "intermediate":
            summary += "Temel bilgileriniz iyi, orta seviye konulardan devam edebilirsiniz. "
        else:
            summary += "İleri seviye konulara geçebilirsiniz. "
        
        if weaknesses:
            summary += f"Şu konulara odaklanmanız faydalı olacaktır: {', '.join(weaknesses[:3])}"
        
        return {
            "level": level,
            "level_tr": level_tr,
            "score": int(overall_score),
            "easy_score": int(easy_pct),
            "medium_score": int(medium_pct),
            "hard_score": int(hard_pct),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommended_start_day": start_day,
            "summary": summary,
            "topic_scores": topic_scores
        }
    
    def _get_python_assessment(self) -> List[Dict]:
        """Python seviye belirleme soruları."""
        return [
            # Kolay sorular
            {
                "id": 1,
                "question": "Python'da ekrana 'Merhaba' yazdırmak için hangi kod kullanılır?",
                "options": ["echo 'Merhaba'", "print('Merhaba')", "console.log('Merhaba')", "System.out.print('Merhaba')"],
                "correct": "print('Merhaba')",
                "difficulty": "easy",
                "topic_area": "Temel Sözdizimi"
            },
            {
                "id": 2,
                "question": "'Merhaba' ifadesinin Python'daki veri tipi nedir?",
                "options": ["int", "float", "str", "bool"],
                "correct": "str",
                "difficulty": "easy",
                "topic_area": "Veri Tipleri"
            },
            {
                "id": 3,
                "question": "Python'da yorum satırı nasıl başlar?",
                "options": ["//", "#", "/*", "--"],
                "correct": "#",
                "difficulty": "easy",
                "topic_area": "Temel Sözdizimi"
            },
            {
                "id": 4,
                "question": "Python'da liste oluşturmak için hangi parantez kullanılır?",
                "options": ["()", "[]", "{}", "<>"],
                "correct": "[]",
                "difficulty": "easy",
                "topic_area": "Veri Yapıları"
            },
            # Orta seviye sorular
            {
                "id": 5,
                "question": "for i in range(3): print(i) çıktısı nedir?",
                "options": ["1 2 3", "0 1 2", "0 1 2 3", "1 2"],
                "correct": "0 1 2",
                "difficulty": "medium",
                "topic_area": "Döngüler"
            },
            {
                "id": 6,
                "question": "len([1, 2, [3, 4]]) sonucu nedir?",
                "options": ["2", "3", "4", "5"],
                "correct": "3",
                "difficulty": "medium",
                "topic_area": "Veri Yapıları"
            },
            {
                "id": 7,
                "question": "def fonk(x, y=5): return x+y şeklinde tanımlanan fonksiyonda fonk(3) sonucu nedir?",
                "options": ["3", "5", "8", "Hata verir"],
                "correct": "8",
                "difficulty": "medium",
                "topic_area": "Fonksiyonlar"
            },
            {
                "id": 8,
                "question": "try-except bloğu ne için kullanılır?",
                "options": ["Döngü oluşturmak", "Hata yakalamak", "Fonksiyon tanımlamak", "Değişken oluşturmak"],
                "correct": "Hata yakalamak",
                "difficulty": "medium",
                "topic_area": "Hata Yönetimi"
            },
            # Zor sorular
            {
                "id": 9,
                "question": "[x**2 for x in range(5) if x%2==0] sonucu nedir?",
                "options": ["[0, 4, 16]", "[1, 9]", "[0, 1, 4, 9, 16]", "[4, 16]"],
                "correct": "[0, 4, 16]",
                "difficulty": "hard",
                "topic_area": "List Comprehension"
            },
            {
                "id": 10,
                "question": "Python'da @decorator ne işe yarar?",
                "options": ["Yorum ekler", "Fonksiyonu değiştirir/genişletir", "Değişken tanımlar", "Döngü oluşturur"],
                "correct": "Fonksiyonu değiştirir/genişletir",
                "difficulty": "hard",
                "topic_area": "İleri Konular"
            },
            {
                "id": 11,
                "question": "class A: pass; class B(A): pass ifadesinde B sınıfı A'dan ne yapar?",
                "options": ["Import eder", "Kalıtım alır", "Silme işlemi yapar", "Kopyalar"],
                "correct": "Kalıtım alır",
                "difficulty": "hard",
                "topic_area": "OOP"
            }
        ]
    
    def _get_web_assessment(self) -> List[Dict]:
        """Web geliştirme seviye belirleme soruları."""
        return [
            # Kolay
            {"id": 1, "question": "HTML'de başlık etiketi hangisidir?", "options": ["<head>", "<h1>", "<title>", "<header>"], "correct": "<h1>", "difficulty": "easy", "topic_area": "HTML"},
            {"id": 2, "question": "CSS'de metin rengini değiştiren özellik hangisidir?", "options": ["text-color", "font-color", "color", "text-style"], "correct": "color", "difficulty": "easy", "topic_area": "CSS"},
            {"id": 3, "question": "HTML'de link oluşturmak için hangi etiket kullanılır?", "options": ["<link>", "<a>", "<href>", "<url>"], "correct": "<a>", "difficulty": "easy", "topic_area": "HTML"},
            {"id": 4, "question": "JavaScript'te değişken tanımlamak için hangisi kullanılır?", "options": ["var", "let", "const", "Hepsi"], "correct": "Hepsi", "difficulty": "easy", "topic_area": "JavaScript"},
            # Orta
            {"id": 5, "question": "CSS Flexbox'ta öğeleri yatay hizalamak için hangi özellik kullanılır?", "options": ["align-items", "justify-content", "flex-direction", "flex-wrap"], "correct": "justify-content", "difficulty": "medium", "topic_area": "CSS Flexbox"},
            {"id": 6, "question": "JavaScript'te DOM'dan bir elementi ID ile seçmek için ne kullanılır?", "options": ["getElement()", "getElementById()", "selectById()", "findById()"], "correct": "getElementById()", "difficulty": "medium", "topic_area": "JavaScript DOM"},
            {"id": 7, "question": "Responsive tasarım için hangi CSS özelliği kullanılır?", "options": ["@media", "@responsive", "@screen", "@device"], "correct": "@media", "difficulty": "medium", "topic_area": "Responsive"},
            # Zor
            {"id": 8, "question": "CSS Grid'de 'grid-template-columns: repeat(3, 1fr)' ne yapar?", "options": ["3 eşit sütun oluşturur", "3 satır oluşturur", "3px genişlik verir", "3 kez tekrarlar"], "correct": "3 eşit sütun oluşturur", "difficulty": "hard", "topic_area": "CSS Grid"},
            {"id": 9, "question": "JavaScript'te async/await ne için kullanılır?", "options": ["Döngü için", "Asenkron işlemler için", "Değişken tanımı için", "CSS değiştirmek için"], "correct": "Asenkron işlemler için", "difficulty": "hard", "topic_area": "JavaScript Async"},
            {"id": 10, "question": "CORS hatası ne zaman oluşur?", "options": ["CSS hatası", "Farklı domain'e istek yapıldığında", "HTML hatası", "JavaScript sözdizimi hatası"], "correct": "Farklı domain'e istek yapıldığında", "difficulty": "hard", "topic_area": "Web Güvenliği"}
        ]
    
    def _get_data_assessment(self) -> List[Dict]:
        """Veri bilimi seviye belirleme soruları."""
        return [
            {"id": 1, "question": "Pandas'ta DataFrame nedir?", "options": ["Grafik türü", "2 boyutlu veri yapısı", "Dosya formatı", "Fonksiyon"], "correct": "2 boyutlu veri yapısı", "difficulty": "easy", "topic_area": "Pandas"},
            {"id": 2, "question": "NumPy ne için kullanılır?", "options": ["Web geliştirme", "Sayısal hesaplama", "Veritabanı", "Dosya işleme"], "correct": "Sayısal hesaplama", "difficulty": "easy", "topic_area": "NumPy"},
            {"id": 3, "question": "CSV dosyası ne tür veri içerir?", "options": ["Resim", "Video", "Tablo verisi", "Ses"], "correct": "Tablo verisi", "difficulty": "easy", "topic_area": "Veri Formatları"},
            {"id": 4, "question": "df.head() ne yapar?", "options": ["Son 5 satır", "İlk 5 satır", "Tüm veri", "Sütun isimleri"], "correct": "İlk 5 satır", "difficulty": "easy", "topic_area": "Pandas"},
            {"id": 5, "question": "df.groupby('sehir').mean() ne yapar?", "options": ["Şehirleri sıralar", "Şehir bazlı ortalama alır", "Şehirleri siler", "Şehir sayar"], "correct": "Şehir bazlı ortalama alır", "difficulty": "medium", "topic_area": "Pandas Gruplama"},
            {"id": 6, "question": "NaN değerler ne anlama gelir?", "options": ["Sıfır", "Eksik veri", "Negatif sayı", "Metin"], "correct": "Eksik veri", "difficulty": "medium", "topic_area": "Veri Temizleme"},
            {"id": 7, "question": "Matplotlib'de plt.scatter() ne çizer?", "options": ["Çizgi grafik", "Pasta grafik", "Dağılım grafiği", "Bar grafik"], "correct": "Dağılım grafiği", "difficulty": "medium", "topic_area": "Görselleştirme"},
            {"id": 8, "question": "Korelasyon katsayısı -1 ise ne anlama gelir?", "options": ["İlişki yok", "Güçlü pozitif", "Güçlü negatif", "Zayıf ilişki"], "correct": "Güçlü negatif", "difficulty": "hard", "topic_area": "İstatistik"},
            {"id": 9, "question": "Overfitting nedir?", "options": ["Az veri", "Modelin eğitim verisini ezberlemesi", "Yavaş çalışma", "Eksik özellik"], "correct": "Modelin eğitim verisini ezberlemesi", "difficulty": "hard", "topic_area": "Makine Öğrenmesi"},
            {"id": 10, "question": "Train-test split neden yapılır?", "options": ["Hız için", "Model performansını test etmek için", "Veri azaltmak için", "Görselleştirme için"], "correct": "Model performansını test etmek için", "difficulty": "hard", "topic_area": "Makine Öğrenmesi"}
        ]
    
    def _get_english_assessment(self) -> List[Dict]:
        """İngilizce seviye belirleme soruları."""
        return [
            {"id": 1, "question": "'Hello' ne demek?", "options": ["Hoşça kal", "Merhaba", "Teşekkürler", "Lütfen"], "correct": "Merhaba", "difficulty": "easy", "topic_area": "Temel Kelimeler"},
            {"id": 2, "question": "'I am' ne demek?", "options": ["Sen varsın", "Ben varım", "O var", "Biz varız"], "correct": "Ben varım", "difficulty": "easy", "topic_area": "To Be"},
            {"id": 3, "question": "'Book' kelimesinin Türkçesi nedir?", "options": ["Kalem", "Kitap", "Masa", "Sandalye"], "correct": "Kitap", "difficulty": "easy", "topic_area": "Temel Kelimeler"},
            {"id": 4, "question": "'She ___ a teacher.' boşluğa ne gelir?", "options": ["am", "is", "are", "be"], "correct": "is", "difficulty": "easy", "topic_area": "To Be"},
            {"id": 5, "question": "'I have been working' hangi zaman?", "options": ["Simple Past", "Present Perfect", "Present Perfect Continuous", "Future"], "correct": "Present Perfect Continuous", "difficulty": "medium", "topic_area": "Zamanlar"},
            {"id": 6, "question": "'If I were you...' ne tür cümle?", "options": ["Real conditional", "Unreal conditional", "Wish clause", "Reported speech"], "correct": "Unreal conditional", "difficulty": "medium", "topic_area": "Conditionals"},
            {"id": 7, "question": "'The book which I read...' - 'which' yerine ne kullanılabilir?", "options": ["who", "whom", "that", "whose"], "correct": "that", "difficulty": "medium", "topic_area": "Relative Clauses"},
            {"id": 8, "question": "'He suggested that I ___ early.' boşluğa ne gelir?", "options": ["leave", "leaves", "left", "leaving"], "correct": "leave", "difficulty": "hard", "topic_area": "Subjunctive"},
            {"id": 9, "question": "'Hardly had I arrived ___ it started raining.' boşluğa ne gelir?", "options": ["than", "when", "then", "that"], "correct": "when", "difficulty": "hard", "topic_area": "Inversion"},
            {"id": 10, "question": "'The more you practice, ___ you become.' boşluğa ne gelir?", "options": ["better", "the better", "best", "the best"], "correct": "the better", "difficulty": "hard", "topic_area": "Comparatives"}
        ]
    
    def _get_generic_assessment(self, topic: str) -> List[Dict]:
        """Genel seviye belirleme soruları."""
        return [
            {"id": 1, "question": f"{topic} konusunda daha önce deneyiminiz var mı?", "options": ["Hiç yok", "Biraz var", "Orta düzeyde", "İleri düzeyde"], "correct": "Biraz var", "difficulty": "easy", "topic_area": "Genel"},
            {"id": 2, "question": f"{topic} ile ilgili temel kavramları biliyor musunuz?", "options": ["Hayır", "Biraz", "Evet", "Çok iyi"], "correct": "Biraz", "difficulty": "easy", "topic_area": "Genel"},
            {"id": 3, "question": f"{topic} konusunda pratik yaptınız mı?", "options": ["Hiç", "Biraz", "Düzenli", "Profesyonel"], "correct": "Biraz", "difficulty": "medium", "topic_area": "Genel"}
        ]


# Singleton
_level_agent = None

def get_level_assessment_agent() -> LevelAssessmentAgent:
    global _level_agent
    if _level_agent is None:
        _level_agent = LevelAssessmentAgent()
    return _level_agent

