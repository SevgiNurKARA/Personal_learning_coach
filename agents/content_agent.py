"""
Content Agent - Ders içeriği ve quiz üretimi
=============================================
AI varsa Gemini kullanır, yoksa konu bazlı hazır içerik döndürür.
"""

from typing import Dict, List, Optional
import os

try:
    from tools.ai_service import get_ai_service
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False


class ContentAgent:
    """Ders içeriği ve quiz üreten agent."""
    
    def __init__(self):
        self.ai_service = None
        if AI_AVAILABLE:
            try:
                self.ai_service = get_ai_service()
            except:
                pass
    
    def _is_ai_available(self) -> bool:
        """AI servisinin kullanılabilir olup olmadığını kontrol eder."""
        return self.ai_service is not None and self.ai_service._is_configured()
    
    def generate_lesson_content(self, topic: str, level: str = "beginner", goal: str = "") -> str:
        """
        Ders içeriği üretir - TAMAMEN AI TABANLI.
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
    
    def generate_quiz(self, topic: str, level: str = "beginner", num_questions: int = 5, goal: str = "") -> List[Dict]:
        """
        Quiz soruları üretir - TAMAMEN AI TABANLI.
        
        Args:
            topic: Konu başlığı
            level: Seviye (beginner/intermediate/advanced)
            num_questions: Soru sayısı
            goal: Kullanıcı hedefi
        
        Returns:
            Quiz soruları listesi (AI'dan)
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
            print(f"⚠️ AI servisi kullanılamıyor")
        
        # AI çalışmazsa minimal fallback
        return self._get_minimal_fallback_quiz(topic, num_questions)
    
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
    
    def _get_static_content_DEPRECATED(self, topic: str, level: str, goal: str) -> str:
        """Konu bazlı hazır içerik döndürür."""
        
        topic_lower = topic.lower()
        goal_lower = goal.lower() if goal else ""
        
        # Python içerikleri
        if "python" in topic_lower or "python" in goal_lower:
            return self._get_python_content(topic_lower, level)
        
        # Web geliştirme içerikleri
        elif any(x in topic_lower or x in goal_lower for x in ["web", "html", "css", "javascript"]):
            return self._get_web_content(topic_lower, level)
        
        # Veri bilimi içerikleri
        elif any(x in topic_lower or x in goal_lower for x in ["veri", "data", "analiz", "pandas"]):
            return self._get_data_content(topic_lower, level)
        
        # İngilizce içerikleri
        elif any(x in topic_lower or x in goal_lower for x in ["ingilizce", "english", "dil"]):
            return self._get_english_content(topic_lower, level)
        
        # Genel içerik
        else:
            return self._get_general_content(topic, level, goal)
    
    def _get_python_content(self, topic: str, level: str) -> str:
        """Python ders içeriği."""
        
        if "temel" in topic or "giriş" in topic or level == "beginner":
            return """
# 🐍 Python'a Giriş

## Python Nedir?
Python, 1991'de Guido van Rossum tarafından geliştirilen, okunması kolay ve güçlü bir programlama dilidir.

## Neden Python Öğrenmeliyiz?
- ✅ **Kolay Sözdizimi**: İngilizceye yakın, okunması kolay
- ✅ **Geniş Kullanım Alanı**: Web, veri bilimi, yapay zeka, otomasyon
- ✅ **Büyük Topluluk**: Sorunlarınıza hızlı çözüm bulabilirsiniz
- ✅ **Zengin Kütüphaneler**: Hazır araçlarla hızlı geliştirme

## İlk Python Programı

```python
# Bu bir yorum satırıdır
print("Merhaba Dünya!")
print("Python öğreniyorum!")
```

## Değişkenler

```python
# Metin (string)
isim = "Ahmet"

# Sayı (integer)
yas = 25

# Ondalıklı sayı (float)
boy = 1.75

# Mantıksal (boolean)
ogrenci_mi = True

# Yazdırma
print(f"Merhaba {isim}, yaşınız {yas}")
```

## Temel Veri Tipleri

| Tip | Örnek | Açıklama |
|-----|-------|----------|
| str | "Merhaba" | Metin |
| int | 42 | Tam sayı |
| float | 3.14 | Ondalıklı sayı |
| bool | True/False | Mantıksal |
| list | [1, 2, 3] | Liste |
| dict | {"ad": "Ali"} | Sözlük |

## Pratik Yapın!
1. Python'u bilgisayarınıza kurun
2. Bir `.py` dosyası oluşturun
3. `print("Merhaba!")` yazıp çalıştırın
4. Kendi değişkenlerinizi tanımlayın

💡 **İpucu**: Her gün en az 30 dakika kod yazın!
"""
        
        elif "değişken" in topic or "veri tip" in topic:
            return """
# 📦 Değişkenler ve Veri Tipleri

## Değişken Nedir?
Değişkenler, verileri saklamak için kullanılan isimlendirilmiş kutulardır.

## Değişken Tanımlama

```python
# String (metin)
isim = "Ayşe"
mesaj = 'Merhaba!'

# Integer (tam sayı)
yas = 30
yil = 2024

# Float (ondalıklı sayı)
fiyat = 99.99
pi = 3.14159

# Boolean (mantıksal)
aktif = True
silindi = False
```

## İsimlendirme Kuralları

✅ **Doğru:**
```python
kullanici_adi = "ali123"
sayi1 = 10
_ozel = "gizli"
```

❌ **Yanlış:**
```python
2sayi = 10      # Rakamla başlayamaz
kullanıcı adı = "x"  # Boşluk olamaz
class = "A"     # Anahtar kelime olamaz
```

## Tip Dönüşümü

```python
# String'den sayıya
sayi_str = "42"
sayi_int = int(sayi_str)    # 42
sayi_float = float(sayi_str) # 42.0

# Sayıdan string'e
yas = 25
yas_str = str(yas)  # "25"

# Tip kontrolü
print(type(isim))   # <class 'str'>
print(type(yas))    # <class 'int'>
```

## Alıştırma

```python
# Kendinizi tanıtan değişkenler oluşturun
ad = "..."
soyad = "..."
yas = ...
boy = ...
ogrenci = True

# Bilgileri yazdırın
print(f"Ben {ad} {soyad}")
print(f"Yaşım: {yas}, Boyum: {boy}")
```

💡 **İpucu**: `type()` fonksiyonu ile her değişkenin tipini kontrol edebilirsiniz!
"""
        
        elif "kontrol" in topic or "if" in topic or "döngü" in topic or "loop" in topic:
            return """
# 🔀 Kontrol Yapıları

## if-else Koşulları

```python
yas = 18

if yas >= 18:
    print("Yetişkinsiniz")
else:
    print("Reşit değilsiniz")
```

## elif (else if)

```python
not_ort = 75

if not_ort >= 90:
    print("AA - Mükemmel!")
elif not_ort >= 80:
    print("BA - Çok iyi")
elif not_ort >= 70:
    print("BB - İyi")
elif not_ort >= 60:
    print("CB - Orta")
else:
    print("Kaldınız")
```

## Mantıksal Operatörler

```python
yas = 25
gelir = 5000

# and - her ikisi de doğru olmalı
if yas >= 18 and gelir >= 3000:
    print("Kredi alabilirsiniz")

# or - en az biri doğru olmalı
if yas < 18 or yas > 65:
    print("İndirimli bilet")

# not - tersine çevirir
if not yas < 18:
    print("18 yaş üstü")
```

## for Döngüsü

```python
# range ile
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# Liste ile
meyveler = ["elma", "armut", "muz"]
for meyve in meyveler:
    print(meyve)
```

## while Döngüsü

```python
sayac = 0
while sayac < 5:
    print(sayac)
    sayac += 1
```

## break ve continue

```python
# break - döngüyü sonlandırır
for i in range(10):
    if i == 5:
        break
    print(i)  # 0, 1, 2, 3, 4

# continue - sonraki iterasyona geçer
for i in range(5):
    if i == 2:
        continue
    print(i)  # 0, 1, 3, 4
```

💡 **İpucu**: Python'da girintiler (4 boşluk) çok önemlidir!
"""
        
        elif "fonksiyon" in topic or "function" in topic:
            return """
# 🔧 Fonksiyonlar

## Fonksiyon Nedir?
Fonksiyonlar, belirli bir görevi yapan ve tekrar kullanılabilen kod bloklarıdır.

## Basit Fonksiyon

```python
def selamla():
    print("Merhaba!")

# Çağırma
selamla()  # Merhaba!
```

## Parametreli Fonksiyon

```python
def selamla(isim):
    print(f"Merhaba {isim}!")

selamla("Ahmet")  # Merhaba Ahmet!
selamla("Ayşe")   # Merhaba Ayşe!
```

## Değer Döndüren Fonksiyon

```python
def topla(a, b):
    return a + b

sonuc = topla(5, 3)
print(sonuc)  # 8
```

## Varsayılan Parametre

```python
def selamla(isim, mesaj="Merhaba"):
    print(f"{mesaj} {isim}!")

selamla("Ali")           # Merhaba Ali!
selamla("Ali", "Günaydın")  # Günaydın Ali!
```

## Birden Fazla Değer Döndürme

```python
def hesapla(a, b):
    toplam = a + b
    fark = a - b
    return toplam, fark

t, f = hesapla(10, 3)
print(f"Toplam: {t}, Fark: {f}")
```

## Lambda (Anonim Fonksiyon)

```python
# Normal fonksiyon
def kare(x):
    return x ** 2

# Lambda ile aynısı
kare = lambda x: x ** 2

print(kare(5))  # 25
```

💡 **İpucu**: Fonksiyonlar kodunuzu düzenli ve tekrar kullanılabilir yapar!
"""
        
        else:
            return """
# 🐍 Python Öğrenme Rehberi

## Bu Derste Öğrenecekleriniz

Python programlama dilinin temellerini öğreneceksiniz:

1. **Değişkenler ve Veri Tipleri**
   - String, int, float, bool
   - Liste, dictionary, tuple

2. **Kontrol Yapıları**
   - if-else koşulları
   - for ve while döngüleri

3. **Fonksiyonlar**
   - Fonksiyon tanımlama
   - Parametreler ve dönüş değerleri

4. **Modüller**
   - import kullanımı
   - Kendi modüllerinizi oluşturma

## Örnek Kod

```python
# Basit bir Python programı
def merhaba(isim):
    return f"Merhaba {isim}!"

# Kullanım
mesaj = merhaba("Dünya")
print(mesaj)

# Liste işlemleri
sayilar = [1, 2, 3, 4, 5]
for sayi in sayilar:
    print(sayi * 2)
```

## Kaynaklar
- [Python Resmi Dokümantasyonu](https://docs.python.org/3/)
- [W3Schools Python](https://www.w3schools.com/python/)
- [Real Python](https://realpython.com/)

💡 **İpucu**: Her gün kod yazarak pratik yapın!
"""
    
    def _get_web_content(self, topic: str, level: str) -> str:
        """Web geliştirme ders içeriği."""
        return """
# 🌐 Web Geliştirme Temelleri

## Web Nasıl Çalışır?

1. **HTML** - Sayfanın yapısı (iskelet)
2. **CSS** - Sayfanın görünümü (stil)
3. **JavaScript** - Sayfanın davranışı (etkileşim)

## HTML Temelleri

```html
<!DOCTYPE html>
<html>
<head>
    <title>İlk Sayfam</title>
</head>
<body>
    <h1>Merhaba Dünya!</h1>
    <p>Bu benim ilk web sayfam.</p>
    <a href="https://google.com">Google'a Git</a>
</body>
</html>
```

## Temel HTML Etiketleri

| Etiket | Açıklama |
|--------|----------|
| `<h1>-<h6>` | Başlıklar |
| `<p>` | Paragraf |
| `<a>` | Link |
| `<img>` | Resim |
| `<div>` | Bölüm |
| `<span>` | Satır içi bölüm |
| `<ul>, <ol>` | Liste |

## CSS Temelleri

```css
/* Stil tanımlama */
h1 {
    color: blue;
    font-size: 24px;
}

.kutu {
    background-color: #f0f0f0;
    padding: 20px;
    border-radius: 10px;
}
```

## JavaScript Temelleri

```javascript
// Değişken
let isim = "Ahmet";

// Fonksiyon
function selamla() {
    alert("Merhaba " + isim);
}

// Olay dinleyici
document.getElementById("btn").onclick = selamla;
```

💡 **İpucu**: Önce HTML ve CSS'i öğrenin, sonra JavaScript'e geçin!
"""
    
    def _get_data_content(self, topic: str, level: str) -> str:
        """Veri bilimi ders içeriği."""
        return """
# 📊 Veri Bilimi Temelleri

## Veri Bilimi Nedir?
Veriden anlamlı bilgiler çıkarmak için istatistik, programlama ve alan bilgisini birleştiren disiplindir.

## Python Kütüphaneleri

### NumPy - Sayısal İşlemler
```python
import numpy as np

# Dizi oluşturma
arr = np.array([1, 2, 3, 4, 5])
print(arr.mean())  # Ortalama: 3.0
print(arr.std())   # Standart sapma
```

### Pandas - Veri Analizi
```python
import pandas as pd

# DataFrame oluşturma
df = pd.DataFrame({
    'isim': ['Ali', 'Ayşe', 'Mehmet'],
    'yas': [25, 30, 35],
    'sehir': ['İstanbul', 'Ankara', 'İzmir']
})

# Temel işlemler
print(df.head())      # İlk 5 satır
print(df.describe())  # İstatistikler
print(df['yas'].mean())  # Yaş ortalaması
```

### Matplotlib - Görselleştirme
```python
import matplotlib.pyplot as plt

x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.plot(x, y)
plt.xlabel('X Ekseni')
plt.ylabel('Y Ekseni')
plt.title('Basit Grafik')
plt.show()
```

## Veri Analizi Adımları

1. **Veri Toplama** - CSV, API, veritabanı
2. **Veri Temizleme** - Eksik değerler, hatalar
3. **Keşifsel Analiz** - İstatistikler, grafikler
4. **Modelleme** - Makine öğrenmesi
5. **Sonuç** - Raporlama, sunum

💡 **İpucu**: Kaggle'da gerçek veri setleriyle pratik yapın!
"""
    
    def _get_english_content(self, topic: str, level: str) -> str:
        """İngilizce ders içeriği."""
        return """
# 🇬🇧 İngilizce Öğrenme Rehberi

## Temel Kelimeler

### Selamlaşma
| İngilizce | Türkçe |
|-----------|--------|
| Hello | Merhaba |
| Good morning | Günaydın |
| Good evening | İyi akşamlar |
| Goodbye | Hoşça kal |
| Thank you | Teşekkür ederim |
| Please | Lütfen |

### Zamirler
| İngilizce | Türkçe |
|-----------|--------|
| I | Ben |
| You | Sen/Siz |
| He | O (erkek) |
| She | O (kadın) |
| It | O (nesne) |
| We | Biz |
| They | Onlar |

## Temel Cümleler

```
I am a student. - Ben bir öğrenciyim.
She is a teacher. - O bir öğretmen.
We are learning English. - İngilizce öğreniyoruz.
What is your name? - Adınız ne?
Where are you from? - Nerelisiniz?
```

## Fiil Çekimi (Present Simple)

```
I work - Ben çalışırım
You work - Sen çalışırsın
He/She works - O çalışır (s eklenir!)
We work - Biz çalışırız
They work - Onlar çalışır
```

## Günlük Pratik

1. **Dinleme**: İngilizce şarkı, podcast, film
2. **Konuşma**: Kendinizle İngilizce konuşun
3. **Okuma**: Basit hikayeler, haberler
4. **Yazma**: Günlük tutun

💡 **İpucu**: Her gün en az 10 yeni kelime öğrenin!
"""
    
    def _get_general_content(self, topic: str, level: str, goal: str) -> str:
        """Genel içerik."""
        return f"""
# 📚 {topic}

## Giriş

Bu derste **{goal if goal else topic}** konusunu öğreneceksiniz.

## Öğrenme Hedefleri

1. Temel kavramları anlama
2. Pratik uygulama yapabilme
3. Bilgilerinizi test etme

## İçerik

Bu konu hakkında sistematik bir şekilde ilerleyeceğiz:

### Adım 1: Temel Kavramlar
Önce konunun temellerini öğrenin. Terminolojiyi ve temel prensipleri anlayın.

### Adım 2: Örnekler
Gerçek dünya örnekleri üzerinden konuyu pekiştirin.

### Adım 3: Pratik
Öğrendiklerinizi uygulayın. Pratik yapmadan öğrenme eksik kalır.

### Adım 4: Test
Quiz çözerek bilgilerinizi test edin.

## Kaynaklar

- Online kurslar ve videolar
- Kitaplar ve makaleler
- Pratik platformları

## İpuçları

💡 Her gün düzenli çalışın
💡 Not alın ve tekrar edin
💡 Pratik yapmayı ihmal etmeyin
💡 Zorlandığınız konuları tekrarlayın

---

**Sonraki adım:** Quiz çözerek öğrendiklerinizi test edin!
"""
    
    def _get_minimal_fallback_quiz(self, topic: str, num_questions: int) -> List[Dict]:
        """
        Minimal fallback - sadece AI çalışmazsa.
        Kullanıcıya AI'yı yapılandırması gerektiğini gösterir.
        """
        return [
            {
                "question_id": f"fallback_{i+1}",
                "question": f"⚠️ AI servisi çalışmıyor. Lütfen GEMINI_API_KEY'i yapılandırın.",
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
    
    def _get_static_quiz_DEPRECATED(self, topic: str, level: str, num_questions: int) -> List[Dict]:
        """Konu bazlı hazır quiz soruları."""
        
        topic_lower = topic.lower()
        
        # AI Mühendisliği quizleri
        if any(x in topic_lower for x in ["ai", "yapay zeka", "makine öğren", "deep learning", "neural"]):
            questions = self._get_ai_quiz(topic_lower)
        # Python quizleri
        elif "python" in topic_lower:
            questions = self._get_python_quiz_by_topic(topic_lower)
        
        # Web quizleri
        elif any(x in topic_lower for x in ["web", "html", "css", "javascript", "js"]):
            questions = self._get_web_quiz_by_topic(topic_lower)
        
        # İngilizce quizleri
        elif any(x in topic_lower for x in ["ingilizce", "english"]):
            questions = [
                {
                    "question_id": "eng1",
                    "question": "'Thank you' ne demek?",
                    "options": ["Merhaba", "Teşekkürler", "Hoşça kal", "Lütfen"],
                    "correct_answer": "Teşekkürler",
                    "topic": "Temel Kelimeler"
                },
                {
                    "question_id": "eng2",
                    "question": "'She' zamiri kimi ifade eder?",
                    "options": ["O (erkek)", "O (kadın)", "Onlar", "Biz"],
                    "correct_answer": "O (kadın)",
                    "topic": "Zamirler"
                },
                {
                    "question_id": "eng3",
                    "question": "'I am a student' cümlesinin Türkçesi nedir?",
                    "options": ["Ben bir öğretmenim", "Ben bir öğrenciyim", "O bir öğrenci", "Biz öğrenciyiz"],
                    "correct_answer": "Ben bir öğrenciyim",
                    "topic": "Cümleler"
                },
                {
                    "question_id": "eng4",
                    "question": "He/She ile kullanılan fiillere ne eklenir?",
                    "options": ["-ed", "-ing", "-s", "-ly"],
                    "correct_answer": "-s",
                    "topic": "Gramer"
                },
                {
                    "question_id": "eng5",
                    "question": "'Good morning' ne zaman söylenir?",
                    "options": ["Akşam", "Sabah", "Gece", "Öğlen"],
                    "correct_answer": "Sabah",
                    "topic": "Selamlaşma"
                }
            ]
        
        # Genel quiz
        else:
            questions = [
                {
                    "question_id": f"q{i+1}",
                    "question": f"Bu konuyla ilgili soru {i+1}",
                    "options": ["Seçenek A", "Seçenek B", "Seçenek C", "Seçenek D"],
                    "correct_answer": "Seçenek A",
                    "topic": topic
                }
                for i in range(num_questions)
            ]
        
        return questions[:num_questions]
    
    def _get_web_quiz_by_topic(self, topic_lower: str) -> List[Dict]:
        """Web konusuna göre spesifik quiz soruları."""
        
        # HTML soruları
        if "html" in topic_lower and "css" not in topic_lower:
            return [
                {"question_id": "html1", "question": "HTML'de başlık etiketi hangisidir?", "options": ["<head>", "<h1>", "<title>", "<header>"], "correct_answer": "<h1>", "topic": "HTML"},
                {"question_id": "html2", "question": "HTML'de paragraf için hangi etiket kullanılır?", "options": ["<p>", "<paragraph>", "<text>", "<para>"], "correct_answer": "<p>", "topic": "HTML"},
                {"question_id": "html3", "question": "HTML'de link oluşturmak için hangi etiket kullanılır?", "options": ["<link>", "<a>", "<href>", "<url>"], "correct_answer": "<a>", "topic": "HTML"},
                {"question_id": "html4", "question": "HTML'de resim eklemek için hangi etiket kullanılır?", "options": ["<image>", "<img>", "<picture>", "<photo>"], "correct_answer": "<img>", "topic": "HTML"},
                {"question_id": "html5", "question": "HTML'de liste oluşturmak için hangi etiket kullanılır?", "options": ["<list>", "<ul> veya <ol>", "<li>", "<item>"], "correct_answer": "<ul> veya <ol>", "topic": "HTML"}
            ]
        
        # CSS soruları
        elif "css" in topic_lower and "flexbox" not in topic_lower and "grid" not in topic_lower:
            return [
                {"question_id": "css1", "question": "CSS'de metin rengini değiştirmek için hangi özellik kullanılır?", "options": ["text-color", "font-color", "color", "text-style"], "correct_answer": "color", "topic": "CSS"},
                {"question_id": "css2", "question": "CSS'de arka plan rengi için hangi özellik kullanılır?", "options": ["color", "background-color", "bg-color", "back-color"], "correct_answer": "background-color", "topic": "CSS"},
                {"question_id": "css3", "question": "CSS'de class seçici nasıl yazılır?", "options": ["#class", ".class", "*class", "@class"], "correct_answer": ".class", "topic": "CSS"},
                {"question_id": "css4", "question": "CSS'de ID seçici nasıl yazılır?", "options": ["#id", ".id", "*id", "@id"], "correct_answer": "#id", "topic": "CSS"},
                {"question_id": "css5", "question": "CSS'de yazı boyutunu değiştirmek için hangi özellik kullanılır?", "options": ["text-size", "font-size", "size", "text-height"], "correct_answer": "font-size", "topic": "CSS"}
            ]
        
        # CSS Flexbox soruları
        elif "flexbox" in topic_lower:
            return [
                {"question_id": "flex1", "question": "Flexbox'ı aktif etmek için hangi CSS özelliği kullanılır?", "options": ["display: flex", "flex: true", "flexbox: on", "layout: flex"], "correct_answer": "display: flex", "topic": "CSS Flexbox"},
                {"question_id": "flex2", "question": "Flexbox'ta öğeleri yatay hizalamak için hangi özellik kullanılır?", "options": ["align-items", "justify-content", "flex-align", "horizontal-align"], "correct_answer": "justify-content", "topic": "CSS Flexbox"},
                {"question_id": "flex3", "question": "Flexbox'ta öğeleri dikey hizalamak için hangi özellik kullanılır?", "options": ["align-items", "justify-content", "vertical-align", "flex-vertical"], "correct_answer": "align-items", "topic": "CSS Flexbox"},
                {"question_id": "flex4", "question": "flex-direction: column ne yapar?", "options": ["Öğeleri yatay sıralar", "Öğeleri dikey sıralar", "Öğeleri ters çevirir", "Hiçbir şey"], "correct_answer": "Öğeleri dikey sıralar", "topic": "CSS Flexbox"},
                {"question_id": "flex5", "question": "flex-wrap: wrap ne işe yarar?", "options": ["Öğeleri alt satıra taşır", "Öğeleri gizler", "Öğeleri büyütür", "Öğeleri döndürür"], "correct_answer": "Öğeleri alt satıra taşır", "topic": "CSS Flexbox"}
            ]
        
        # CSS Grid soruları
        elif "grid" in topic_lower:
            return [
                {"question_id": "grid1", "question": "CSS Grid'i aktif etmek için hangi özellik kullanılır?", "options": ["display: grid", "grid: true", "layout: grid", "grid-on: true"], "correct_answer": "display: grid", "topic": "CSS Grid"},
                {"question_id": "grid2", "question": "grid-template-columns ne işe yarar?", "options": ["Sütun sayısını ve boyutunu belirler", "Satır sayısını belirler", "Renk belirler", "Kenarlık ekler"], "correct_answer": "Sütun sayısını ve boyutunu belirler", "topic": "CSS Grid"},
                {"question_id": "grid3", "question": "grid-gap ne yapar?", "options": ["Öğeler arası boşluk ekler", "Kenarlık ekler", "Renk değiştirir", "Boyut ayarlar"], "correct_answer": "Öğeler arası boşluk ekler", "topic": "CSS Grid"},
                {"question_id": "grid4", "question": "grid-template-columns: repeat(3, 1fr) ne yapar?", "options": ["3 eşit sütun oluşturur", "3 satır oluşturur", "3px genişlik verir", "3 kez tekrarlar"], "correct_answer": "3 eşit sütun oluşturur", "topic": "CSS Grid"},
                {"question_id": "grid5", "question": "fr birimi ne anlama gelir?", "options": ["Fraction (kesir) - esnek birim", "Frame", "Fixed ratio", "Full row"], "correct_answer": "Fraction (kesir) - esnek birim", "topic": "CSS Grid"}
            ]
        
        # JavaScript soruları
        elif "javascript" in topic_lower or "js" in topic_lower:
            return [
                {"question_id": "js1", "question": "JavaScript'te değişken tanımlamak için hangisi kullanılır?", "options": ["var", "let", "const", "Hepsi"], "correct_answer": "Hepsi", "topic": "JavaScript"},
                {"question_id": "js2", "question": "console.log() ne işe yarar?", "options": ["Konsola yazdırır", "Dosya kaydeder", "Hesaplama yapar", "Sayfa yeniler"], "correct_answer": "Konsola yazdırır", "topic": "JavaScript"},
                {"question_id": "js3", "question": "document.getElementById() ne yapar?", "options": ["ID'ye göre element seçer", "Class'a göre seçer", "Tag'e göre seçer", "Hepsini seçer"], "correct_answer": "ID'ye göre element seçer", "topic": "JavaScript DOM"},
                {"question_id": "js4", "question": "addEventListener() ne işe yarar?", "options": ["Olay dinleyici ekler", "Element ekler", "Stil ekler", "Sayfa yükler"], "correct_answer": "Olay dinleyici ekler", "topic": "JavaScript Events"},
                {"question_id": "js5", "question": "== ve === arasındaki fark nedir?", "options": ["=== tip kontrolü de yapar", "Fark yok", "== daha hızlı", "=== daha yavaş"], "correct_answer": "=== tip kontrolü de yapar", "topic": "JavaScript"}
            ]
        
        # Responsive tasarım
        elif "responsive" in topic_lower or "tasarım" in topic_lower:
            return [
                {"question_id": "resp1", "question": "Responsive tasarım için hangi CSS özelliği kullanılır?", "options": ["@media", "@responsive", "@screen", "@device"], "correct_answer": "@media", "topic": "Responsive"},
                {"question_id": "resp2", "question": "Mobile-first yaklaşım ne demektir?", "options": ["Önce mobil için tasarla", "Önce desktop için tasarla", "Sadece mobil", "Sadece tablet"], "correct_answer": "Önce mobil için tasarla", "topic": "Responsive"},
                {"question_id": "resp3", "question": "Viewport meta tag ne işe yarar?", "options": ["Mobil görünümü optimize eder", "Renk ayarlar", "Font yükler", "Resim sıkıştırır"], "correct_answer": "Mobil görünümü optimize eder", "topic": "Responsive"}
            ]
        
        # Genel web soruları
        else:
            return [
                {"question_id": "web1", "question": "HTML ne demektir?", "options": ["HyperText Markup Language", "High Tech Modern Language", "Home Tool Markup Language", "Hyperlinks and Text Markup Language"], "correct_answer": "HyperText Markup Language", "topic": "Web Temelleri"},
                {"question_id": "web2", "question": "CSS ne işe yarar?", "options": ["Sayfayı stillendirir", "Programlama yapar", "Veritabanı yönetir", "Sunucu kurar"], "correct_answer": "Sayfayı stillendirir", "topic": "Web Temelleri"},
                {"question_id": "web3", "question": "JavaScript hangi amaçla kullanılır?", "options": ["Sayfa etkileşimi ve dinamiklik", "Sadece stil", "Sadece yapı", "Sadece veritabanı"], "correct_answer": "Sayfa etkileşimi ve dinamiklik", "topic": "Web Temelleri"},
                {"question_id": "web4", "question": "Frontend nedir?", "options": ["Kullanıcının gördüğü kısım", "Sunucu tarafı", "Veritabanı", "API"], "correct_answer": "Kullanıcının gördüğü kısım", "topic": "Web Temelleri"},
                {"question_id": "web5", "question": "Backend nedir?", "options": ["Sunucu tarafı mantık", "Kullanıcı arayüzü", "Tasarım", "Grafik"], "correct_answer": "Sunucu tarafı mantık", "topic": "Web Temelleri"}
            ]
    
    def _get_python_quiz_by_topic(self, topic_lower: str) -> List[Dict]:
        """Python konusuna göre spesifik quiz soruları."""
        
        # Değişkenler ve Veri Tipleri
        if any(x in topic_lower for x in ["değişken", "veri tip", "veri tipi"]):
            return [
                {"question_id": "py1", "question": "'Merhaba' ifadesinin veri tipi nedir?", "options": ["int", "float", "str", "bool"], "correct_answer": "str", "topic": "Veri Tipleri"},
                {"question_id": "py2", "question": "Hangisi geçerli bir değişken ismi DEĞİLDİR?", "options": ["_isim", "isim1", "1isim", "isim_soyisim"], "correct_answer": "1isim", "topic": "Değişkenler"},
                {"question_id": "py3", "question": "type(42) sonucu nedir?", "options": ["<class 'str'>", "<class 'int'>", "<class 'float'>", "<class 'bool'>"], "correct_answer": "<class 'int'>", "topic": "Veri Tipleri"},
                {"question_id": "py4", "question": "int('10') ne yapar?", "options": ["Hata verir", "String'i sayıya çevirir", "10 yazar", "Hiçbir şey"], "correct_answer": "String'i sayıya çevirir", "topic": "Tip Dönüşümü"},
                {"question_id": "py5", "question": "x = 5; x = 'beş' ifadesi geçerli midir?", "options": ["Evet, Python dinamik tipli", "Hayır, hata verir", "Sadece Python 2'de", "Sadece Python 3'te"], "correct_answer": "Evet, Python dinamik tipli", "topic": "Değişkenler"}
            ]
        
        # Döngüler
        elif "döngü" in topic_lower or "loop" in topic_lower or "for" in topic_lower or "while" in topic_lower:
            return [
                {"question_id": "py1", "question": "range(5) kaç eleman üretir?", "options": ["4", "5", "6", "1"], "correct_answer": "5", "topic": "range()"},
                {"question_id": "py2", "question": "for i in range(3): print(i) çıktısı nedir?", "options": ["1 2 3", "0 1 2", "0 1 2 3", "1 2"], "correct_answer": "0 1 2", "topic": "for Döngüsü"},
                {"question_id": "py3", "question": "break komutu ne yapar?", "options": ["Döngüyü sonlandırır", "Bir sonraki iterasyona geçer", "Programı durdurur", "Hata verir"], "correct_answer": "Döngüyü sonlandırır", "topic": "break"},
                {"question_id": "py4", "question": "continue komutu ne yapar?", "options": ["Döngüyü sonlandırır", "Sonraki iterasyona geçer", "Programı durdurur", "Döngüyü başa sarar"], "correct_answer": "Sonraki iterasyona geçer", "topic": "continue"},
                {"question_id": "py5", "question": "while True: ne yapar?", "options": ["Sonsuz döngü", "Bir kez çalışır", "Hata verir", "Hiçbir şey"], "correct_answer": "Sonsuz döngü", "topic": "while Döngüsü"}
            ]
        
        # Fonksiyonlar
        elif "fonksiyon" in topic_lower or "function" in topic_lower or "def" in topic_lower:
            return [
                {"question_id": "py1", "question": "Fonksiyon tanımlamak için hangi anahtar kelime kullanılır?", "options": ["func", "def", "function", "define"], "correct_answer": "def", "topic": "Fonksiyonlar"},
                {"question_id": "py2", "question": "def topla(a, b): return a+b ifadesinde topla(3, 5) sonucu nedir?", "options": ["35", "8", "Hata", "None"], "correct_answer": "8", "topic": "Fonksiyonlar"},
                {"question_id": "py3", "question": "return komutu ne yapar?", "options": ["Değer döndürür ve fonksiyonu bitirir", "Sadece yazdırır", "Döngüyü bitirir", "Hata verir"], "correct_answer": "Değer döndürür ve fonksiyonu bitirir", "topic": "return"},
                {"question_id": "py4", "question": "def selamla(isim='Dünya'): print(f'Merhaba {isim}') - selamla() çıktısı nedir?", "options": ["Merhaba Dünya", "Merhaba", "Hata", "None"], "correct_answer": "Merhaba Dünya", "topic": "Varsayılan Parametre"},
                {"question_id": "py5", "question": "lambda x: x*2 ne yapar?", "options": ["Anonim fonksiyon oluşturur", "x'i 2 ile çarpar", "Hata verir", "Liste oluşturur"], "correct_answer": "Anonim fonksiyon oluşturur", "topic": "Lambda"}
            ]
        
        # Listeler
        elif "liste" in topic_lower or "list" in topic_lower:
            return [
                {"question_id": "py1", "question": "Liste oluşturmak için hangi parantez kullanılır?", "options": ["()", "[]", "{}", "<>"], "correct_answer": "[]", "topic": "Listeler"},
                {"question_id": "py2", "question": "liste = [1,2,3]; liste.append(4) sonucu liste nedir?", "options": ["[1,2,3]", "[1,2,3,4]", "[4,1,2,3]", "Hata"], "correct_answer": "[1,2,3,4]", "topic": "append()"},
                {"question_id": "py3", "question": "len([1,2,3,4,5]) sonucu nedir?", "options": ["4", "5", "15", "Hata"], "correct_answer": "5", "topic": "len()"},
                {"question_id": "py4", "question": "liste[0] ne yapar?", "options": ["İlk elemanı getirir", "Son elemanı getirir", "Hata verir", "Tüm listeyi getirir"], "correct_answer": "İlk elemanı getirir", "topic": "İndeksleme"},
                {"question_id": "py5", "question": "[1,2,3] + [4,5] sonucu nedir?", "options": ["[1,2,3,4,5]", "[5,7]", "Hata", "[1,2,3,[4,5]]"], "correct_answer": "[1,2,3,4,5]", "topic": "Liste Birleştirme"}
            ]
        
        # String işlemleri
        elif "string" in topic_lower or "metin" in topic_lower:
            return [
                {"question_id": "py1", "question": "Python'da string birleştirmek için hangi operatör kullanılır?", "options": ["+", "*", "&", "||"], "correct_answer": "+", "topic": "String"},
                {"question_id": "py2", "question": "'Merhaba'.upper() sonucu nedir?", "options": ["merhaba", "MERHABA", "Merhaba", "MeRhAbA"], "correct_answer": "MERHABA", "topic": "String Metodları"},
                {"question_id": "py3", "question": "len('Python') sonucu nedir?", "options": ["5", "6", "7", "Hata"], "correct_answer": "6", "topic": "String"},
                {"question_id": "py4", "question": "'Python'[0] sonucu nedir?", "options": ["P", "y", "Python", "Hata"], "correct_answer": "P", "topic": "String İndeksleme"},
                {"question_id": "py5", "question": "'Merhaba Dünya'.split() sonucu nedir?", "options": ["['Merhaba', 'Dünya']", "['Merhaba Dünya']", "Hata", "None"], "correct_answer": "['Merhaba', 'Dünya']", "topic": "String Metodları"}
            ]
        
        # Operatörler ve sayılar
        elif any(x in topic_lower for x in ["operatör", "sayı", "number", "matematik"]):
            return [
                {"question_id": "py1", "question": "10 // 3 işleminin sonucu nedir?", "options": ["3.33", "3", "1", "30"], "correct_answer": "3", "topic": "Operatörler"},
                {"question_id": "py2", "question": "10 % 3 işleminin sonucu nedir?", "options": ["3", "1", "0", "10"], "correct_answer": "1", "topic": "Mod Operatörü"},
                {"question_id": "py3", "question": "2 ** 3 işleminin sonucu nedir?", "options": ["6", "8", "9", "5"], "correct_answer": "8", "topic": "Üs Alma"},
                {"question_id": "py4", "question": "5 / 2 sonucu hangi tipte döner?", "options": ["int", "float", "str", "bool"], "correct_answer": "float", "topic": "Bölme"},
                {"question_id": "py5", "question": "abs(-5) sonucu nedir?", "options": ["-5", "5", "0", "Hata"], "correct_answer": "5", "topic": "Matematiksel Fonksiyonlar"}
            ]
        
        # Input ve kullanıcı girdisi
        elif "input" in topic_lower or "girdi" in topic_lower or "kullanıcı" in topic_lower:
            return [
                {"question_id": "py1", "question": "input() fonksiyonu ne yapar?", "options": ["Kullanıcıdan girdi alır", "Ekrana yazar", "Dosya okur", "Hesaplama yapar"], "correct_answer": "Kullanıcıdan girdi alır", "topic": "input()"},
                {"question_id": "py2", "question": "input() fonksiyonu hangi tipte veri döndürür?", "options": ["str", "int", "float", "bool"], "correct_answer": "str", "topic": "input()"},
                {"question_id": "py3", "question": "Kullanıcıdan sayı almak için ne yapmalıyız?", "options": ["int(input())", "input(int)", "number(input())", "input.int()"], "correct_answer": "int(input())", "topic": "Tip Dönüşümü"},
                {"question_id": "py4", "question": "input('Adınız: ') ne yapar?", "options": ["Mesaj gösterir ve girdi alır", "Sadece yazdırır", "Hata verir", "Dosya açar"], "correct_answer": "Mesaj gösterir ve girdi alır", "topic": "input()"},
                {"question_id": "py5", "question": "x = input(); y = input() sonrası x + y ne yapar?", "options": ["String birleştirme", "Sayısal toplama", "Hata", "Çıkarma"], "correct_answer": "String birleştirme", "topic": "input()"}
            ]
        
        # Koşullar
        elif "koşul" in topic_lower or "if" in topic_lower or "else" in topic_lower:
            return [
                {"question_id": "py1", "question": "if x > 5: print('büyük') - x=10 için çıktı nedir?", "options": ["büyük", "küçük", "Hata", "Hiçbir şey"], "correct_answer": "büyük", "topic": "if"},
                {"question_id": "py2", "question": "elif ne demektir?", "options": ["else if", "end if", "exit if", "error if"], "correct_answer": "else if", "topic": "elif"},
                {"question_id": "py3", "question": "5 > 3 and 2 < 1 sonucu nedir?", "options": ["True", "False", "Hata", "None"], "correct_answer": "False", "topic": "Mantıksal Operatörler"},
                {"question_id": "py4", "question": "not True sonucu nedir?", "options": ["True", "False", "None", "Hata"], "correct_answer": "False", "topic": "not Operatörü"},
                {"question_id": "py5", "question": "5 == 5 sonucu nedir?", "options": ["True", "False", "5", "Hata"], "correct_answer": "True", "topic": "Karşılaştırma"}
            ]
        
        # Genel Python soruları
        else:
            return [
                {"question_id": "py1", "question": "Python'da ekrana yazı yazdırmak için hangi fonksiyon kullanılır?", "options": ["echo()", "print()", "write()", "display()"], "correct_answer": "print()", "topic": "Python Temelleri"},
                {"question_id": "py2", "question": "Python'da yorum satırı nasıl başlar?", "options": ["//", "#", "/*", "--"], "correct_answer": "#", "topic": "Python Temelleri"},
                {"question_id": "py3", "question": "10 // 3 işleminin sonucu nedir?", "options": ["3.33", "3", "1", "30"], "correct_answer": "3", "topic": "Operatörler"},
                {"question_id": "py4", "question": "Python'da girintiler (indentation) neden önemlidir?", "options": ["Kod bloklarını belirler", "Sadece görsel", "Zorunlu değil", "Hata verir"], "correct_answer": "Kod bloklarını belirler", "topic": "Python Sözdizimi"},
                {"question_id": "py5", "question": "input() fonksiyonu ne yapar?", "options": ["Kullanıcıdan girdi alır", "Ekrana yazar", "Dosya okur", "Hesaplama yapar"], "correct_answer": "Kullanıcıdan girdi alır", "topic": "input()"}
            ]
    
    def _get_ai_quiz(self, topic_lower: str) -> List[Dict]:
        """AI/ML konuları için quiz soruları."""
        
        # Genel AI soruları
        if "giriş" in topic_lower or "temel kavram" in topic_lower:
            return [
                {
                    "question_id": "ai1",
                    "question": "Yapay Zeka (AI) nedir?",
                    "options": [
                        "Sadece robotlar",
                        "Makinelerin insan gibi düşünmesi ve öğrenmesi",
                        "Sadece oyun yapımı",
                        "Sadece hesap makineleri"
                    ],
                    "correct_answer": "Makinelerin insan gibi düşünmesi ve öğrenmesi",
                    "topic": "AI Temelleri"
                },
                {
                    "question_id": "ai2",
                    "question": "Makine Öğrenmesi (Machine Learning) ne demektir?",
                    "options": [
                        "Makinelerin kendiliğinden öğrenmesi",
                        "Sadece programlama",
                        "Robot üretimi",
                        "Oyun geliştirme"
                    ],
                    "correct_answer": "Makinelerin kendiliğinden öğrenmesi",
                    "topic": "Machine Learning"
                },
                {
                    "question_id": "ai3",
                    "question": "Supervised Learning nedir?",
                    "options": [
                        "Etiketli verilerle öğrenme",
                        "Etiketsiz verilerle öğrenme",
                        "Oyunla öğrenme",
                        "İnternetten öğrenme"
                    ],
                    "correct_answer": "Etiketli verilerle öğrenme",
                    "topic": "ML Türleri"
                },
                {
                    "question_id": "ai4",
                    "question": "AI'da 'model' ne anlama gelir?",
                    "options": [
                        "Manken",
                        "Eğitilmiş algoritma",
                        "Veri tabanı",
                        "Programlama dili"
                    ],
                    "correct_answer": "Eğitilmiş algoritma",
                    "topic": "AI Kavramları"
                },
                {
                    "question_id": "ai5",
                    "question": "Deep Learning hangi yapıyı kullanır?",
                    "options": [
                        "Ağaçlar",
                        "Neural Networks (Sinir Ağları)",
                        "Tablolar",
                        "Grafikler"
                    ],
                    "correct_answer": "Neural Networks (Sinir Ağları)",
                    "topic": "Deep Learning"
                }
            ]
        
        # NumPy ve veri işleme soruları
        elif any(x in topic_lower for x in ["numpy", "veri işleme", "veri işlem", "veri görsel", "görselleştirme"]):
            return [
                {
                    "question_id": "np1",
                    "question": "NumPy ne için kullanılır?",
                    "options": ["Sayısal hesaplama", "Web geliştirme", "Oyun yapımı", "Grafik tasarım"],
                    "correct_answer": "Sayısal hesaplama",
                    "topic": "NumPy"
                },
                {
                    "question_id": "np2",
                    "question": "NumPy dizisi oluşturmak için hangi fonksiyon kullanılır?",
                    "options": ["np.array()", "np.list()", "np.create()", "np.make()"],
                    "correct_answer": "np.array()",
                    "topic": "NumPy"
                },
                {
                    "question_id": "np3",
                    "question": "np.mean() ne yapar?",
                    "options": ["Ortalama hesaplar", "Toplam hesaplar", "Maksimum bulur", "Sıralar"],
                    "correct_answer": "Ortalama hesaplar",
                    "topic": "NumPy"
                }
            ]
        
        # Pandas soruları
        elif "pandas" in topic_lower:
            return [
                {
                    "question_id": "pd1",
                    "question": "Pandas'ta DataFrame nedir?",
                    "options": ["2 boyutlu tablo", "Grafik", "Dosya", "Fonksiyon"],
                    "correct_answer": "2 boyutlu tablo",
                    "topic": "Pandas"
                },
                {
                    "question_id": "pd2",
                    "question": "df.head() ne yapar?",
                    "options": ["İlk 5 satırı gösterir", "Son 5 satır", "Tüm veri", "Sütun isimleri"],
                    "correct_answer": "İlk 5 satırı gösterir",
                    "topic": "Pandas"
                },
                {
                    "question_id": "pd3",
                    "question": "CSV dosyası okumak için hangi fonksiyon kullanılır?",
                    "options": ["pd.read_csv()", "pd.open()", "pd.load()", "pd.import()"],
                    "correct_answer": "pd.read_csv()",
                    "topic": "Pandas"
                }
            ]
        
        # Neural Networks soruları
        elif "neural" in topic_lower or "sinir ağ" in topic_lower:
            return [
                {
                    "question_id": "nn1",
                    "question": "Neural Network'ün temel birimi nedir?",
                    "options": ["Neuron (Nöron)", "Hücre", "Blok", "Parça"],
                    "correct_answer": "Neuron (Nöron)",
                    "topic": "Neural Networks"
                },
                {
                    "question_id": "nn2",
                    "question": "Activation function ne işe yarar?",
                    "options": ["Doğrusal olmayan ilişkiler öğrenmek", "Veri kaydetmek", "Grafik çizmek", "Dosya okumak"],
                    "correct_answer": "Doğrusal olmayan ilişkiler öğrenmek",
                    "topic": "Neural Networks"
                },
                {
                    "question_id": "nn3",
                    "question": "Backpropagation nedir?",
                    "options": ["Hataları geriye yayma ve ağırlık güncelleme", "İleri besleme", "Veri temizleme", "Model kaydetme"],
                    "correct_answer": "Hataları geriye yayma ve ağırlık güncelleme",
                    "topic": "Neural Networks"
                }
            ]
        
        # Genel AI soruları
        else:
            return [
                {
                    "question_id": "gen1",
                    "question": "AI'da 'training' ne demektir?",
                    "options": ["Modeli eğitme", "Veri toplama", "Kod yazma", "Test etme"],
                    "correct_answer": "Modeli eğitme",
                    "topic": "AI Genel"
                },
                {
                    "question_id": "gen2",
                    "question": "Overfitting nedir?",
                    "options": ["Modelin eğitim verisini ezberlemesi", "Çok hızlı öğrenme", "Veri eksikliği", "Hata yapma"],
                    "correct_answer": "Modelin eğitim verisini ezberlemesi",
                    "topic": "AI Genel"
                },
                {
                    "question_id": "gen3",
                    "question": "Test verisi neden kullanılır?",
                    "options": ["Model performansını değerlendirmek", "Model eğitmek", "Veri temizlemek", "Grafik çizmek"],
                    "correct_answer": "Model performansını değerlendirmek",
                    "topic": "AI Genel"
                }
            ]


# Singleton
_content_agent = None

def get_content_agent() -> ContentAgent:
    global _content_agent
    if _content_agent is None:
        _content_agent = ContentAgent()
    return _content_agent

