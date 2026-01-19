"""
Öğrenme Programları - Spesifik müfredatlar
==========================================

Her program:
- Haftalık temalar
- Günlük dersler
- Quiz soruları
- Pratik egzersizler
içerir.
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class Lesson:
    """Ders yapısı."""
    lesson_id: str
    title: str
    description: str
    duration_min: int
    lesson_type: str  # theory, practice, quiz, project
    content: str
    resources: List[Dict]
    quiz_questions: List[Dict] = None


@dataclass
class DayPlan:
    """Günlük plan yapısı."""
    day: int
    theme: str
    lessons: List[Lesson]
    objectives: List[str]
    tip: str


@dataclass
class WeekPlan:
    """Haftalık plan yapısı."""
    week: int
    title: str
    description: str
    days: List[DayPlan]
    project: Dict  # Hafta sonu projesi


@dataclass
class LearningProgram:
    """Öğrenme programı yapısı."""
    program_id: str
    title: str
    description: str
    duration_weeks: int
    difficulty: str
    prerequisites: List[str]
    skills_gained: List[str]
    weeks: List[WeekPlan]
    icon: str


# =============================================================================
# PYTHON TEMELLER PROGRAMI (4 Hafta)
# =============================================================================

PYTHON_BASICS_PROGRAM = {
    "program_id": "python_basics",
    "title": "🐍 Python Temelleri",
    "description": "Sıfırdan Python programlamayı öğrenin. Değişkenler, veri tipleri, kontrol yapıları, fonksiyonlar ve daha fazlası.",
    "duration_weeks": 4,
    "difficulty": "Başlangıç",
    "prerequisites": [],
    "skills_gained": [
        "Python syntax ve temel kavramlar",
        "Değişkenler ve veri tipleri",
        "Koşullu ifadeler ve döngüler",
        "Fonksiyon yazma",
        "Liste, dictionary kullanımı",
        "Dosya işlemleri",
        "Hata yönetimi"
    ],
    "icon": "🐍",
    "curriculum": {
        # HAFTA 1: Python'a Giriş
        1: {
            "title": "Python'a Giriş ve Temel Kavramlar",
            "description": "Python kurulumu, ilk program, değişkenler ve veri tipleri",
            "days": {
                1: {
                    "theme": "Python Kurulumu ve İlk Program",
                    "lessons": [
                        {
                            "id": "w1d1_l1",
                            "title": "Python Nedir?",
                            "type": "theory",
                            "duration": 15,
                            "content": """
# Python Nedir?

Python, 1991'de Guido van Rossum tarafından geliştirilen, okunması kolay ve güçlü bir programlama dilidir.

## Neden Python?
- ✅ Öğrenmesi kolay syntax
- ✅ Geniş kütüphane desteği
- ✅ Web, veri bilimi, AI, otomasyon için kullanılır
- ✅ Büyük topluluk desteği

## Kullanım Alanları
1. Web Geliştirme (Django, Flask)
2. Veri Bilimi (Pandas, NumPy)
3. Yapay Zeka (TensorFlow, PyTorch)
4. Otomasyon ve Scripting
5. Oyun Geliştirme
                            """,
                            "resources": [
                                {"title": "Python Resmi Sitesi", "url": "https://python.org"},
                                {"title": "Python Kurulum Rehberi", "url": "https://realpython.com/installing-python/"}
                            ]
                        },
                        {
                            "id": "w1d1_l2",
                            "title": "İlk Python Programı",
                            "type": "practice",
                            "duration": 20,
                            "content": """
# İlk Python Programı

## Merhaba Dünya!

```python
print("Merhaba Dünya!")
print("Python öğreniyorum!")
```

## Çalıştırma
1. Python dosyası oluşturun: `merhaba.py`
2. Kodu yazın
3. Terminal'de çalıştırın: `python merhaba.py`

## Alıştırma
Aşağıdaki çıktıyı veren programı yazın:
```
*****
Adım: [Sizin adınız]
Python öğreniyorum!
*****
```
                            """,
                            "resources": []
                        }
                    ],
                    "quiz": [
                        {
                            "id": "w1d1_q1",
                            "question": "Python hangi yılda geliştirildi?",
                            "options": ["1989", "1991", "1995", "2000"],
                            "correct": "1991"
                        },
                        {
                            "id": "w1d1_q2",
                            "question": "Ekrana yazı yazdırmak için hangi fonksiyon kullanılır?",
                            "options": ["echo()", "print()", "write()", "display()"],
                            "correct": "print()"
                        },
                        {
                            "id": "w1d1_q3",
                            "question": "Python dosyalarının uzantısı nedir?",
                            "options": [".python", ".pt", ".py", ".pyt"],
                            "correct": ".py"
                        }
                    ],
                    "objectives": [
                        "Python'un ne olduğunu anlama",
                        "İlk Python programını yazma",
                        "print() fonksiyonunu kullanma"
                    ],
                    "tip": "💡 Kod yazarken hata yapmaktan korkmayın! Hatalar öğrenmenin en iyi yoludur."
                },
                2: {
                    "theme": "Değişkenler ve Veri Tipleri",
                    "lessons": [
                        {
                            "id": "w1d2_l1",
                            "title": "Değişkenler",
                            "type": "theory",
                            "duration": 20,
                            "content": """
# Değişkenler

Değişkenler, verileri saklamak için kullanılan isimlendirilmiş alanlardır.

## Değişken Tanımlama

```python
# Metin (string)
isim = "Ahmet"
soyisim = 'Yılmaz'

# Sayı (integer)
yas = 25

# Ondalıklı sayı (float)
boy = 1.75

# Mantıksal (boolean)
ogrenci_mi = True
```

## Değişken İsimlendirme Kuralları
- ✅ Harf veya _ ile başlamalı
- ✅ Harf, rakam ve _ içerebilir
- ❌ Rakamla başlayamaz
- ❌ Boşluk içeremez
- ❌ Python anahtar kelimeleri kullanılamaz (if, for, while vb.)

## Örnekler
```python
kullanici_adi = "john123"  # ✅ Doğru
_ozel = "gizli"            # ✅ Doğru
2sayi = 10                 # ❌ Yanlış (rakamla başlıyor)
kullanıcı adı = "test"     # ❌ Yanlış (boşluk var)
```
                            """,
                            "resources": [
                                {"title": "Python Değişkenler", "url": "https://www.w3schools.com/python/python_variables.asp"}
                            ]
                        },
                        {
                            "id": "w1d2_l2",
                            "title": "Veri Tipleri",
                            "type": "theory",
                            "duration": 20,
                            "content": """
# Temel Veri Tipleri

## 1. String (str) - Metin
```python
mesaj = "Merhaba"
print(type(mesaj))  # <class 'str'>
```

## 2. Integer (int) - Tam Sayı
```python
sayi = 42
print(type(sayi))  # <class 'int'>
```

## 3. Float - Ondalıklı Sayı
```python
pi = 3.14159
print(type(pi))  # <class 'float'>
```

## 4. Boolean (bool) - Mantıksal
```python
dogru = True
yanlis = False
print(type(dogru))  # <class 'bool'>
```

## Tip Dönüşümü
```python
# String'den int'e
sayi_str = "123"
sayi_int = int(sayi_str)  # 123

# Int'den string'e
yas = 25
yas_str = str(yas)  # "25"

# Int'den float'a
tam = 10
ondalik = float(tam)  # 10.0
```
                            """,
                            "resources": []
                        },
                        {
                            "id": "w1d2_l3",
                            "title": "Değişken Alıştırmaları",
                            "type": "practice",
                            "duration": 20,
                            "content": """
# Alıştırmalar

## Alıştırma 1: Kişisel Bilgiler
Aşağıdaki değişkenleri tanımlayın ve ekrana yazdırın:
- isim (string)
- yas (int)
- boy (float)
- ogrenci_mi (bool)

```python
# Çözüm
isim = "Ali"
yas = 22
boy = 1.80
ogrenci_mi = True

print("İsim:", isim)
print("Yaş:", yas)
print("Boy:", boy)
print("Öğrenci mi:", ogrenci_mi)
```

## Alıştırma 2: Tip Dönüşümü
```python
# Kullanıcıdan yaş al ve 5 yıl sonrasını hesapla
yas_str = "25"
yas = int(yas_str)
bes_yil_sonra = yas + 5
print("5 yıl sonra yaşınız:", bes_yil_sonra)
```
                            """,
                            "resources": []
                        }
                    ],
                    "quiz": [
                        {
                            "id": "w1d2_q1",
                            "question": "Hangisi geçerli bir değişken ismi DEĞİLDİR?",
                            "options": ["kullanici_adi", "_ozel", "2sayi", "isim123"],
                            "correct": "2sayi"
                        },
                        {
                            "id": "w1d2_q2",
                            "question": "'Merhaba' ifadesinin veri tipi nedir?",
                            "options": ["int", "float", "str", "bool"],
                            "correct": "str"
                        },
                        {
                            "id": "w1d2_q3",
                            "question": "int('42') ifadesinin sonucu nedir?",
                            "options": ["'42'", "42", "42.0", "Hata verir"],
                            "correct": "42"
                        }
                    ],
                    "objectives": [
                        "Değişken tanımlama kurallarını öğrenme",
                        "Temel veri tiplerini anlama",
                        "Tip dönüşümü yapabilme"
                    ],
                    "tip": "💡 type() fonksiyonu ile her değişkenin tipini kontrol edebilirsiniz."
                },
                3: {
                    "theme": "String İşlemleri",
                    "lessons": [
                        {
                            "id": "w1d3_l1",
                            "title": "String Metodları",
                            "type": "theory",
                            "duration": 25,
                            "content": """
# String İşlemleri

## String Birleştirme
```python
ad = "Ali"
soyad = "Veli"
tam_isim = ad + " " + soyad  # "Ali Veli"

# f-string (önerilen)
mesaj = f"Merhaba {ad} {soyad}!"
```

## Yaygın String Metodları
```python
metin = "  Merhaba Dünya  "

metin.upper()      # "  MERHABA DÜNYA  "
metin.lower()      # "  merhaba dünya  "
metin.strip()      # "Merhaba Dünya"
metin.replace("Dünya", "Python")  # "  Merhaba Python  "
metin.split()      # ["Merhaba", "Dünya"]
len(metin)         # 17
```

## String İndeksleme
```python
kelime = "Python"
print(kelime[0])   # P
print(kelime[-1])  # n
print(kelime[0:3]) # Pyt
print(kelime[2:])  # thon
```
                            """,
                            "resources": []
                        }
                    ],
                    "quiz": [
                        {
                            "id": "w1d3_q1",
                            "question": "'python'.upper() sonucu nedir?",
                            "options": ["python", "PYTHON", "Python", "Hata"],
                            "correct": "PYTHON"
                        },
                        {
                            "id": "w1d3_q2",
                            "question": "'Merhaba'[0] sonucu nedir?",
                            "options": ["M", "e", "Merhaba", "a"],
                            "correct": "M"
                        }
                    ],
                    "objectives": [
                        "String birleştirme yöntemlerini öğrenme",
                        "String metodlarını kullanma",
                        "String indeksleme yapabilme"
                    ],
                    "tip": "💡 f-string en modern ve okunabilir string formatlama yöntemidir."
                },
                4: {
                    "theme": "Sayısal İşlemler ve Operatörler",
                    "lessons": [
                        {
                            "id": "w1d4_l1",
                            "title": "Aritmetik Operatörler",
                            "type": "theory",
                            "duration": 20,
                            "content": """
# Aritmetik Operatörler

```python
a = 10
b = 3

print(a + b)   # 13  (Toplama)
print(a - b)   # 7   (Çıkarma)
print(a * b)   # 30  (Çarpma)
print(a / b)   # 3.33 (Bölme)
print(a // b)  # 3   (Tam bölme)
print(a % b)   # 1   (Mod - kalan)
print(a ** b)  # 1000 (Üs alma)
```

## Karşılaştırma Operatörleri
```python
x = 5
y = 10

print(x == y)  # False (Eşit mi?)
print(x != y)  # True  (Eşit değil mi?)
print(x < y)   # True  (Küçük mü?)
print(x > y)   # False (Büyük mü?)
print(x <= y)  # True  (Küçük eşit mi?)
print(x >= y)  # False (Büyük eşit mi?)
```
                            """,
                            "resources": []
                        }
                    ],
                    "quiz": [
                        {
                            "id": "w1d4_q1",
                            "question": "10 // 3 sonucu nedir?",
                            "options": ["3.33", "3", "1", "30"],
                            "correct": "3"
                        },
                        {
                            "id": "w1d4_q2",
                            "question": "10 % 3 sonucu nedir?",
                            "options": ["3", "3.33", "1", "0"],
                            "correct": "1"
                        }
                    ],
                    "objectives": [
                        "Aritmetik operatörleri kullanma",
                        "Karşılaştırma operatörlerini anlama"
                    ],
                    "tip": "💡 // tam bölme, % ise kalanı verir."
                },
                5: {
                    "theme": "Kullanıcı Girdisi (input)",
                    "lessons": [
                        {
                            "id": "w1d5_l1",
                            "title": "input() Fonksiyonu",
                            "type": "theory",
                            "duration": 15,
                            "content": """
# Kullanıcıdan Veri Alma

## input() Fonksiyonu
```python
isim = input("Adınızı girin: ")
print(f"Merhaba {isim}!")
```

## Sayı Alma (Tip Dönüşümü Gerekli!)
```python
yas_str = input("Yaşınızı girin: ")
yas = int(yas_str)

# veya tek satırda
yas = int(input("Yaşınızı girin: "))
```

## Örnek Program: Basit Hesap Makinesi
```python
sayi1 = float(input("İlk sayı: "))
sayi2 = float(input("İkinci sayı: "))

toplam = sayi1 + sayi2
print(f"Toplam: {toplam}")
```
                            """,
                            "resources": []
                        }
                    ],
                    "quiz": [
                        {
                            "id": "w1d5_q1",
                            "question": "input() fonksiyonu varsayılan olarak hangi tipte veri döndürür?",
                            "options": ["int", "float", "str", "bool"],
                            "correct": "str"
                        }
                    ],
                    "objectives": [
                        "input() fonksiyonunu kullanma",
                        "Kullanıcı girdisini işleme"
                    ],
                    "tip": "💡 input() her zaman string döndürür, sayı için int() veya float() kullanın."
                },
                6: {
                    "theme": "Hafta 1 Tekrar ve Mini Proje",
                    "lessons": [
                        {
                            "id": "w1d6_l1",
                            "title": "Hafta 1 Özet",
                            "type": "theory",
                            "duration": 15,
                            "content": """
# Hafta 1 Özet

## Öğrendiklerimiz
1. ✅ Python nedir ve neden kullanılır
2. ✅ print() ile ekrana yazdırma
3. ✅ Değişkenler ve isimlendirme kuralları
4. ✅ Veri tipleri: str, int, float, bool
5. ✅ String işlemleri ve metodları
6. ✅ Aritmetik ve karşılaştırma operatörleri
7. ✅ input() ile kullanıcıdan veri alma

## Önemli Fonksiyonlar
- print() - Ekrana yazdırma
- input() - Kullanıcıdan veri alma
- type() - Veri tipini öğrenme
- int(), float(), str() - Tip dönüşümü
- len() - Uzunluk
                            """,
                            "resources": []
                        },
                        {
                            "id": "w1d6_l2",
                            "title": "Mini Proje: Kişisel Bilgi Kartı",
                            "type": "project",
                            "duration": 30,
                            "content": """
# Mini Proje: Kişisel Bilgi Kartı

Kullanıcıdan bilgi alıp güzel formatlanmış bir kart oluşturun.

## Gereksinimler
1. Kullanıcıdan isim, yaş, şehir, meslek alın
2. Bilgileri güzel bir formatta yazdırın

## Beklenen Çıktı
```
╔════════════════════════════╗
║     KİŞİSEL BİLGİ KARTI    ║
╠════════════════════════════╣
║ İsim    : Ahmet Yılmaz     ║
║ Yaş     : 25               ║
║ Şehir   : İstanbul         ║
║ Meslek  : Yazılımcı        ║
╚════════════════════════════╝
```

## Çözüm
```python
print("=== Kişisel Bilgi Kartı ===")
isim = input("İsminiz: ")
yas = input("Yaşınız: ")
sehir = input("Şehriniz: ")
meslek = input("Mesleğiniz: ")

print()
print("╔" + "═"*28 + "╗")
print("║     KİŞİSEL BİLGİ KARTI    ║")
print("╠" + "═"*28 + "╣")
print(f"║ İsim    : {isim:<17}║")
print(f"║ Yaş     : {yas:<17}║")
print(f"║ Şehir   : {sehir:<17}║")
print(f"║ Meslek  : {meslek:<17}║")
print("╚" + "═"*28 + "╝")
```
                            """,
                            "resources": []
                        }
                    ],
                    "quiz": [],
                    "objectives": [
                        "Hafta 1 konularını pekiştirme",
                        "İlk mini projeyi tamamlama"
                    ],
                    "tip": "💡 Projeyi önce kendiniz yazmayı deneyin, takılırsanız çözüme bakın."
                },
                7: {
                    "theme": "Hafta 1 Final Quiz ve Değerlendirme",
                    "lessons": [
                        {
                            "id": "w1d7_l1",
                            "title": "Hafta 1 Final Quiz",
                            "type": "quiz",
                            "duration": 20,
                            "content": "Hafta 1'de öğrendiğiniz tüm konuları kapsayan final quiz.",
                            "resources": []
                        }
                    ],
                    "quiz": [
                        {"id": "w1_final_q1", "question": "Python'da yorum satırı nasıl yazılır?", "options": ["// yorum", "# yorum", "/* yorum */", "-- yorum"], "correct": "# yorum"},
                        {"id": "w1_final_q2", "question": "type(3.14) sonucu nedir?", "options": ["<class 'int'>", "<class 'float'>", "<class 'str'>", "<class 'double'>"], "correct": "<class 'float'>"},
                        {"id": "w1_final_q3", "question": "'Python'[-1] sonucu nedir?", "options": ["P", "n", "o", "Hata"], "correct": "n"},
                        {"id": "w1_final_q4", "question": "2 ** 3 sonucu nedir?", "options": ["6", "8", "5", "9"], "correct": "8"},
                        {"id": "w1_final_q5", "question": "f'Yaş: {25}' ifadesinin adı nedir?", "options": ["concat", "format", "f-string", "template"], "correct": "f-string"}
                    ],
                    "objectives": [
                        "Hafta 1 bilgilerini test etme",
                        "Eksik konuları belirleme"
                    ],
                    "tip": "💡 %70 ve üzeri puan alırsanız Hafta 2'ye geçebilirsiniz."
                }
            },
            "project": {
                "title": "Basit Hesap Makinesi",
                "description": "Dört işlem yapabilen basit bir hesap makinesi programı yazın.",
                "requirements": [
                    "Kullanıcıdan iki sayı alın",
                    "İşlem seçtirin (+, -, *, /)",
                    "Sonucu gösterin"
                ]
            }
        },
        # HAFTA 2: Kontrol Yapıları
        2: {
            "title": "Kontrol Yapıları",
            "description": "if-else koşulları ve döngüler",
            "days": {
                1: {
                    "theme": "if-else Koşulları",
                    "lessons": [
                        {
                            "id": "w2d1_l1",
                            "title": "if-else Yapısı",
                            "type": "theory",
                            "duration": 25,
                            "content": """
# if-else Koşulları

## Temel Yapı
```python
yas = 18

if yas >= 18:
    print("Yetişkinsiniz")
else:
    print("Reşit değilsiniz")
```

## elif (else if)
```python
not_ortalamasi = 75

if not_ortalamasi >= 90:
    print("AA")
elif not_ortalamasi >= 80:
    print("BA")
elif not_ortalamasi >= 70:
    print("BB")
elif not_ortalamasi >= 60:
    print("CB")
else:
    print("Kaldınız")
```

## Mantıksal Operatörler
```python
yas = 25
gelir = 5000

# and - her iki koşul da doğru olmalı
if yas >= 18 and gelir >= 3000:
    print("Kredi alabilirsiniz")

# or - en az biri doğru olmalı
if yas < 18 or yas > 65:
    print("İndirimli bilet")

# not - koşulu tersine çevirir
if not yas < 18:
    print("Yetişkin")
```
                            """,
                            "resources": []
                        }
                    ],
                    "quiz": [
                        {"id": "w2d1_q1", "question": "if bloğu içindeki kod ne zaman çalışır?", "options": ["Her zaman", "Koşul True ise", "Koşul False ise", "Rastgele"], "correct": "Koşul True ise"},
                        {"id": "w2d1_q2", "question": "True and False sonucu nedir?", "options": ["True", "False", "None", "Hata"], "correct": "False"}
                    ],
                    "objectives": ["if-else yapısını anlama", "Mantıksal operatörleri kullanma"],
                    "tip": "💡 Python'da girintiler (indent) çok önemlidir! 4 boşluk kullanın."
                },
                2: {
                    "theme": "for Döngüsü",
                    "lessons": [
                        {
                            "id": "w2d2_l1",
                            "title": "for Döngüsü",
                            "type": "theory",
                            "duration": 25,
                            "content": """
# for Döngüsü

## range() ile Kullanım
```python
# 0'dan 4'e kadar (5 dahil değil)
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# 1'den 5'e kadar
for i in range(1, 6):
    print(i)  # 1, 2, 3, 4, 5

# 2'şer artarak
for i in range(0, 10, 2):
    print(i)  # 0, 2, 4, 6, 8
```

## Liste ile Kullanım
```python
meyveler = ["elma", "armut", "muz"]
for meyve in meyveler:
    print(meyve)
```

## String ile Kullanım
```python
kelime = "Python"
for harf in kelime:
    print(harf)
```
                            """,
                            "resources": []
                        }
                    ],
                    "quiz": [
                        {"id": "w2d2_q1", "question": "range(3) kaç sayı üretir?", "options": ["2", "3", "4", "1"], "correct": "3"},
                        {"id": "w2d2_q2", "question": "range(1, 5) hangi sayıları üretir?", "options": ["1,2,3,4,5", "1,2,3,4", "0,1,2,3,4", "2,3,4"], "correct": "1,2,3,4"}
                    ],
                    "objectives": ["for döngüsünü anlama", "range() fonksiyonunu kullanma"],
                    "tip": "💡 range(n) 0'dan n-1'e kadar sayı üretir."
                },
                3: {
                    "theme": "while Döngüsü",
                    "lessons": [
                        {
                            "id": "w2d3_l1",
                            "title": "while Döngüsü",
                            "type": "theory",
                            "duration": 20,
                            "content": """
# while Döngüsü

## Temel Yapı
```python
sayac = 0
while sayac < 5:
    print(sayac)
    sayac += 1  # sayac = sayac + 1
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

## Sonsuz Döngü (Dikkat!)
```python
# Bu döngü sonsuza kadar çalışır!
# while True:
#     print("Sonsuz!")

# Doğru kullanım
while True:
    cevap = input("Çıkmak için 'q' yazın: ")
    if cevap == 'q':
        break
```
                            """,
                            "resources": []
                        }
                    ],
                    "quiz": [
                        {"id": "w2d3_q1", "question": "break ne işe yarar?", "options": ["Döngüyü sonlandırır", "Sonraki iterasyona geçer", "Döngüyü duraklatır", "Hata verir"], "correct": "Döngüyü sonlandırır"}
                    ],
                    "objectives": ["while döngüsünü anlama", "break ve continue kullanma"],
                    "tip": "💡 while döngüsünde koşulun bir noktada False olmasını sağlayın, yoksa sonsuz döngüye girersiniz!"
                },
                4: {"theme": "Döngü Alıştırmaları", "lessons": [], "quiz": [], "objectives": ["Döngü pratiği yapma"], "tip": ""},
                5: {"theme": "İç İçe Döngüler", "lessons": [], "quiz": [], "objectives": ["İç içe döngüleri anlama"], "tip": ""},
                6: {"theme": "Hafta 2 Tekrar", "lessons": [], "quiz": [], "objectives": ["Hafta 2 konularını pekiştirme"], "tip": ""},
                7: {"theme": "Hafta 2 Final Quiz", "lessons": [], "quiz": [], "objectives": ["Hafta 2 bilgilerini test etme"], "tip": ""}
            },
            "project": {
                "title": "Sayı Tahmin Oyunu",
                "description": "Bilgisayarın tuttuğu sayıyı tahmin etme oyunu",
                "requirements": ["1-100 arası rastgele sayı", "Kullanıcıya ipucu ver (büyük/küçük)", "Deneme sayısını say"]
            }
        },
        # HAFTA 3 ve 4 için kısa tanımlar
        3: {
            "title": "Veri Yapıları",
            "description": "Liste, tuple, dictionary, set",
            "days": {i: {"theme": f"Gün {i}", "lessons": [], "quiz": [], "objectives": [], "tip": ""} for i in range(1, 8)},
            "project": {"title": "Telefon Rehberi", "description": "Dictionary kullanarak telefon rehberi", "requirements": []}
        },
        4: {
            "title": "Fonksiyonlar ve Modüller",
            "description": "Fonksiyon tanımlama, parametreler, modüller",
            "days": {i: {"theme": f"Gün {i}", "lessons": [], "quiz": [], "objectives": [], "tip": ""} for i in range(1, 8)},
            "project": {"title": "Kütüphane Yönetim Sistemi", "description": "Kitap ekleme, silme, arama", "requirements": []}
        }
    }
}


# =============================================================================
# WEB GELİŞTİRME PROGRAMI (6 Hafta)
# =============================================================================

WEB_DEV_PROGRAM = {
    "program_id": "web_development",
    "title": "🌐 Web Geliştirme Temelleri",
    "description": "HTML, CSS ve JavaScript ile web sitesi geliştirmeyi öğrenin.",
    "duration_weeks": 6,
    "difficulty": "Başlangıç",
    "prerequisites": [],
    "skills_gained": [
        "HTML5 ile sayfa yapısı",
        "CSS3 ile stil ve tasarım",
        "JavaScript temelleri",
        "Responsive tasarım",
        "DOM manipülasyonu"
    ],
    "icon": "🌐",
    "curriculum": {
        1: {"title": "HTML Temelleri", "description": "HTML etiketleri ve sayfa yapısı", "days": {}, "project": {}},
        2: {"title": "CSS Temelleri", "description": "Stil, renkler, layout", "days": {}, "project": {}},
        3: {"title": "CSS İleri", "description": "Flexbox, Grid, animasyonlar", "days": {}, "project": {}},
        4: {"title": "JavaScript Temelleri", "description": "Değişkenler, fonksiyonlar, olaylar", "days": {}, "project": {}},
        5: {"title": "DOM Manipülasyonu", "description": "Sayfa elementlerini kontrol etme", "days": {}, "project": {}},
        6: {"title": "Final Proje", "description": "Kişisel portfolio sitesi", "days": {}, "project": {}}
    }
}


# =============================================================================
# VERİ BİLİMİ PROGRAMI (8 Hafta)
# =============================================================================

DATA_SCIENCE_PROGRAM = {
    "program_id": "data_science",
    "title": "📊 Veri Bilimi Temelleri",
    "description": "Python ile veri analizi, görselleştirme ve makine öğrenmesine giriş.",
    "duration_weeks": 8,
    "difficulty": "Orta",
    "prerequisites": ["Python Temelleri"],
    "skills_gained": [
        "NumPy ile sayısal işlemler",
        "Pandas ile veri analizi",
        "Matplotlib/Seaborn ile görselleştirme",
        "Temel istatistik",
        "Makine öğrenmesine giriş"
    ],
    "icon": "📊",
    "curriculum": {}
}


# =============================================================================
# PROGRAM YÖNETİMİ
# =============================================================================

ALL_PROGRAMS = {
    "python_basics": PYTHON_BASICS_PROGRAM,
    "web_development": WEB_DEV_PROGRAM,
    "data_science": DATA_SCIENCE_PROGRAM
}


def get_all_programs() -> Dict:
    """Tüm programları döndürür."""
    return ALL_PROGRAMS


def get_program(program_id: str) -> Dict:
    """Belirli bir programı döndürür."""
    return ALL_PROGRAMS.get(program_id)


def get_day_content(program_id: str, week: int, day: int) -> Dict:
    """Belirli bir günün içeriğini döndürür."""
    program = get_program(program_id)
    if not program:
        return None
    
    curriculum = program.get("curriculum", {})
    week_data = curriculum.get(week, {})
    days = week_data.get("days", {})
    return days.get(day)


def get_week_content(program_id: str, week: int) -> Dict:
    """Belirli bir haftanın içeriğini döndürür."""
    program = get_program(program_id)
    if not program:
        return None
    
    return program.get("curriculum", {}).get(week)

