"""Quiz sistemi test scripti"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

print("=" * 60)
print("TEST 1: CurriculumAgent - Müfredat Quiz'leri")
print("=" * 60)

from agents.curriculum_agent import get_curriculum_agent

c = get_curriculum_agent()
curr = c.generate_curriculum('Python öğrenmek', 'beginner', 1)

print(f"✅ Müfredat oluşturuldu")
print(f"   Kaynak: {curr.get('source', 'N/A')}")
print(f"   Toplam gün: {len(curr['daily_lessons'])}")

for i, lesson in enumerate(curr['daily_lessons'][:3]):  # İlk 3 gün
    quiz_count = len(lesson.get('quiz', []))
    print(f"   Gün {lesson['day']}: {lesson['theme'][:40]} - Quiz: {quiz_count} soru")
    
    if quiz_count > 0:
        first_q = lesson['quiz'][0]
        print(f"      İlk soru: {first_q.get('question', 'N/A')[:50]}...")

print("\n" + "=" * 60)
print("TEST 2: ContentAgent - Dinamik Quiz Üretimi")
print("=" * 60)

from agents.content_agent import get_content_agent

ca = get_content_agent()
quiz = ca.generate_quiz('Python Değişkenler', 'beginner', 5)

print(f"✅ ContentAgent quiz üretti")
print(f"   Soru sayısı: {len(quiz)}")

if quiz:
    for i, q in enumerate(quiz[:2]):  # İlk 2 soru
        print(f"   Soru {i+1}: {q.get('question', 'N/A')[:50]}...")
        print(f"      Seçenekler: {len(q.get('options', []))}")
        print(f"      Doğru: {q.get('correct_answer', 'N/A')}")

print("\n" + "=" * 60)
print("TEST 3: App.py Quiz Yükleme Simülasyonu")
print("=" * 60)

# Senaryo 1: Müfredatta quiz var
lesson_with_quiz = curr['daily_lessons'][0]
existing_quiz = lesson_with_quiz.get('quiz', [])

print(f"Senaryo 1: Müfredatta quiz var mı?")
print(f"   Lesson quiz sayısı: {len(existing_quiz)}")

if existing_quiz and len(existing_quiz) >= 3:
    print(f"   ✅ Müfredattan {len(existing_quiz)} soru kullanılacak")
else:
    print(f"   ⚠️ Müfredatta yeterli quiz yok, ContentAgent çağrılacak")
    
    # ContentAgent'tan al
    theme = lesson_with_quiz['theme']
    level = 'beginner'
    questions = ca.generate_quiz(theme, level, 5)
    
    if questions and len(questions) > 0:
        print(f"   ✅ ContentAgent {len(questions)} soru üretti")
    else:
        print(f"   ❌ ContentAgent soru üretemedi")

print("\n" + "=" * 60)
print("✅ TÜM TESTLER TAMAMLANDI")
print("=" * 60)

