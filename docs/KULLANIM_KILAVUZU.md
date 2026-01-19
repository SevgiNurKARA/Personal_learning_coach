# 🎓 AI Öğrenme Koçu - Kullanım Kılavuzu

## 📋 Özellikler

### ✅ Yeni Eklenen Özellikler

1. **İlerleme Kaydı** 
   - Kullanıcı çıkış yapıp tekrar giriş yaptığında kaldığı yerden devam eder
   - Tamamlanan dersler kaydedilir
   - Quiz sonuçları saklanır
   - Müfredat otomatik yüklenir

2. **Seviye Belirleme Testi**
   - 10 soruluk kapsamlı test
   - Kolay, orta ve zor sorular
   - Otomatik seviye belirleme (Başlangıç/Orta/İleri)
   - Güçlü ve zayıf yönler analizi

3. **AI Destekli Quiz**
   - Her ders için dinamik sorular
   - AI varsa Gemini üretiyor
   - Detaylı skor analizi

4. **Kişiselleştirilmiş Müfredat**
   - Hedefe göre özel içerik
   - Seviyeye uygun başlangıç noktası
   - 2-8 haftalık esnek program

## 🚀 Nasıl Kullanılır?

### 1. İlk Kullanım

```
1. Kayıt Ol
   └── Kullanıcı adı, email, şifre

2. Giriş Yap
   └── Email ve şifre ile

3. Hedef Belirle
   └── "Python öğrenmek istiyorum"
   └── Süre: 2-8 hafta
   └── Günlük çalışma: 0.5-4 saat

4. Seviye Testi Çöz (opsiyonel)
   └── 10 soru
   └── Veya "Seviye Testini Atla"

5. Müfredat Oluştur
   └── AI otomatik oluşturur

6. Öğrenmeye Başla!
   └── Dashboard → Ders → Quiz
```

### 2. Tekrar Giriş

```
1. Giriş Yap
   └── Email ve şifre

2. Otomatik Yükleme
   └── Önceki müfredat yüklenir
   └── Kaldığınız gün açılır
   └── Tamamlanan dersler görünür

3. Devam Et
   └── Kaldığınız yerden devam edin
```

## 📊 Dashboard Özellikleri

### Konu Haritası (Sol Panel)

- **✅ Yeşil Tik**: Tamamlanan dersler
- **▶️ Play**: Mevcut ders
- **⏭️ İleri**: Geçilebilir dersler
- **🔒 Kilit**: Henüz açılmamış dersler

### Günlük İçerik (Sağ Panel)

- **Yapılacaklar**: Görevler ve süreleri
- **Kaynaklar**: Öğrenme materyalleri
- **İpucu**: Günlük motivasyon

### Aksiyonlar (Sıralı Akış)

1. **📚 Ders İçeriği**: Önce dersi okuyun
2. **📝 Quiz Çöz**: Sonra quiz'i çözün
3. **✅ Günü Tamamla**: Quiz'i çözdükten sonra aktif olur

⚠️ **ÖNEMLİ**: Günü tamamlamak için önce quiz'i çözmelisiniz!

## 🎯 Sidebar Menüsü

| Buton | Açıklama |
|-------|----------|
| 🏠 Dashboard | Ana sayfaya dön |
| 📚 Ders | Mevcut dersi aç |
| 📝 Quiz | Quiz sayfası |
| 🎯 Yeni Hedef | Yeni müfredat başlat (mevcut ilerleme silinir) |
| 📊 Seviye Testi | Seviye testini tekrar çöz |
| 🚪 Çıkış | Oturumu kapat |

## 💾 Veri Saklama

### Kaydedilen Bilgiler

```json
{
  "curriculum": "Tam müfredat (konular, dersler, quizler)",
  "goal_input": "Hedef ve tercihler",
  "user_level": "Seviye test sonuçları",
  "current_day": "Mevcut gün numarası",
  "completed_days": "Tamamlanan günler listesi",
  "quiz_scores": "Quiz sonuçları ve tarihler",
  "total_study_hours": "Toplam çalışma saati"
}
```

### Dosya Konumu

- **Kullanıcı Verileri**: `data/users.json`
- **Müfredat**: Her kullanıcı için `user.curriculum` alanında

## 🔄 İlerleme Takibi

### Otomatik Kayıt

- ✅ Gün tamamlandığında
- 📝 Quiz çözüldüğünde
- 🎯 Müfredat oluşturulduğunda
- 🔄 Her önemli değişiklikte

### Manuel Kayıt

Gerek yok! Sistem otomatik kaydeder.

## 🎓 Seviye Sistemi

### Başlangıç (Beginner)
- Temel kavramlar
- Adım adım öğrenme
- Gün 1'den başlar

### Orta (Intermediate)
- Uygulama odaklı
- Bazı konular atlanır
- Gün 8'den başlar

### İleri (Advanced)
- Derinlemesine konular
- Hızlı ilerleme
- Gün 15'ten başlar

## 🤖 AI Özellikleri

### AI Aktif İse
- ✅ Kişiselleştirilmiş müfredat
- ✅ Dinamik quiz soruları
- ✅ Detaylı ders içeriği
- ✅ Seviye testi soruları

### AI Mock Mod İse
- ⚠️ Şablon müfredat
- ⚠️ Hazır quiz soruları
- ⚠️ Genel ders içeriği
- ⚠️ Standart seviye testi

## 📱 Kullanım İpuçları

1. **Düzenli Çalışın**: Her gün belirlediğiniz süre kadar çalışın
2. **Sıralı İlerleyin**: Ders → Quiz → Gün Tamamla sırasını takip edin
3. **Quiz'leri Atlayamayın**: Quiz çözmeden gün tamamlanamaz
4. **Kaynakları İnceleyin**: Ek materyaller faydalıdır
5. **İlerlemeyi Takip Edin**: Sidebar'daki istatistiklere bakın
6. **Seviye Testini Ciddiye Alın**: Doğru seviyeden başlamak önemli
7. **Quiz'i Tekrarlayın**: Düşük skor aldıysanız dersi tekrar okuyup quiz'i tekrarlayabilirsiniz

## 🔧 Sorun Giderme

### "Müfredat Yüklenemiyor"
- Çıkış yapıp tekrar giriş yapın
- Yeni hedef belirleyin

### "Quiz Soruları Gelmiyor"
- Sayfayı yenileyin
- "Tekrar Dene" butonuna tıklayın

### "İlerleme Kayboldu"
- Aynı hesapla giriş yaptığınızdan emin olun
- `data/users.json` dosyasını kontrol edin

## 📞 Destek

Sorun yaşarsanız:
1. Tarayıcı konsolunu kontrol edin (F12)
2. Terminal çıktısına bakın
3. `data/users.json` dosyasını kontrol edin

---

**İyi Öğrenmeler! 🎓**

