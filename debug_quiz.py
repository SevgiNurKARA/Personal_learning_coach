
import os
import sys
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Windows encoding fix
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

print("="*50)
print("📝 QUIZ MODÜLÜ DEBUGGER")
print("="*50)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ API Key yok!")
    sys.exit(1)

genai.configure(api_key=api_key)

# App'in kullandığı model
MODEL_NAME = "gemini-2.5-flash" 

print(f"🤖 Model: {MODEL_NAME}")
print("🔄 Quiz üretimi deneniyor...")

try:
    model = genai.GenerativeModel(MODEL_NAME)
    
    topic = "Python Değişkenler"
    prompt = f"""
    Günlük ders konusu: "{topic}"
    Seviye: başlangıç
    
    Bu günün dersi için TAMAMEN "{topic}" konusuna odaklanmış 3 adet çoktan seçmeli quiz sorusu oluştur.
    
    JSON formatında döndür:
    [
        {{
            "question_id": "q1",
            "question": "Soru metni?",
            "options": ["A", "B", "C", "D"],
            "correct_answer": "Doğru seçenek (tam olarak options'dan biri)",
            "topic": "{topic}"
        }}
    ]
    
    SADECE JSON döndür.
    """
    
    response = model.generate_content(prompt)
    raw_text = response.text
    
    print("\n📦 AI RAW ÇIKTI:")
    print("-" * 20)
    print(raw_text)
    print("-" * 20)
    
    # JSON Parsing Testi
    clean_text = raw_text.strip()
    if "```json" in clean_text:
        clean_text = clean_text.split("```json")[1].split("```")[0]
    elif "```" in clean_text:
        clean_text = clean_text.split("```")[1].split("```")[0]
        
    data = json.loads(clean_text)
    print(f"\n✅ JSON Parse Başarılı! {len(data)} soru üretildi.")
    print(json.dumps(data, indent=2, ensure_ascii=False))

except Exception as e:
    print(f"\n❌ HATA: {e}")
    if "404" in str(e):
        print("⚠️ Model bulunamadı hatası. 'gemini-2.5-flash' kullanılamıyor olabilir.")
        print("   Alternatif olarak 'gemini-1.5-flash' denenmeli.")

print("\n" + "="*50)
