# 🚀 Gerçek API'lerle Çalıştırma Rehberi

Bu rehber, projeyi gerçek AI ve arama API'leriyle çalıştırmak için gerekli adımları açıklar.

---

## 📋 Gereksinimler

1. Python 3.8+
2. Google hesabı
3. İnternet bağlantısı

---

## 🔧 Kurulum Adımları

### Adım 1: Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### Adım 2: Google Gemini API Anahtarı Alın (ÜCRETSİZ)

1. **https://aistudio.google.com/app/apikey** adresine gidin
2. Google hesabınızla giriş yapın
3. "Create API Key" butonuna tıklayın
4. API anahtarınızı kopyalayın

### Adım 3: .env Dosyası Oluşturun

Proje klasöründe `.env` adında bir dosya oluşturun ve içine şunları yazın:

```
GEMINI_API_KEY=buraya_api_anahtarinizi_yapiştirin
GEMINI_MODEL=gemini-1.5-flash
```

**Örnek:**
```
GEMINI_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GEMINI_MODEL=gemini-1.5-flash
```

### Adım 4: Projeyi Çalıştırın

```bash
python main.py --demo
```

---

## 🔍 Google Search API (Opsiyonel)

Gerçek web araması için ek olarak:

### 1. Google Cloud Console'da API Anahtarı Alın
- https://console.cloud.google.com/apis/credentials
- "Create Credentials" > "API Key"

### 2. Custom Search Engine Oluşturun
- https://programmablesearchengine.google.com/
- Yeni arama motoru oluşturun
- "Search engine ID" değerini kopyalayın

### 3. .env Dosyasına Ekleyin
```
GOOGLE_SEARCH_API_KEY=buraya_search_api_key
GOOGLE_SEARCH_ENGINE_ID=buraya_search_engine_id
```

---

## ✅ Test Etme

API'nin çalışıp çalışmadığını test etmek için:

```bash
python -c "from tools.ai_service import AIService; ai = AIService(); print('Configured:', ai._is_configured())"
```

Çıktı `Configured: True` olmalı.

---

## ⚠️ Önemli Notlar

1. **Ücretsiz Kullanım:** Gemini API günlük 60 istek ücretsiz
2. **Güvenlik:** `.env` dosyasını asla GitHub'a yüklemeyin
3. **Mock Mod:** API anahtarı yoksa otomatik olarak örnek veriler kullanılır

---

## 🎯 Hızlı Başlangıç (Sadece Gemini)

En hızlı şekilde başlamak için sadece Gemini API yeterli:

1. https://aistudio.google.com/app/apikey → API key al
2. `.env` dosyası oluştur → `GEMINI_API_KEY=...` yaz
3. `python main.py --demo` çalıştır

**Bu kadar!** 🎉

