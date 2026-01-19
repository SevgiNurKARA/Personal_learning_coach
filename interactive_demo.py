"""
Interaktif Demo - Gerçek API'lerle Çalışma
==========================================

Bu script, projenin gerçek API'lerle nasıl çalıştığını gösterir.
.env dosyasında API anahtarlarınız varsa gerçek AI yanıtları alırsınız.
"""

import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

from agents.orchestrator_agent import OrchestratorAgent
from tools.google_search import GoogleSearchTool
from tools.ai_service import AIService, get_ai_service
from tools.quiz_scoring import QuizScorer
from memory.memory_bank import MemoryBank


def check_api_status():
    """API durumlarını kontrol eder."""
    print("\n" + "=" * 60)
    print("🔍 API DURUM KONTROLÜ")
    print("=" * 60)
    
    # Gemini API kontrolü
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    if gemini_key and gemini_key != "your_gemini_api_key_here":
        print("✅ Gemini API: Yapılandırılmış")
        ai_mode = "GERÇEK AI"
    else:
        print("⚠️  Gemini API: Yapılandırılmamış (Mock mod)")
        ai_mode = "MOCK"
    
    # Google Search API kontrolü
    search_key = os.getenv("GOOGLE_SEARCH_API_KEY", "")
    search_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")
    if search_key and search_id:
        print("✅ Google Search API: Yapılandırılmış")
        search_mode = "GERÇEK ARAMA"
    else:
        print("⚠️  Google Search API: Yapılandırılmamış (Mock mod)")
        search_mode = "MOCK"
    
    print(f"\n📊 Çalışma Modu: AI={ai_mode}, Arama={search_mode}")
    print("=" * 60)
    
    return ai_mode == "GERÇEK AI"


def interactive_profile_creation():
    """Kullanıcıdan interaktif profil oluşturur."""
    print("\n" + "=" * 60)
    print("👤 PROFİL OLUŞTURMA")
    print("=" * 60)
    
    print("\nÖğrenme hedefinizi girin:")
    print("  Örnekler: 'Python öğrenmek', 'Web geliştirme', 'Veri bilimi'")
    goal = input("  Hedefiniz: ").strip() or "Python programlama öğrenmek"
    
    print("\nMevcut seviyenizi seçin:")
    print("  1. Başlangıç (hiç bilmiyorum)")
    print("  2. Orta (temel bilgim var)")
    print("  3. İleri (deneyimliyim)")
    level_choice = input("  Seçiminiz (1/2/3): ").strip()
    level_map = {"1": "başlangıç", "2": "orta", "3": "ileri"}
    level = level_map.get(level_choice, "başlangıç")
    
    print("\nGünde kaç saat çalışabilirsiniz?")
    try:
        daily_time = float(input("  Saat (örn: 1.5): ").strip() or "1")
    except ValueError:
        daily_time = 1.0
    
    print("\nÖğrenme stilinizi seçin:")
    print("  1. Teori ağırlıklı")
    print("  2. Pratik ağırlıklı")
    print("  3. Karma (teori + pratik)")
    style_choice = input("  Seçiminiz (1/2/3): ").strip()
    style_map = {"1": "teori", "2": "pratik", "3": "teori + uygulama"}
    style = style_map.get(style_choice, "teori + uygulama")
    
    profile_input = {
        "goal": goal,
        "current_level": level,
        "daily_available_time": daily_time,
        "preferred_learning_style": style
    }
    
    print("\n✅ Profiliniz oluşturuldu!")
    return profile_input


def run_interactive_demo():
    """Interaktif demo çalıştırır."""
    print("\n" + "=" * 60)
    print("🎓 AI ÖĞRENME KOÇU - İNTERAKTİF DEMO")
    print("=" * 60)
    
    # API durumunu kontrol et
    is_ai_configured = check_api_status()
    
    # Kullanıcıya seçenek sun
    print("\nNasıl devam etmek istersiniz?")
    print("  1. Hızlı demo (hazır verilerle)")
    print("  2. Kendi profilimi oluştur")
    choice = input("  Seçiminiz (1/2): ").strip()
    
    if choice == "2":
        user_input = interactive_profile_creation()
    else:
        # Varsayılan demo verisi
        user_input = {
            "goal": "3 ayda Python temeli",
            "current_level": "başlangıç",
            "daily_available_time": 1.0,
            "preferred_learning_style": "teori + uygulama"
        }
        print("\n📋 Varsayılan profil kullanılıyor...")
    
    # Sistemi başlat
    print("\n" + "=" * 60)
    print("🚀 SİSTEM BAŞLATILIYOR...")
    print("=" * 60)
    
    memory = MemoryBank()
    search_tool = GoogleSearchTool()
    orchestrator = OrchestratorAgent(search_tool=search_tool, memory_service=memory)
    
    # İlk akışı çalıştır
    print("\n📊 Profil analiz ediliyor...")
    out = orchestrator.run_initial_flow(user_input)
    
    print("\n" + "=" * 60)
    print("👤 OLUŞTURULAN PROFİL")
    print("=" * 60)
    print(json.dumps(out["profile"], ensure_ascii=False, indent=2))
    
    print("\n" + "=" * 60)
    print("📅 GÜN 1 - ÇALIŞMA PLANI")
    print("=" * 60)
    print(json.dumps(out["plan"], ensure_ascii=False, indent=2))
    
    # Quiz demo
    print("\n" + "=" * 60)
    print("📝 ÖRNEK QUİZ")
    print("=" * 60)
    
    quiz_scorer = QuizScorer()
    quiz_questions = quiz_scorer.generate_sample_quiz("python", 3)
    
    print("\nSize 3 soruluk bir quiz sunuyorum:\n")
    user_answers = {}
    
    for i, q in enumerate(quiz_questions, 1):
        print(f"Soru {i}: {q.question}")
        for j, opt in enumerate(q.options):
            print(f"  {j+1}. {opt}")
        
        try:
            ans_idx = int(input("  Cevabınız (1-4): ").strip()) - 1
            user_answers[q.question_id] = q.options[ans_idx] if 0 <= ans_idx < 4 else q.options[0]
        except (ValueError, IndexError):
            user_answers[q.question_id] = q.options[0]
        print()
    
    # Quiz sonuçlarını hesapla
    key_answers = {q.question_id: q.correct_answer for q in quiz_questions}
    score = quiz_scorer.score_quiz(user_answers, key_answers)
    
    print(f"🎯 Quiz Puanınız: %{score}")
    
    if score >= 80:
        print("🌟 Harika! Çok iyi gidiyorsunuz!")
    elif score >= 50:
        print("👍 İyi! Biraz daha pratik yapın.")
    else:
        print("📚 Konuları tekrar gözden geçirin.")
    
    # Günlük rapor simülasyonu
    print("\n" + "=" * 60)
    print("📊 GÜN SONU DEĞERLENDİRMESİ")
    print("=" * 60)
    
    day_report = {
        "day": 1,
        "completed_tasks": 3,
        "perceived_difficulty": 3,
        "quiz_score": score
    }
    
    out2 = orchestrator.run_daily_cycle(user_id="interactive_user", day_report=day_report)
    
    print("\n✅ Değerlendirme:")
    print(json.dumps(out2["evaluation"], ensure_ascii=False, indent=2))
    
    print("\n📅 GÜN 2 - YENİ PLAN:")
    print(json.dumps(out2["next_plan"], ensure_ascii=False, indent=2))
    
    # AI açıklama (eğer yapılandırılmışsa)
    if is_ai_configured:
        print("\n" + "=" * 60)
        print("🤖 AI KONU AÇIKLAMASI")
        print("=" * 60)
        
        ai_service = get_ai_service()
        topic = out["profile"].get("domain", "python")
        explanation = ai_service.explain_topic(f"{topic} değişkenler", "beginner")
        print(f"\n{explanation}")
    
    print("\n" + "=" * 60)
    print("✨ DEMO TAMAMLANDI!")
    print("=" * 60)
    print("\n💡 İpucu: Gerçek AI yanıtları için .env dosyasına")
    print("   GEMINI_API_KEY ekleyin.")
    print("\n   Detaylar için: SETUP_GUIDE.md dosyasını okuyun.")


def test_ai_directly():
    """AI servisini doğrudan test eder."""
    print("\n" + "=" * 60)
    print("🤖 AI SERVİSİ DOĞRUDAN TEST")
    print("=" * 60)
    
    ai_service = get_ai_service()
    
    if not ai_service._is_configured():
        print("\n⚠️ Gemini API yapılandırılmamış!")
        print("\nYapılandırmak için:")
        print("1. https://aistudio.google.com/app/apikey adresinden API key alın")
        print("2. Proje klasöründe .env dosyası oluşturun")
        print("3. İçine şunu yazın: GEMINI_API_KEY=sizin_api_keyiniz")
        return
    
    print("\n✅ Gemini API yapılandırılmış!")
    print("\nBir konu girin (örn: 'Python listeler'):")
    topic = input("  Konu: ").strip() or "Python değişkenler"
    
    print(f"\n🔄 '{topic}' konusu açıklanıyor...\n")
    explanation = ai_service.explain_topic(topic, "beginner")
    print(explanation)


if __name__ == "__main__":
    print("\n🎓 AI ÖĞRENME KOÇU")
    print("=" * 40)
    print("\nSeçenekler:")
    print("  1. İnteraktif demo çalıştır")
    print("  2. AI servisini test et")
    print("  3. Çıkış")
    
    choice = input("\nSeçiminiz (1/2/3): ").strip()
    
    if choice == "1":
        run_interactive_demo()
    elif choice == "2":
        test_ai_directly()
    else:
        print("\nGörüşmek üzere! 👋")

