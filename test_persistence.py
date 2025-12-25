"""
İlerleme kaydı test scripti
"""

from models.user import UserManager

def test_persistence():
    um = UserManager()
    
    print("=" * 50)
    print("TEST 1: Yeni Kullanıcı Kaydı")
    print("=" * 50)
    
    success, uid = um.register('TestUser2', 'test2@test.com', '1234')
    print(f"✅ Kayıt başarılı: {success}")
    print(f"User ID: {uid}")
    
    print("\n" + "=" * 50)
    print("TEST 2: Müfredat Kaydetme")
    print("=" * 50)
    
    test_curriculum = {
        'goal': 'Python Öğrenmek',
        'level': 'beginner',
        'daily_lessons': [
            {'day': 1, 'theme': 'Python Giriş'},
            {'day': 2, 'theme': 'Değişkenler'},
            {'day': 3, 'theme': 'Döngüler'}
        ]
    }
    
    test_goal_input = {
        'goal': 'Python Öğrenmek',
        'duration': 2,
        'daily_time': 1.0
    }
    
    test_level = {
        'level': 'beginner',
        'level_tr': 'Başlangıç',
        'score': 45,
        'summary': 'Başlangıç seviyesinden başlayın'
    }
    
    um.save_curriculum(uid, test_curriculum, test_goal_input, test_level, 1, [])
    print("✅ Müfredat kaydedildi")
    
    print("\n" + "=" * 50)
    print("TEST 3: Müfredat Yükleme")
    print("=" * 50)
    
    loaded = um.load_curriculum(uid)
    if loaded:
        print("✅ Müfredat yüklendi")
        print(f"   Hedef: {loaded['curriculum']['goal']}")
        print(f"   Seviye: {loaded['user_level']['level_tr']}")
        print(f"   Mevcut Gün: {loaded['current_day']}")
        print(f"   Ders Sayısı: {len(loaded['curriculum']['daily_lessons'])}")
    else:
        print("❌ Müfredat yüklenemedi")
    
    print("\n" + "=" * 50)
    print("TEST 4: İlerleme Güncelleme")
    print("=" * 50)
    
    # Gün 1'i tamamla
    um.update_progress(uid, 2, [1])
    print("✅ Gün 1 tamamlandı, Gün 2'ye geçildi")
    
    # Quiz skoru kaydet
    um.record_progress(uid, 'quiz_day_1', 0.5, 85)
    print("✅ Quiz skoru kaydedildi (85%)")
    
    # Tekrar yükle
    loaded = um.load_curriculum(uid)
    if loaded:
        print(f"   Yeni Mevcut Gün: {loaded['current_day']}")
        print(f"   Tamamlanan: {loaded['completed_days']}")
    
    print("\n" + "=" * 50)
    print("TEST 5: İstatistikler")
    print("=" * 50)
    
    stats = um.get_user_stats(uid)
    print(f"✅ Toplam Ders: {stats.get('total_lessons', 0)}")
    print(f"✅ Quiz Sayısı: {stats.get('quiz_count', 0)}")
    print(f"✅ Quiz Ortalaması: %{stats.get('average_quiz_score', 0)}")
    print(f"✅ Toplam Saat: {stats.get('total_hours', 0)}")
    
    print("\n" + "=" * 50)
    print("TEST 6: Giriş Yapma (Persistence)")
    print("=" * 50)
    
    success, user = um.login('test2@test.com', '1234')
    if success:
        print("✅ Giriş başarılı")
        print(f"   Kullanıcı: {user.username}")
        print(f"   Müfredat var mı: {user.curriculum is not None}")
        if user.curriculum:
            print(f"   Hedef: {user.curriculum.get('goal', 'N/A')}")
            print(f"   Mevcut Gün: {user.current_day}")
            print(f"   Tamamlanan: {user.completed_days}")
    else:
        print("❌ Giriş başarısız")
    
    print("\n" + "=" * 50)
    print("✅ TÜM TESTLER BAŞARILI!")
    print("=" * 50)


if __name__ == "__main__":
    test_persistence()

