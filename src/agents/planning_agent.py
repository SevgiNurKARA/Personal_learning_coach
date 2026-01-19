"""
Planning Agent - Spesifik günlük planlar oluşturur
==================================================
Her görev net ve uygulanabilir olacak şekilde tasarlanmıştır.
"""

from typing import Dict, List, Optional

try:
    from tools.ai_service import AIService, get_ai_service
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


class PlanningAgent:
    """Kişiselleştirilmiş günlük planlar oluşturan agent."""
    
    def __init__(self, memory_service=None, ai_service: Optional['AIService'] = None):
        self.memory = memory_service
        self.ai_service = ai_service
        
        if self.ai_service is None and AI_AVAILABLE:
            try:
                self.ai_service = get_ai_service()
            except:
                pass
        
        # Konu bazlı müfredatlar
        self.curriculums = {
            "python": self._get_python_curriculum(),
            "web": self._get_web_curriculum(),
            "veri": self._get_data_curriculum(),
            "ingilizce": self._get_english_curriculum(),
            "genel": self._get_general_curriculum()
        }

    def generate_daily_plan(
        self, 
        profile: Dict, 
        resources: List[Dict], 
        day: int = 1,
        previous_evaluation: Optional[Dict] = None
    ) -> Dict:
        """Spesifik günlük plan oluşturur."""
        
        goal = profile.get("goal", "").lower()
        level = profile.get("level", "beginner")
        daily_time = profile.get("daily_time", 1)
        
        # Konuyu belirle
        if "python" in goal:
            curriculum = self.curriculums["python"]
            domain = "python"
        elif any(x in goal for x in ["web", "html", "css", "site"]):
            curriculum = self.curriculums["web"]
            domain = "web"
        elif any(x in goal for x in ["veri", "data", "analiz"]):
            curriculum = self.curriculums["veri"]
            domain = "veri"
        elif any(x in goal for x in ["ingilizce", "english"]):
            curriculum = self.curriculums["ingilizce"]
            domain = "ingilizce"
        else:
            curriculum = self.curriculums["genel"]
            domain = "genel"
        
        # Günün içeriğini al (döngüsel)
        day_index = (day - 1) % len(curriculum)
        day_content = curriculum[day_index]
        
        # Süreleri ayarla
        total_minutes = int(daily_time * 60)
        
        plan = {
            "type": "learning_plan",
            "day": day,
            "theme": day_content["theme"],
            "total_duration_min": total_minutes,
            "tasks": self._scale_tasks(day_content["tasks"], total_minutes),
            "resources": resources[:3] if resources else [],
            "learning_objectives": day_content["objectives"],
            "tips": day_content["tip"],
            "domain": domain,
            "level": level,
            "practice_exercise": day_content.get("exercise", "")
        }
        
        # Önceki değerlendirmeye göre ayarla
        if previous_evaluation:
            plan = self._adjust_plan(plan, previous_evaluation)
        
        # Belleğe kaydet
        if self.memory:
            self.memory.append_daily_plan(plan)
        
        return plan
    
    def _scale_tasks(self, tasks: List[Dict], total_minutes: int) -> List[Dict]:
        """Görevleri toplam süreye göre ölçekler."""
        # Orijinal toplam süre
        original_total = sum(t.get("duration_min", 20) for t in tasks)
        scale_factor = total_minutes / original_total if original_total > 0 else 1
        
        scaled_tasks = []
        for task in tasks:
            scaled_task = task.copy()
            scaled_task["duration_min"] = max(5, int(task.get("duration_min", 20) * scale_factor))
            scaled_tasks.append(scaled_task)
        
        return scaled_tasks
    
    def _adjust_plan(self, plan: Dict, evaluation: Dict) -> Dict:
        """Değerlendirmeye göre planı ayarlar."""
        score = evaluation.get("daily_score", 0)
        
        if score < 20:
            plan["tips"] = "⚠️ Önceki konuda zorlandınız. Bugün daha yavaş ilerleyin ve önceki konuyu tekrar edin."
        elif score >= 40:
            plan["tips"] = "🌟 Harika gidiyorsunuz! " + plan["tips"]
        
        return plan
    
    def _get_python_curriculum(self) -> List[Dict]:
        """Python müfredatı - 14 günlük döngü."""
        return [
            {
                "theme": "Python'a Giriş ve Kurulum",
                "tasks": [
                    {
                        "task_id": 1,
                        "task": "Python Kurulumu",
                        "type": "theory",
                        "duration_min": 15,
                        "description": "python.org'dan Python 3.x indirin ve kurun. Kurulum sırasında 'Add to PATH' seçeneğini işaretleyin.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 2,
                        "task": "İlk Program: Merhaba Dünya",
                        "type": "practice",
                        "duration_min": 20,
                        "description": "Bir metin editörü açın, 'merhaba.py' dosyası oluşturun ve print('Merhaba Dünya!') yazıp çalıştırın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 3,
                        "task": "Quiz: Python Temelleri",
                        "type": "quiz",
                        "duration_min": 10,
                        "description": "Python'un ne olduğu ve temel kullanımı hakkında quiz çözün.",
                        "priority": "medium",
                        "completed": False
                    }
                ],
                "objectives": [
                    "Python'u bilgisayarınıza kurmak",
                    "İlk Python programınızı yazmak ve çalıştırmak",
                    "print() fonksiyonunu kullanmak"
                ],
                "tip": "💡 Python'u kurduktan sonra terminal/cmd'de 'python --version' yazarak kontrol edin.",
                "exercise": "Ekrana kendi adınızı ve yaşınızı yazdıran bir program yazın."
            },
            {
                "theme": "Değişkenler ve Veri Tipleri",
                "tasks": [
                    {
                        "task_id": 1,
                        "task": "Değişken Tanımlama",
                        "type": "theory",
                        "duration_min": 20,
                        "description": "W3Schools'dan 'Python Variables' konusunu okuyun. String, int, float, bool tiplerini öğrenin.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 2,
                        "task": "Kişisel Bilgi Programı",
                        "type": "practice",
                        "duration_min": 25,
                        "description": "isim, yas, boy, ogrenci_mi değişkenlerini tanımlayın ve f-string ile ekrana yazdırın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 3,
                        "task": "Quiz: Veri Tipleri",
                        "type": "quiz",
                        "duration_min": 10,
                        "description": "Değişkenler ve veri tipleri hakkında quiz çözün.",
                        "priority": "medium",
                        "completed": False
                    }
                ],
                "objectives": [
                    "Değişken tanımlama kurallarını öğrenmek",
                    "str, int, float, bool tiplerini anlamak",
                    "f-string ile formatlı yazdırma yapmak"
                ],
                "tip": "💡 type() fonksiyonu ile değişkenin tipini kontrol edebilirsiniz: type(degisken)",
                "exercise": "Bir ürünün adı, fiyatı ve stok durumunu tutan değişkenler oluşturun."
            },
            {
                "theme": "String İşlemleri",
                "tasks": [
                    {
                        "task_id": 1,
                        "task": "String Metodları",
                        "type": "theory",
                        "duration_min": 20,
                        "description": "upper(), lower(), strip(), split(), replace() metodlarını öğrenin. W3Schools 'Python Strings' bölümünü okuyun.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 2,
                        "task": "Metin İşleme Programı",
                        "type": "practice",
                        "duration_min": 25,
                        "description": "Kullanıcıdan alınan metni büyük harfe çeviren, kelime sayısını bulan bir program yazın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 3,
                        "task": "Quiz: String İşlemleri",
                        "type": "quiz",
                        "duration_min": 10,
                        "description": "String metodları ve indeksleme hakkında quiz çözün.",
                        "priority": "medium",
                        "completed": False
                    }
                ],
                "objectives": [
                    "String metodlarını kullanmak",
                    "String indeksleme ve dilimleme yapmak",
                    "len() fonksiyonunu kullanmak"
                ],
                "tip": "💡 String'ler değiştirilemez (immutable). metin[0] = 'X' hata verir!",
                "exercise": "Email adresinden kullanıcı adını ayıklayan bir program yazın."
            },
            {
                "theme": "Sayılar ve Operatörler",
                "tasks": [
                    {
                        "task_id": 1,
                        "task": "Aritmetik Operatörler",
                        "type": "theory",
                        "duration_min": 15,
                        "description": "+, -, *, /, //, %, ** operatörlerini öğrenin. Özellikle // (tam bölme) ve % (mod) farkını anlayın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 2,
                        "task": "Hesap Makinesi",
                        "type": "practice",
                        "duration_min": 30,
                        "description": "İki sayı alan ve dört işlemi yapan basit bir hesap makinesi programı yazın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 3,
                        "task": "Quiz: Operatörler",
                        "type": "quiz",
                        "duration_min": 10,
                        "description": "Aritmetik ve karşılaştırma operatörleri hakkında quiz çözün.",
                        "priority": "medium",
                        "completed": False
                    }
                ],
                "objectives": [
                    "Aritmetik operatörleri kullanmak",
                    "// ve % operatörlerini anlamak",
                    "input() ile kullanıcıdan sayı almak"
                ],
                "tip": "💡 input() her zaman string döner. Sayı için int() veya float() kullanın.",
                "exercise": "Daire alanı ve çevresi hesaplayan program yazın (pi = 3.14159)."
            },
            {
                "theme": "Koşullu İfadeler (if-else)",
                "tasks": [
                    {
                        "task_id": 1,
                        "task": "if-elif-else Yapısı",
                        "type": "theory",
                        "duration_min": 20,
                        "description": "if, elif, else yapısını öğrenin. and, or, not mantıksal operatörlerini anlayın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 2,
                        "task": "Not Hesaplama Programı",
                        "type": "practice",
                        "duration_min": 25,
                        "description": "Girilen nota göre harf notu (AA, BA, BB, CB, CC, DC, DD, FF) veren program yazın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 3,
                        "task": "Quiz: Koşullar",
                        "type": "quiz",
                        "duration_min": 10,
                        "description": "if-else ve mantıksal operatörler hakkında quiz çözün.",
                        "priority": "medium",
                        "completed": False
                    }
                ],
                "objectives": [
                    "if-elif-else yapısını kullanmak",
                    "Mantıksal operatörleri (and, or, not) anlamak",
                    "İç içe koşullar yazmak"
                ],
                "tip": "💡 Python'da girintiler (4 boşluk) zorunludur! Yanlış girinti = Hata",
                "exercise": "Yaşa göre bilet fiyatı hesaplayan program yazın (çocuk/yetişkin/yaşlı)."
            },
            {
                "theme": "for Döngüsü",
                "tasks": [
                    {
                        "task_id": 1,
                        "task": "for ve range()",
                        "type": "theory",
                        "duration_min": 20,
                        "description": "for döngüsü ve range() fonksiyonunu öğrenin. range(n), range(a,b), range(a,b,c) kullanımlarını anlayın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 2,
                        "task": "Çarpım Tablosu",
                        "type": "practice",
                        "duration_min": 25,
                        "description": "1'den 10'a kadar çarpım tablosu yazdıran program yazın. İç içe for kullanın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 3,
                        "task": "Quiz: for Döngüsü",
                        "type": "quiz",
                        "duration_min": 10,
                        "description": "for döngüsü ve range() hakkında quiz çözün.",
                        "priority": "medium",
                        "completed": False
                    }
                ],
                "objectives": [
                    "for döngüsünü kullanmak",
                    "range() fonksiyonunu anlamak",
                    "İç içe döngüler yazmak"
                ],
                "tip": "💡 range(5) = 0,1,2,3,4 üretir. 5 dahil değil!",
                "exercise": "1'den N'e kadar sayıların toplamını hesaplayan program yazın."
            },
            {
                "theme": "while Döngüsü ve Kontrol",
                "tasks": [
                    {
                        "task_id": 1,
                        "task": "while, break, continue",
                        "type": "theory",
                        "duration_min": 20,
                        "description": "while döngüsü, break ve continue ifadelerini öğrenin. Sonsuz döngüden kaçınmayı anlayın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 2,
                        "task": "Sayı Tahmin Oyunu",
                        "type": "practice",
                        "duration_min": 30,
                        "description": "1-100 arası rastgele sayı tutan, kullanıcıya ipucu veren (büyük/küçük) tahmin oyunu yazın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 3,
                        "task": "Quiz: while Döngüsü",
                        "type": "quiz",
                        "duration_min": 10,
                        "description": "while döngüsü ve kontrol ifadeleri hakkında quiz çözün.",
                        "priority": "medium",
                        "completed": False
                    }
                ],
                "objectives": [
                    "while döngüsünü kullanmak",
                    "break ve continue'yu anlamak",
                    "random modülünü kullanmak"
                ],
                "tip": "💡 import random; random.randint(1, 100) ile rastgele sayı üretin.",
                "exercise": "Kullanıcı 'çık' yazana kadar devam eden bir sohbet programı yazın."
            },
            {
                "theme": "Listeler",
                "tasks": [
                    {
                        "task_id": 1,
                        "task": "Liste Oluşturma ve Metodları",
                        "type": "theory",
                        "duration_min": 20,
                        "description": "Liste oluşturma, append(), remove(), pop(), sort() metodlarını öğrenin. Liste indekslemeyi anlayın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 2,
                        "task": "Alışveriş Listesi Programı",
                        "type": "practice",
                        "duration_min": 30,
                        "description": "Ürün ekleme, silme, listeleme yapabilen bir alışveriş listesi programı yazın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 3,
                        "task": "Quiz: Listeler",
                        "type": "quiz",
                        "duration_min": 10,
                        "description": "Liste metodları ve işlemleri hakkında quiz çözün.",
                        "priority": "medium",
                        "completed": False
                    }
                ],
                "objectives": [
                    "Liste oluşturmak ve elemanlarına erişmek",
                    "Liste metodlarını kullanmak",
                    "Liste üzerinde döngü yazmak"
                ],
                "tip": "💡 liste[-1] son elemanı verir. liste[1:3] dilimleme yapar.",
                "exercise": "Notları listeye ekleyip ortalama hesaplayan program yazın."
            },
            {
                "theme": "Dictionary (Sözlük)",
                "tasks": [
                    {
                        "task_id": 1,
                        "task": "Dictionary Yapısı",
                        "type": "theory",
                        "duration_min": 20,
                        "description": "Dictionary oluşturma, anahtar-değer erişimi, keys(), values(), items() metodlarını öğrenin.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 2,
                        "task": "Telefon Rehberi",
                        "type": "practice",
                        "duration_min": 30,
                        "description": "İsim-telefon kaydeden, arayan, silen bir telefon rehberi programı yazın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 3,
                        "task": "Quiz: Dictionary",
                        "type": "quiz",
                        "duration_min": 10,
                        "description": "Dictionary yapısı ve metodları hakkında quiz çözün.",
                        "priority": "medium",
                        "completed": False
                    }
                ],
                "objectives": [
                    "Dictionary oluşturmak",
                    "Anahtar ile değere erişmek",
                    "Dictionary üzerinde döngü yazmak"
                ],
                "tip": "💡 dict.get('key', 'varsayilan') ile KeyError'dan kaçının.",
                "exercise": "Ürün-fiyat dictionary'si ile market kasa programı yazın."
            },
            {
                "theme": "Fonksiyonlar",
                "tasks": [
                    {
                        "task_id": 1,
                        "task": "Fonksiyon Tanımlama",
                        "type": "theory",
                        "duration_min": 20,
                        "description": "def ile fonksiyon tanımlama, parametreler, return ifadesi, varsayılan parametreleri öğrenin.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 2,
                        "task": "Matematik Fonksiyonları",
                        "type": "practice",
                        "duration_min": 30,
                        "description": "Faktöriyel, asal sayı kontrolü, fibonacci hesaplayan fonksiyonlar yazın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 3,
                        "task": "Quiz: Fonksiyonlar",
                        "type": "quiz",
                        "duration_min": 10,
                        "description": "Fonksiyon tanımlama ve kullanımı hakkında quiz çözün.",
                        "priority": "medium",
                        "completed": False
                    }
                ],
                "objectives": [
                    "Fonksiyon tanımlamak ve çağırmak",
                    "Parametre ve return kullanmak",
                    "Varsayılan parametre değeri vermek"
                ],
                "tip": "💡 Fonksiyon isimleri küçük harf ve alt çizgi kullanın: hesapla_ortalama()",
                "exercise": "Sıcaklık dönüştürücü fonksiyonlar yazın (C↔F)."
            },
            {
                "theme": "Dosya İşlemleri",
                "tasks": [
                    {
                        "task_id": 1,
                        "task": "Dosya Okuma/Yazma",
                        "type": "theory",
                        "duration_min": 20,
                        "description": "open(), read(), write(), with statement kullanımını öğrenin. 'r', 'w', 'a' modlarını anlayın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 2,
                        "task": "Not Defteri Programı",
                        "type": "practice",
                        "duration_min": 30,
                        "description": "Metin dosyasına not ekleyen, okuyan, silen bir not defteri programı yazın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 3,
                        "task": "Quiz: Dosya İşlemleri",
                        "type": "quiz",
                        "duration_min": 10,
                        "description": "Dosya okuma/yazma işlemleri hakkında quiz çözün.",
                        "priority": "medium",
                        "completed": False
                    }
                ],
                "objectives": [
                    "Dosya açmak ve kapatmak",
                    "with statement kullanmak",
                    "Dosya modlarını anlamak (r, w, a)"
                ],
                "tip": "💡 with open('dosya.txt', 'r') as f: kullanın - otomatik kapatır.",
                "exercise": "Yapılacaklar listesini dosyaya kaydeden program yazın."
            },
            {
                "theme": "Hata Yönetimi (try-except)",
                "tasks": [
                    {
                        "task_id": 1,
                        "task": "try-except Yapısı",
                        "type": "theory",
                        "duration_min": 20,
                        "description": "try, except, finally yapısını öğrenin. ValueError, TypeError, FileNotFoundError gibi hataları anlayın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 2,
                        "task": "Güvenli Hesap Makinesi",
                        "type": "practice",
                        "duration_min": 25,
                        "description": "Hatalı girişlerde çökmeyip uyarı veren güvenli bir hesap makinesi yazın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 3,
                        "task": "Quiz: Hata Yönetimi",
                        "type": "quiz",
                        "duration_min": 10,
                        "description": "try-except ve hata türleri hakkında quiz çözün.",
                        "priority": "medium",
                        "completed": False
                    }
                ],
                "objectives": [
                    "try-except yapısını kullanmak",
                    "Farklı hata türlerini yakalamak",
                    "finally bloğunu anlamak"
                ],
                "tip": "💡 except Exception as e: ile hatanın mesajını alabilirsiniz.",
                "exercise": "Dosya okurken hata yönetimi yapan program yazın."
            },
            {
                "theme": "Modüller ve Paketler",
                "tasks": [
                    {
                        "task_id": 1,
                        "task": "import Kullanımı",
                        "type": "theory",
                        "duration_min": 20,
                        "description": "import, from...import, as kullanımlarını öğrenin. math, random, datetime modüllerini tanıyın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 2,
                        "task": "Tarih/Saat Programı",
                        "type": "practice",
                        "duration_min": 25,
                        "description": "datetime modülü ile bugünün tarihi, iki tarih arası fark hesaplayan program yazın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 3,
                        "task": "Quiz: Modüller",
                        "type": "quiz",
                        "duration_min": 10,
                        "description": "Modül import etme ve kullanımı hakkında quiz çözün.",
                        "priority": "medium",
                        "completed": False
                    }
                ],
                "objectives": [
                    "Modül import etmek",
                    "Standart kütüphane modüllerini kullanmak",
                    "Kendi modülünüzü oluşturmak"
                ],
                "tip": "💡 pip install paket_adi ile harici paketler kurabilirsiniz.",
                "exercise": "Doğum tarihinize kaç gün kaldığını hesaplayan program yazın."
            },
            {
                "theme": "Mini Proje: Kişisel Asistan",
                "tasks": [
                    {
                        "task_id": 1,
                        "task": "Proje Planlama",
                        "type": "theory",
                        "duration_min": 15,
                        "description": "Öğrendiğiniz tüm konuları birleştiren bir proje planlayın: menü, dosya kayıt, fonksiyonlar.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 2,
                        "task": "Proje Kodlama",
                        "type": "practice",
                        "duration_min": 40,
                        "description": "Not alma, yapılacaklar listesi, hesap makinesi özellikli kişisel asistan programı yazın.",
                        "priority": "high",
                        "completed": False
                    },
                    {
                        "task_id": 3,
                        "task": "Proje Değerlendirme",
                        "type": "quiz",
                        "duration_min": 10,
                        "description": "Projenizi test edin, hataları düzeltin, iyileştirmeler yapın.",
                        "priority": "medium",
                        "completed": False
                    }
                ],
                "objectives": [
                    "Öğrenilenleri bir projede birleştirmek",
                    "Modüler kod yazmak",
                    "Hata yönetimi uygulamak"
                ],
                "tip": "💡 Projeyi küçük parçalara bölün ve adım adım geliştirin.",
                "exercise": "Projenize yeni bir özellik ekleyin (örn: hatırlatıcı)."
            }
        ]
    
    def _get_web_curriculum(self) -> List[Dict]:
        """Web geliştirme müfredatı."""
        return [
            {
                "theme": "HTML'e Giriş",
                "tasks": [
                    {"task_id": 1, "task": "HTML Temel Yapısı", "type": "theory", "duration_min": 20, 
                     "description": "W3Schools'dan HTML temel yapısını öğrenin: <!DOCTYPE>, <html>, <head>, <body> etiketleri.", "priority": "high", "completed": False},
                    {"task_id": 2, "task": "İlk Web Sayfası", "type": "practice", "duration_min": 25,
                     "description": "Başlık, paragraf ve resim içeren basit bir HTML sayfası oluşturun.", "priority": "high", "completed": False},
                    {"task_id": 3, "task": "Quiz: HTML Temelleri", "type": "quiz", "duration_min": 10,
                     "description": "HTML etiketleri hakkında quiz çözün.", "priority": "medium", "completed": False}
                ],
                "objectives": ["HTML dosya yapısını anlamak", "Temel etiketleri kullanmak", "Tarayıcıda sayfa görüntülemek"],
                "tip": "💡 HTML dosyalarını .html uzantısıyla kaydedin ve tarayıcıda açın.",
                "exercise": "Kendinizi tanıtan bir web sayfası yapın."
            },
            {
                "theme": "CSS'e Giriş",
                "tasks": [
                    {"task_id": 1, "task": "CSS Temelleri", "type": "theory", "duration_min": 20,
                     "description": "CSS seçiciler, renkler, fontlar, margin/padding öğrenin.", "priority": "high", "completed": False},
                    {"task_id": 2, "task": "Sayfayı Stillendirme", "type": "practice", "duration_min": 25,
                     "description": "Dünkü HTML sayfanıza CSS ekleyerek güzelleştirin.", "priority": "high", "completed": False},
                    {"task_id": 3, "task": "Quiz: CSS", "type": "quiz", "duration_min": 10,
                     "description": "CSS özellikleri hakkında quiz çözün.", "priority": "medium", "completed": False}
                ],
                "objectives": ["CSS ile stil vermek", "Renk ve font ayarlamak", "Box model'i anlamak"],
                "tip": "💡 Chrome DevTools (F12) ile CSS'i canlı düzenleyebilirsiniz.",
                "exercise": "Sayfanıza hover efekti ekleyin."
            }
        ]
    
    def _get_data_curriculum(self) -> List[Dict]:
        """Veri bilimi müfredatı."""
        return [
            {
                "theme": "Pandas'a Giriş",
                "tasks": [
                    {"task_id": 1, "task": "DataFrame Oluşturma", "type": "theory", "duration_min": 20,
                     "description": "Pandas kurulumu, DataFrame ve Series yapılarını öğrenin.", "priority": "high", "completed": False},
                    {"task_id": 2, "task": "CSV Dosyası Okuma", "type": "practice", "duration_min": 25,
                     "description": "Kaggle'dan bir CSV indirin ve pandas ile okuyun, head(), info(), describe() kullanın.", "priority": "high", "completed": False},
                    {"task_id": 3, "task": "Quiz: Pandas Temelleri", "type": "quiz", "duration_min": 10,
                     "description": "Pandas temel işlemleri hakkında quiz çözün.", "priority": "medium", "completed": False}
                ],
                "objectives": ["Pandas kurulumu yapmak", "DataFrame oluşturmak", "CSV dosyası okumak"],
                "tip": "💡 pip install pandas ile Pandas'ı kurun.",
                "exercise": "Bir veri setinin ilk 10 satırını görüntüleyin."
            }
        ]
    
    def _get_english_curriculum(self) -> List[Dict]:
        """İngilizce müfredatı."""
        return [
            {
                "theme": "Temel Kelimeler ve Selamlaşma",
                "tasks": [
                    {"task_id": 1, "task": "Günlük Kelimeler", "type": "theory", "duration_min": 20,
                     "description": "En sık kullanılan 50 İngilizce kelimeyi öğrenin: hello, thank you, please, sorry, yes, no...", "priority": "high", "completed": False},
                    {"task_id": 2, "task": "Telaffuz Pratiği", "type": "practice", "duration_min": 25,
                     "description": "Cambridge Dictionary'de kelimelerin telaffuzlarını dinleyin ve tekrarlayın.", "priority": "high", "completed": False},
                    {"task_id": 3, "task": "Quiz: Temel Kelimeler", "type": "quiz", "duration_min": 10,
                     "description": "Öğrendiğiniz kelimeler hakkında quiz çözün.", "priority": "medium", "completed": False}
                ],
                "objectives": ["Temel selamlaşma ifadelerini öğrenmek", "Doğru telaffuz yapmak", "Günlük kelimeleri ezberlemek"],
                "tip": "💡 Her gün 10 yeni kelime öğrenin ve cümle içinde kullanın.",
                "exercise": "Öğrendiğiniz 10 kelimeyle kısa cümleler yazın."
            }
        ]
    
    def _get_general_curriculum(self) -> List[Dict]:
        """Genel öğrenme müfredatı."""
        return [
            {
                "theme": "Öğrenme Stratejileri",
                "tasks": [
                    {"task_id": 1, "task": "Hedef Belirleme", "type": "theory", "duration_min": 20,
                     "description": "SMART hedefler belirlemeyi öğrenin: Specific, Measurable, Achievable, Relevant, Time-bound.", "priority": "high", "completed": False},
                    {"task_id": 2, "task": "Çalışma Planı", "type": "practice", "duration_min": 25,
                     "description": "Haftalık çalışma planınızı oluşturun. Her gün için spesifik hedefler belirleyin.", "priority": "high", "completed": False},
                    {"task_id": 3, "task": "Quiz: Öğrenme", "type": "quiz", "duration_min": 10,
                     "description": "Etkili öğrenme teknikleri hakkında quiz çözün.", "priority": "medium", "completed": False}
                ],
                "objectives": ["Etkili hedef belirlemek", "Çalışma planı oluşturmak", "Motivasyonu korumak"],
                "tip": "💡 Pomodoro tekniği: 25 dk çalış, 5 dk mola ver.",
                "exercise": "Bu hafta için 3 SMART hedef yazın."
            }
        ]
    
    def get_weekly_overview(self, profile: Dict) -> Dict:
        """Haftalık genel bakış."""
        daily_time = profile.get("daily_time", 1)
        goal = profile.get("goal", "Genel öğrenme")
        
        return {
            "type": "weekly_overview",
            "goal": goal,
            "total_hours": daily_time * 7,
            "message": f"Bu hafta {goal} için toplam {daily_time * 7} saat çalışacaksınız."
        }
