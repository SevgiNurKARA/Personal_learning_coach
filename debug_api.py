
import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Windows encoding fix
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

print("="*50)
print("🔍 API DİAGNOSTİK ARACI")
print("="*50)

# 1. .env Dosyası Kontrolü
env_path = os.path.join(os.getcwd(), '.env')
print(f"📂 Çalışma dizini: {os.getcwd()}")
print(f"📄 .env yolu: {env_path}")

if os.path.exists(env_path):
    print("✅ .env dosyası bulundu.")
else:
    print("❌ .env dosyası BULUNAMADI!")

# 2. Yükleme
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    masked_key = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else "****"
    print(f"✅ API Key yüklendi: {masked_key}")
    
    # "your_" kontrolü
    if "your_" in api_key.lower():
        print("❌ HATA: API Key değiştirilmemiş! Lütfen .env dosyasını düzenleyin.")
        sys.exit(1)
else:
    print("❌ HATA: GEMINI_API_KEY bulunamadı!")
    sys.exit(1)

# 3. Bağlantı Testi
print("\n🔄 Google Gemini API bağlantısı test ediliyor...")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    response = model.generate_content("Merhaba, bu bir test mesajıdır. Cevap ver: 'Bağlantı Başarılı'")
    
    print("\n✅ API BAŞARIYLA ÇALIŞTI!")
    print(f"🤖 AI Cevabı: {response.text}")
    
except Exception as e:
    print("\n❌ API BAĞLANTI HATASI:")
    print(e)
    print("\nOlası nedenler:")
    print("1. API Key hatalı kopyalanmış olabilir")
    print("2. İnternet bağlantısı kısıtlı olabilir (VPN/Proxy gerekebilir)")
    print("3. Google AI Studio kotası dolmuş olabilir")

print("\n" + "="*50)
