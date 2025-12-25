# 📚 Günlük Öğrenme Akışı

## 🔄 Doğru Sıralama

```
┌─────────────────────────────────────────────────────────┐
│                    GÜN BAŞLANGICI                        │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  1️⃣  DERS İÇERİĞİ                                       │
│  📚 Dersi Oku                                            │
│  • Teori ve kavramları öğren                             │
│  • Örnekleri incele                                      │
│  • Kaynakları gözden geçir                               │
│  ⏱️  Tahmini Süre: 20-30 dakika                          │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│  2️⃣  QUIZ                                                │
│  📝 Öğrendiklerini Test Et                               │
│  • 5 soru çöz                                            │
│  • Anlık geri bildirim al                                │
│  • Yanlış cevapları gör                                  │
│  ⏱️  Tahmini Süre: 10-15 dakika                          │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Quiz Skoru? │
                    └─────────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
            ▼              ▼              ▼
      ┌─────────┐    ┌─────────┐    ┌─────────┐
      │ < %60   │    │ %60-79  │    │ ≥ %80   │
      │ Düşük   │    │  İyi    │    │ Harika  │
      └─────────┘    └─────────┘    └─────────┘
            │              │              │
            └──────────────┼──────────────┘
                           │
                    ┌──────▼──────┐
                    │  Seçenekler │
                    └─────────────┘
                           │
            ┌──────────────┼──────────────┐
            │                             │
            ▼                             ▼
    ┌──────────────┐            ┌──────────────┐
    │ 🔄 Tekrarla  │            │ ✅ Devam Et  │
    │ Dersi oku    │            │ Günü tamamla │
    │ Quiz tekrar  │            │              │
    └──────────────┘            └──────────────┘
                                        │
                                        ▼
                            ┌─────────────────────┐
                            │  3️⃣  GÜN TAMAMLA     │
                            │  ✅ İlerle           │
                            │  • Gün kaydedilir   │
                            │  • Sonraki gün açılır│
                            └─────────────────────┘
                                        │
                                        ▼
                            ┌─────────────────────┐
                            │   SONRAKİ GÜN       │
                            │   🎯 Devam!         │
                            └─────────────────────┘
```

## ⚠️ Önemli Kurallar

### ✅ Yapılabilir

- ✅ Dersi okumadan quiz'e geçebilirsiniz
- ✅ Quiz'i istediğiniz kadar tekrarlayabilirsiniz
- ✅ Geçmiş günlere geri dönebilirsiniz
- ✅ Quiz'i çözdükten sonra günü tamamlayabilirsiniz

### ❌ Yapılamaz

- ❌ Quiz çözmeden gün tamamlanamaz
- ❌ Günü tamamlamadan sonraki güne geçilemez
- ❌ Kilitli günlere erişilemez

## 📊 Durum Göstergeleri

### Konu Haritasında

| İkon | Durum | Açıklama |
|------|-------|----------|
| ▶️ | Mevcut Gün | Şu an bu gündeysiniz |
| 📝 | Quiz Tamamlandı | Quiz çözüldü, gün tamamlanmayı bekliyor |
| ✅ | Tamamlandı | Gün başarıyla tamamlandı |
| 🔒 | Kilitli | Henüz açılmadı |

### Dashboard'da

| Durum | Mesaj | Aksiyon |
|-------|-------|---------|
| Quiz Çözülmedi | ⚠️ Önce dersi okuyun ve quiz'i çözün | Quiz butonu aktif |
| Quiz Çözüldü | ✅ Quiz tamamlandı (%XX). Günü tamamlayabilirsiniz! | Tamamla butonu aktif |
| Gün Tamamlandı | ✅ Bu gün tamamlandı! | Sonraki güne geçildi |

## 🎯 Örnek Senaryo

### Senaryo 1: İlk Kez Gün 1

```
1. Dashboard'a gir
   └── Gün 1 açık, diğerleri kilitli

2. "📚 Ders İçeriği" butonuna tıkla
   └── Python Giriş dersini oku
   └── 20 dakika

3. "📝 Quiz'e Geç" butonuna tıkla
   └── 5 soru çöz
   └── Sonuç: %80 (4/5 doğru)
   └── ✅ "Artık günü tamamlayabilirsiniz!"

4. Dashboard'a dön
   └── "✅ Günü Tamamla" butonu aktif
   └── Tıkla

5. Gün 2 otomatik açıldı
   └── Gün 1 ✅ işaretli
   └── Gün 2 ▶️ aktif
```

### Senaryo 2: Düşük Skor

```
1. Quiz çöz
   └── Sonuç: %40 (2/5 doğru)
   └── ⚠️ "Daha iyi bir skor için tekrarlayın"

2. Seçenekler:
   
   A) Tekrarla:
      └── "📚 Ders İçeriği" → Dersi tekrar oku
      └── "🔄 Quiz Tekrarla" → Yeniden çöz
      └── Yeni skor: %80
      └── ✅ Günü tamamla
   
   B) Devam Et:
      └── %40 ile de günü tamamlayabilirsiniz
      └── Ama öğrenme kalitesi düşük olur
```

### Senaryo 3: Geçmiş Günlere Dönme

```
1. Gün 5'tesin
   └── Gün 1-4 tamamlandı ✅
   └── Gün 5 aktif ▶️

2. Gün 2'ye tıkla
   └── Gün 2 içeriği açıldı
   └── Quiz skoru görünüyor: %85
   └── "🔄 Quiz Tekrarla" ile yeniden çözebilirsin

3. Gün 5'e geri dön
   └── Konu haritasından tıkla
   └── Kaldığın yerden devam et
```

## 💡 İpuçları

1. **Düşük Skor Aldıysanız**
   - Dersi tekrar okuyun
   - Kaynakları inceleyin
   - Quiz'i tekrarlayın
   - %60+ hedefleyin

2. **Zaman Yönetimi**
   - Ders: 20-30 dakika
   - Quiz: 10-15 dakika
   - Toplam: ~45 dakika/gün

3. **Öğrenme Stratejisi**
   - Dersi dikkatlice okuyun
   - Örnekleri anlamaya çalışın
   - Quiz'de tahmin yapmayın
   - Yanlış cevapları analiz edin

4. **Motivasyon**
   - Her gün küçük adımlar
   - Quiz skorlarınızı takip edin
   - İlerleme çubuğunuzu izleyin
   - Tamamlanan günleri kutlayın

---

**Başarılar! 🎓**

