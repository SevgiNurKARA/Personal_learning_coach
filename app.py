"""
🎓 AI Öğrenme Koçu - Web Arayüzü v5.0
=====================================
- Kullanıcı hedef yazar
- Seviye testi ile gerçek seviye belirlenir
- AI tam müfredat oluşturur
- Quiz soruları AI'dan gelir

Çalıştırmak için: streamlit run app.py
"""

import streamlit as st
import json
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Agent'ları import et
from agents.curriculum_agent import CurriculumAgent, get_curriculum_agent
from agents.content_agent import ContentAgent, get_content_agent
from agents.level_assessment_agent import LevelAssessmentAgent, get_level_assessment_agent
from models.user import UserManager, User

# Sayfa yapılandırması
st.set_page_config(
    page_title="AI Öğrenme Koçu",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    
    .main-header {
        font-family: 'Poppins', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
    }
    
    .stat-number {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .topic-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 0.8rem;
        margin: 0.3rem 0;
        border-left: 4px solid #28a745;
    }
    
    .task-item {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid #e9ecef;
    }
    
    .task-item.theory { border-left: 4px solid #007bff; }
    .task-item.practice { border-left: 4px solid #28a745; }
    .task-item.quiz { border-left: 4px solid #ffc107; }
    
    .level-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .level-beginner { background: #d4edda; color: #155724; }
    .level-intermediate { background: #fff3cd; color: #856404; }
    .level-advanced { background: #cce5ff; color: #004085; }
    
    .question-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
    
    .difficulty-easy { border-left: 4px solid #28a745; }
    .difficulty-medium { border-left: 4px solid #ffc107; }
    .difficulty-hard { border-left: 4px solid #dc3545; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# SESSION STATE
# =============================================================================

def init_session():
    """Session state başlatır."""
    defaults = {
        "user": None,
        "page": "login",
        "curriculum": None,
        "current_day": 1,
        "daily_content": None,
        "quiz_questions": None,
        "quiz_answers": {},
        "quiz_submitted": False,
        "completed_days": [],
        # Seviye testi için
        "assessment_questions": None,
        "assessment_answers": {},
        "assessment_submitted": False,
        "user_level": None,
        "goal_input": None,
        # Günlük ilerleme takibi
        "day_quiz_completed": {}  # {day: quiz_score}
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def check_api_status():
    """API durumunu kontrol eder."""
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    return bool(gemini_key and "your_" not in gemini_key.lower())


# =============================================================================
# LOGIN / REGISTER
# =============================================================================

def render_login_page():
    """Giriş sayfası."""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<h1 class="main-header">🎓 AI Öğrenme Koçu</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center; color:#666">Kişiselleştirilmiş öğrenme yolculuğunuz</p>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Giriş Yap", "📝 Kayıt Ol"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("📧 Email")
                password = st.text_input("🔒 Şifre", type="password")
                submit = st.form_submit_button("Giriş Yap", use_container_width=True)
                
                if submit and email and password:
                    um = UserManager()
                    success, user = um.login(email, password)
                    if success:
                        st.session_state.user = user
                        
                        # Aktif müfredatı yükle
                        saved_data = um.load_curriculum(user.user_id)
                        if saved_data:
                            st.session_state.curriculum = saved_data.get("curriculum")
                            st.session_state.goal_input = saved_data.get("goal_input")
                            st.session_state.user_level = saved_data.get("user_level")
                            st.session_state.current_day = saved_data.get("current_day", 1)
                            st.session_state.completed_days = saved_data.get("completed_days", [])
                            st.session_state.day_quiz_completed = saved_data.get("day_quiz_completed", {})
                            st.session_state.curriculum_id = saved_data.get("id")
                            
                            st.session_state.page = "dashboard"
                        else:
                            st.session_state.page = "set_goal"
                        
                        st.rerun()
                    else:
                        st.error("❌ Email veya şifre hatalı!")
        
        with tab2:
            with st.form("register_form"):
                new_username = st.text_input("👤 Kullanıcı Adı")
                new_email = st.text_input("📧 Email", key="reg_email")
                new_password = st.text_input("🔒 Şifre", type="password", key="reg_pass")
                new_password2 = st.text_input("🔒 Şifre Tekrar", type="password")
                
                submit_reg = st.form_submit_button("Kayıt Ol", use_container_width=True)
                
                if submit_reg:
                    if new_password != new_password2:
                        st.error("❌ Şifreler eşleşmiyor!")
                    elif len(new_password) < 4:
                        st.error("❌ Şifre en az 4 karakter olmalı!")
                    elif new_username and new_email and new_password:
                        um = UserManager()
                        success, result = um.register(new_username, new_email, new_password)
                        if success:
                            st.success("✅ Kayıt başarılı! Giriş yapabilirsiniz.")
                        else:
                            st.error(f"❌ {result}")


# =============================================================================
# GOAL SETTING
# =============================================================================

def render_goal_setting():
    """Kullanıcı hedef belirler."""
    st.markdown('<h1 class="main-header">🎯 Öğrenme Hedefiniz</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Ne öğrenmek istiyorsunuz?")
        st.info("💡 Hedefinizi yazın, ardından seviyenizi belirleyelim!")
        
        with st.form("goal_form"):
            goal = st.text_area(
                "Hedefiniz",
                placeholder="Örnek:\n• Python programlama öğrenmek istiyorum\n• Web sitesi yapmayı öğrenmek istiyorum\n• Veri analizi öğrenmek istiyorum\n• İngilizce öğrenmek istiyorum",
                height=100
            )
            
            duration = st.selectbox("📅 Hedef Süre", [2, 4, 6, 8], index=1, format_func=lambda x: f"{x} Hafta")
            daily_time = st.slider("⏰ Günlük çalışma süresi (saat)", 0.5, 4.0, 1.0, 0.5)
            
            submit = st.form_submit_button("🎯 Seviye Testine Geç", use_container_width=True)
            
            if submit and goal:
                st.session_state.goal_input = {
                    "goal": goal,
                    "duration": duration,
                    "daily_time": daily_time
                }
                st.session_state.page = "level_test"
                st.session_state.assessment_questions = None
                st.session_state.assessment_answers = {}
                st.session_state.assessment_submitted = False
                st.rerun()
            elif submit:
                st.warning("⚠️ Lütfen hedefinizi yazın!")
        
        # Hızlı başlangıç seçeneği
        st.markdown("---")
        st.markdown("### 🚀 Veya Hızlı Başla")
        st.caption("Seviye testini atlayıp başlangıç seviyesinden başlayabilirsiniz.")
        
        if st.button("Seviye Testini Atla (Başlangıç)", use_container_width=True):
            if st.session_state.goal_input:
                st.session_state.user_level = {
                    "level": "beginner",
                    "level_tr": "Başlangıç",
                    "score": 0,
                    "recommended_start_day": 1,
                    "summary": "Başlangıç seviyesinden başlıyorsunuz."
                }
                st.session_state.page = "create_curriculum"
                st.rerun()
        
        # API durumu
        if check_api_status():
            st.success("✅ AI Aktif - Kişiselleştirilmiş içerik")
        else:
            st.warning("⚠️ AI Mock Mod - Şablon içerik")


# =============================================================================
# LEVEL TEST - Seviye Belirleme
# =============================================================================

def render_level_test():
    """Seviye belirleme testi."""
    goal_data = st.session_state.goal_input
    
    if not goal_data:
        st.session_state.page = "set_goal"
        st.rerun()
        return
    
    goal = goal_data["goal"]
    
    st.markdown('<h1 class="main-header">📊 Seviye Belirleme Testi</h1>', unsafe_allow_html=True)
    st.markdown(f"**Hedef:** {goal}")
    st.info("💡 Bu test mevcut bilgi seviyenizi belirlemek için tasarlanmıştır. Bilmediğiniz soruları tahmin etmeyin, boş bırakabilirsiniz.")
    
    # Soruları yükle
    if st.session_state.assessment_questions is None:
        with st.spinner("📝 Seviye testi hazırlanıyor..."):
            level_agent = get_level_assessment_agent()
            questions = level_agent.get_assessment_questions(goal, 10)
            st.session_state.assessment_questions = questions
    
    questions = st.session_state.assessment_questions
    
    if not questions:
        st.error("Sorular yüklenemedi.")
        if st.button("← Geri"):
            st.session_state.page = "set_goal"
            st.rerun()
        return
    
    st.markdown("---")
    
    if not st.session_state.assessment_submitted:
        # Test formu
        for i, q in enumerate(questions):
            q_id = q.get("id", i+1)
            question_text = q.get("question", f"Soru {i+1}")
            difficulty = q.get("difficulty", "medium")
            topic_area = q.get("topic_area", "")
            
            difficulty_label = {"easy": "🟢 Kolay", "medium": "🟡 Orta", "hard": "🔴 Zor"}.get(difficulty, "")
            
            st.markdown(f"""
            <div class="question-card difficulty-{difficulty}">
                <small style="color:#666">{difficulty_label} | {topic_area}</small>
                <h4>Soru {i+1}: {question_text}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            options = q.get("options", [])
            options_with_skip = ["-- Bilmiyorum / Atla --"] + options
            
            answer = st.radio(
                f"Cevabınız (Soru {i+1}):",
                options=options_with_skip,
                key=f"assess_{q_id}",
                label_visibility="collapsed"
            )
            
            if answer != "-- Bilmiyorum / Atla --":
                st.session_state.assessment_answers[q_id] = answer
            elif q_id in st.session_state.assessment_answers:
                del st.session_state.assessment_answers[q_id]
            
            st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("← Hedefi Değiştir", use_container_width=True):
                st.session_state.page = "set_goal"
                st.rerun()
        
        with col2:
            answered = len(st.session_state.assessment_answers)
            if st.button(f"✅ Testi Bitir ({answered}/{len(questions)} cevaplandı)", use_container_width=True, type="primary"):
                st.session_state.assessment_submitted = True
                st.rerun()
    
    else:
        # Sonuçları hesapla
        level_agent = get_level_assessment_agent()
        result = level_agent.calculate_level(st.session_state.assessment_answers, questions)
        st.session_state.user_level = result
        
        # Sonuçları göster
        level = result["level"]
        level_tr = result["level_tr"]
        score = result["score"]
        
        level_class = f"level-{level}"
        
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem;">
            <h2>🎯 Seviye Sonucunuz</h2>
            <div class="level-badge {level_class}" style="font-size: 1.5rem; padding: 0.5rem 1.5rem;">
                {level_tr} Seviye
            </div>
            <h3 style="margin-top: 1rem;">Genel Skor: %{score}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Detaylı sonuçlar
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🟢 Kolay Sorular", f"%{result.get('easy_score', 0)}")
        with col2:
            st.metric("🟡 Orta Sorular", f"%{result.get('medium_score', 0)}")
        with col3:
            st.metric("🔴 Zor Sorular", f"%{result.get('hard_score', 0)}")
        
        st.markdown("---")
        
        # Güçlü ve zayıf yönler
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("### ✅ Güçlü Yönleriniz")
            strengths = result.get("strengths", [])
            if strengths:
                for s in strengths:
                    st.success(f"• {s}")
            else:
                st.info("Henüz belirlenmedi")
        
        with col_b:
            st.markdown("### 📚 Geliştirilecek Alanlar")
            weaknesses = result.get("weaknesses", [])
            if weaknesses:
                for w in weaknesses:
                    st.warning(f"• {w}")
            else:
                st.info("Harika! Tüm alanlarda iyisiniz.")
        
        st.markdown("---")
        st.info(f"💡 {result.get('summary', '')}")
        
        # Müfredat oluştur butonu
        start_day = result.get("recommended_start_day", 1)
        
        st.markdown(f"### 📋 Önerilen Başlangıç: Gün {start_day}")
        
        if st.button("🚀 Müfredatımı Oluştur", use_container_width=True, type="primary"):
            st.session_state.page = "create_curriculum"
            st.rerun()


# =============================================================================
# CREATE CURRICULUM
# =============================================================================

def render_create_curriculum():
    """Müfredat oluşturur."""
    goal_data = st.session_state.goal_input
    level_data = st.session_state.user_level
    
    if not goal_data or not level_data:
        st.session_state.page = "set_goal"
        st.rerun()
        return
    
    st.markdown('<h1 class="main-header">🎓 Müfredat Oluşturuluyor</h1>', unsafe_allow_html=True)
    
    with st.spinner("🤖 AI müfredatınızı hazırlıyor... Bu birkaç saniye sürebilir."):
        # Curriculum Agent ile müfredat oluştur
        curriculum_agent = get_curriculum_agent()
        curriculum = curriculum_agent.generate_curriculum(
            goal_data["goal"],
            level_data["level"],
            goal_data["duration"]
        )
        
        # Ek bilgileri ekle
        curriculum["daily_time"] = goal_data["daily_time"]
        curriculum["level"] = level_data["level"]
        curriculum["level_tr"] = level_data["level_tr"]
        curriculum["user_score"] = level_data.get("score", 0)
        curriculum["start_day"] = level_data.get("recommended_start_day", 1)
        
        # Session'a kaydet
        st.session_state.curriculum = curriculum
        st.session_state.current_day = level_data.get("recommended_start_day", 1)
        st.session_state.completed_days = []
        
        # Kullanıcıya kaydet (veritabanına) - yeni müfredat olarak
        um = UserManager()
        user = st.session_state.user
        curriculum_id = um.save_curriculum(
            user.user_id,
            curriculum,
            goal_data,
            level_data,
            st.session_state.current_day,
            st.session_state.completed_days
        )
        
        st.session_state.curriculum_id = curriculum_id
        
        # User objesini güncelle
        user = um.get_user(user.user_id)
        st.session_state.user = user
    
    st.success("✅ Müfredat hazır!")
    st.session_state.page = "dashboard"
    st.rerun()


# =============================================================================
# DASHBOARD
# =============================================================================

def render_dashboard():
    """Ana dashboard."""
    user = st.session_state.user
    curriculum = st.session_state.curriculum
    
    if not curriculum:
        st.session_state.page = "set_goal"
        st.rerun()
        return
    
    um = UserManager()
    stats = um.get_user_stats(user.user_id)
    
    # Header
    st.markdown(f'<h1 class="main-header">📚 {curriculum.get("goal", "Öğrenme Yolculuğum")}</h1>', unsafe_allow_html=True)
    
    # Seviye badge
    level = curriculum.get("level", "beginner")
    level_tr = curriculum.get("level_tr", "Başlangıç")
    level_class = f"level-{level}"
    
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 1rem;">
        <span class="level-badge {level_class}">{level_tr} Seviye</span>
    </div>
    """, unsafe_allow_html=True)
    
    if curriculum.get("summary"):
        st.info(f"📋 {curriculum['summary']}")
    
    # İstatistikler
    total_days = len(curriculum.get("daily_lessons", []))
    completed = len(st.session_state.completed_days)
    current_day = st.session_state.current_day
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{current_day}</div>
            <div class="stat-label">Mevcut Gün</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{completed}/{total_days}</div>
            <div class="stat-label">Tamamlanan</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        progress = int((completed / total_days) * 100) if total_days > 0 else 0
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">%{progress}</div>
            <div class="stat-label">İlerleme</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">%{int(stats.get('average_quiz_score', 0))}</div>
            <div class="stat-label">Quiz Ort.</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # İki sütun
    col_left, col_right = st.columns([1, 2])
    
    with col_left:
        st.markdown("### 📋 Konu Haritası")
        
        # Tamamlanan ders sayısını göster
        if st.session_state.completed_days:
            st.success(f"✅ {len(st.session_state.completed_days)} ders tamamlandı")
        
        daily_lessons = curriculum.get("daily_lessons", [])
        
        # Scroll için container
        with st.container():
            for lesson in daily_lessons:
                day = lesson.get("day", 0)
                theme = lesson.get("theme", f"Gün {day}")
                
                # Quiz durumu
                quiz_score = st.session_state.day_quiz_completed.get(day, None)
                quiz_indicator = f" 📝%{quiz_score}" if quiz_score is not None else ""
                
                # Durum belirleme
                if day in st.session_state.completed_days:
                    icon = "✅"
                    status = "completed"
                elif day == current_day:
                    # Mevcut gün - quiz çözüldü mü kontrol et
                    if quiz_score is not None:
                        icon = "📝"  # Quiz tamamlandı
                    else:
                        icon = "▶️"
                    status = "current"
                elif day < current_day:
                    icon = "⏭️"
                    status = "available"
                else:
                    icon = "🔒"
                    status = "locked"
                
                # Buton metni
                btn_text = f"{icon} Gün {day}: {theme[:20]}{quiz_indicator}"
                
                # Buton stili
                if status == "current":
                    btn_type = "primary"
                elif status == "completed":
                    btn_type = "secondary"
                else:
                    btn_type = "secondary"
                
                # Tıklanabilir mi?
                is_accessible = (day <= current_day) or (day in st.session_state.completed_days)
                
                if is_accessible:
                    if st.button(btn_text, key=f"topic_{day}", use_container_width=True, type=btn_type if status == "current" else "secondary"):
                        st.session_state.current_day = day
                        st.session_state.daily_content = None
                        st.session_state.quiz_questions = None
                        st.rerun()
                else:
                    # Kilitli dersler
                    st.button(btn_text, key=f"topic_{day}", use_container_width=True, disabled=True)
    
    with col_right:
        render_current_day_content()


def render_current_day_content():
    """Mevcut günün içeriği."""
    curriculum = st.session_state.curriculum
    current_day = st.session_state.current_day
    
    daily_lessons = curriculum.get("daily_lessons", [])
    
    if current_day > len(daily_lessons):
        st.success("🎉 Tebrikler! Tüm müfredatı tamamladınız!")
        return
    
    lesson = daily_lessons[current_day - 1]
    
    st.markdown(f"## 📅 Gün {current_day}: {lesson.get('theme', 'Günün Konusu')}")
    
    # Gün durumu kontrolü
    is_day_completed = current_day in st.session_state.completed_days
    quiz_score = st.session_state.day_quiz_completed.get(current_day, None)
    
    # Durum göstergesi
    if is_day_completed:
        st.success(f"✅ Bu gün tamamlandı! Quiz Skoru: %{quiz_score if quiz_score else 'N/A'}")
    elif quiz_score is not None:
        st.info(f"📝 Quiz tamamlandı (%{quiz_score}). Günü tamamlayabilirsiniz!")
    else:
        st.warning("⚠️ Günü tamamlamak için önce dersi okuyun ve quiz'i çözün.")
    
    st.markdown("---")
    
    # Görevler
    st.markdown("### ✅ Yapılacaklar")
    
    tasks = lesson.get("tasks", [])
    for i, task in enumerate(tasks):
        task_type = task.get("type", "theory")
        type_icon = {"theory": "📖", "practice": "💻", "quiz": "📝"}.get(task_type, "📌")
        
        # Görev durumu
        task_status = ""
        if task_type == "quiz" and quiz_score is not None:
            task_status = f" <span style='color: green;'>✓ Tamamlandı (%{quiz_score})</span>"
        
        st.markdown(f"""
        <div class="task-item {task_type}">
            <strong>{type_icon} {task.get('task', 'Görev')}{task_status}</strong><br>
            <small style="color:#666">{task.get('description', '')}</small><br>
            <small>⏱️ {task.get('duration_min', 20)} dakika</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Kaynaklar
    resources = lesson.get("resources", [])
    if resources:
        st.markdown("### 📚 Kaynaklar")
        for res in resources:
            st.markdown(f"- [{res.get('title', 'Kaynak')}]({res.get('url', '#')})")
    
    if lesson.get("tip"):
        st.info(f"💡 {lesson['tip']}")
    
    st.markdown("---")
    
    # Öğrenme Akışı
    st.markdown("### 📖 Öğrenme Akışı")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**1️⃣ Ders**")
        if st.button("📚 Ders İçeriği", use_container_width=True, type="primary"):
            st.session_state.page = "lesson"
            st.session_state.daily_content = None
            st.rerun()
    
    with col2:
        st.markdown("**2️⃣ Quiz**")
        quiz_btn_text = "📝 Quiz Çöz" if quiz_score is None else f"🔄 Quiz Tekrarla (%{quiz_score})"
        if st.button(quiz_btn_text, use_container_width=True, type="primary" if quiz_score is None else "secondary"):
            st.session_state.page = "quiz"
            st.session_state.quiz_submitted = False
            st.session_state.quiz_answers = {}
            st.session_state.quiz_questions = None
            st.rerun()
    
    with col3:
        st.markdown("**3️⃣ Tamamla**")
        # Günü tamamla butonu - sadece quiz çözüldüyse aktif
        if quiz_score is not None and not is_day_completed:
            if st.button("✅ Günü Tamamla", use_container_width=True, type="primary"):
                complete_day()
                st.rerun()
        elif is_day_completed:
            st.button("✅ Tamamlandı", use_container_width=True, disabled=True)
        else:
            st.button("🔒 Önce Quiz Çöz", use_container_width=True, disabled=True)


def complete_day():
    """Günü tamamlar."""
    current_day = st.session_state.current_day
    
    if current_day not in st.session_state.completed_days:
        st.session_state.completed_days.append(current_day)
    
    um = UserManager()
    um.record_progress(st.session_state.user.user_id, f"day_{current_day}", 1.0)
    
    total_days = len(st.session_state.curriculum.get("daily_lessons", []))
    if current_day < total_days:
        st.session_state.current_day = current_day + 1
    
    # İlerlemeyi kaydet
    um.update_progress(
        st.session_state.user.user_id,
        st.session_state.current_day,
        st.session_state.completed_days,
        st.session_state.day_quiz_completed
    )
    
    st.success(f"🎉 Gün {current_day} tamamlandı!")


# =============================================================================
# LESSON PAGE
# =============================================================================

def render_lesson_page():
    """Ders içeriği sayfası."""
    curriculum = st.session_state.curriculum
    current_day = st.session_state.current_day
    
    daily_lessons = curriculum.get("daily_lessons", [])
    
    if current_day > len(daily_lessons):
        st.warning("Ders bulunamadı.")
        if st.button("← Geri"):
            st.session_state.page = "dashboard"
            st.rerun()
        return
    
    lesson = daily_lessons[current_day - 1]
    theme = lesson.get("theme", "Günün Dersi")
    
    st.markdown(f"## 📚 {theme}")
    
    # İçerik oluştur veya göster
    if st.session_state.daily_content is None:
        with st.spinner("📖 Ders içeriği hazırlanıyor..."):
            if lesson.get("learning_content"):
                content = lesson["learning_content"]
            elif lesson.get("content"):
                content = lesson["content"]
            else:
                content_agent = get_content_agent()
                goal = curriculum.get("goal", "")
                level = curriculum.get("level", "beginner")
                content = content_agent.generate_lesson_content(theme, level, goal)
            
            st.session_state.daily_content = content
    
    st.markdown("---")
    st.markdown(st.session_state.daily_content)
    
    st.markdown("---")
    
    # Quiz durumu kontrolü
    current_day = st.session_state.current_day
    quiz_score = st.session_state.day_quiz_completed.get(current_day, None)
    
    if quiz_score is not None:
        st.info(f"✅ Bu günün quiz'i tamamlandı (Skor: %{quiz_score}). İsterseniz tekrar çözebilirsiniz.")
    else:
        st.success("📝 Dersi okudunuz mu? Şimdi quiz'i çözme zamanı!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("← Dashboard", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()
    
    with col2:
        quiz_btn_text = "📝 Quiz'e Geç →" if quiz_score is None else "🔄 Quiz'i Tekrarla →"
        if st.button(quiz_btn_text, use_container_width=True, type="primary"):
            st.session_state.page = "quiz"
            st.session_state.quiz_submitted = False
            st.session_state.quiz_answers = {}
            st.session_state.quiz_questions = None
            st.rerun()


# =============================================================================
# QUIZ PAGE - AI Entegrasyonu
# =============================================================================

def render_quiz_page():
    """Quiz sayfası - AI'dan sorular gelir."""
    curriculum = st.session_state.curriculum
    current_day = st.session_state.current_day
    
    daily_lessons = curriculum.get("daily_lessons", [])
    
    if current_day > len(daily_lessons):
        st.warning("Quiz bulunamadı.")
        if st.button("← Geri"):
            st.session_state.page = "dashboard"
            st.rerun()
        return
    
    lesson = daily_lessons[current_day - 1]
    theme = lesson.get("theme", "Quiz")
    goal = curriculum.get("goal", "")
    level = curriculum.get("level", "beginner")
    
    st.markdown(f"## 📝 Quiz: {theme}")
    
    # Quiz sorularını al - HER ZAMAN AI'DAN YENİ SORULAR OLUŞTUR
    if st.session_state.quiz_questions is None:
        questions = None
        
        # ContentAgent'tan AI tabanlı sorular al
        try:
            content_agent = get_content_agent()
            with st.spinner("🤖 AI quiz soruları oluşturuyor..."):
                questions = content_agent.generate_quiz(theme, level, 5, goal)
            
            if questions and len(questions) > 0:
                # Fallback kontrolü
                first_q = questions[0]
                if first_q.get("is_fallback"):
                    st.warning("⚠️ AI servisi çalışmıyor. Lütfen GEMINI_API_KEY yapılandırın.")
                else:
                    st.success("✅ AI tarafından konuya özel sorular oluşturuldu!")
                    
        except Exception as e:
            st.error(f"❌ Quiz oluşturulurken hata: {e}")
            questions = None
        
        # Hala yoksa fallback sorular
        if not questions or len(questions) == 0:
            st.warning("⚠️ AI servisi kullanılamıyor, fallback sorular gösteriliyor.")
            questions = [
                {
                    "question_id": f"q{i+1}",
                    "question": f"{theme} hakkında soru {i+1}",
                    "options": ["Seçenek A", "Seçenek B", "Seçenek C", "Seçenek D"],
                    "correct_answer": "Seçenek A",
                    "topic": theme,
                    "is_fallback": True
                }
                for i in range(5)
            ]
        
        st.session_state.quiz_questions = questions
    
    questions = st.session_state.quiz_questions
    
    if not questions or len(questions) == 0:
        st.error("❌ Quiz soruları yüklenemedi.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Tekrar Dene", use_container_width=True):
                st.session_state.quiz_questions = None
                st.rerun()
        with col2:
            if st.button("← Dashboard", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()
        return
    
    st.markdown("---")
    
    if not st.session_state.quiz_submitted:
        # Quiz formu
        for i, q in enumerate(questions):
            q_id = q.get("question_id", q.get("id", i))
            question_text = q.get("question", f"Soru {i+1}")
            topic = q.get("topic", q.get("topic_area", ""))
            
            st.markdown(f"""
            <div class="question-card">
                <small style="color:#666">{topic}</small>
                <h4>Soru {i+1}: {question_text}</h4>
            </div>
            """, unsafe_allow_html=True)
            
            options = q.get("options", ["A", "B", "C", "D"])
            
            answer = st.radio(
                f"Cevabınız:",
                options=options,
                key=f"quiz_{i}",
                label_visibility="collapsed"
            )
            st.session_state.quiz_answers[i] = answer
            st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("← Dashboard", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()
        
        with col2:
            if st.button("✅ Cevapları Gönder", use_container_width=True, type="primary"):
                st.session_state.quiz_submitted = True
                st.rerun()
    
    else:
        # Sonuçlar
        correct_count = 0
        wrong_questions = []  # Yanlış soruları sakla
        
        for i, q in enumerate(questions):
            user_answer = st.session_state.quiz_answers.get(i, "")
            # Farklı formatlardaki doğru cevabı kontrol et
            correct_answer = q.get("correct_answer", q.get("correct", ""))
            
            is_correct = user_answer == correct_answer
            
            question_text = q.get("question", f"Soru {i+1}")
            topic = q.get("topic", theme)
            
            if is_correct:
                correct_count += 1
                st.success(f"✅ **Soru {i+1}:** {question_text}\n\n**Cevabınız:** {user_answer} ✓")
            else:
                wrong_questions.append({
                    "number": i+1,
                    "question": question_text,
                    "user_answer": user_answer,
                    "correct_answer": correct_answer,
                    "topic": topic
                })
                st.error(f"❌ **Soru {i+1}:** {question_text}\n\n**Cevabınız:** {user_answer}\n\n**Doğru cevap:** {correct_answer}")
        
        score = int((correct_count / len(questions)) * 100) if questions else 0
        
        # Quiz skorunu session'a kaydet
        st.session_state.day_quiz_completed[current_day] = score
        
        st.markdown("---")
        
        # Skor gösterimi
        if score >= 80:
            st.balloons()
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: #d4edda; border-radius: 12px;">
                <h2>🎉 Mükemmel!</h2>
                <h1 style="color: #155724;">%{score}</h1>
                <p>{correct_count}/{len(questions)} doğru</p>
            </div>
            """, unsafe_allow_html=True)
            st.success("✅ Artık günü tamamlayabilirsiniz!")
        elif score >= 60:
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: #fff3cd; border-radius: 12px;">
                <h2>👍 İyi!</h2>
                <h1 style="color: #856404;">%{score}</h1>
                <p>{correct_count}/{len(questions)} doğru</p>
            </div>
            """, unsafe_allow_html=True)
            st.info("✅ Quiz tamamlandı. Dashboard'dan günü tamamlayabilirsiniz.")
        else:
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: #f8d7da; border-radius: 12px;">
                <h2>📚 Tekrar Deneyin</h2>
                <h1 style="color: #721c24;">%{score}</h1>
                <p>{correct_count}/{len(questions)} doğru</p>
            </div>
            """, unsafe_allow_html=True)
            st.warning("⚠️ Daha iyi bir skor için dersi tekrar gözden geçirip quiz'i tekrarlayabilirsiniz.")
        
        # Yanlış sorular için AI açıklaması
        if wrong_questions and score < 100:
            st.markdown("---")
            st.markdown("### 📚 Yanlış Cevaplarınız İçin Açıklamalar")
            st.info("💡 AI, yanlış cevapladığınız soruları analiz ediyor ve size öğrenme önerileri sunuyor...")
            
            from tools.ai_service import get_ai_service
            ai_service = get_ai_service()
            
            for wrong_q in wrong_questions:
                with st.expander(f"❌ Soru {wrong_q['number']}: {wrong_q['question'][:50]}...", expanded=True):
                    st.markdown(f"**Soru:** {wrong_q['question']}")
                    st.markdown(f"**Sizin Cevabınız:** {wrong_q['user_answer']}")
                    st.markdown(f"**Doğru Cevap:** {wrong_q['correct_answer']}")
                    
                    # AI'dan açıklama al
                    with st.spinner("🤖 AI açıklama hazırlıyor..."):
                        explanation = ai_service.explain_wrong_answer(
                            question=wrong_q['question'],
                            user_answer=wrong_q['user_answer'],
                            correct_answer=wrong_q['correct_answer'],
                            topic=wrong_q['topic'],
                            level=level
                        )
                    
                    st.markdown("**💡 Açıklama:**")
                    st.success(explanation)
        
        # Skoru veritabanına kaydet
        um = UserManager()
        um.record_progress(st.session_state.user.user_id, f"quiz_day_{current_day}", 0.5, score)
        
        # İlerlemeyi kaydet
        um.update_progress(
            st.session_state.user.user_id,
            st.session_state.current_day,
            st.session_state.completed_days,
            st.session_state.day_quiz_completed
        )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Quiz'i Tekrarla", use_container_width=True):
                st.session_state.quiz_submitted = False
                st.session_state.quiz_answers = {}
                st.session_state.quiz_questions = None  # Yeni sorular
                st.rerun()
        
        with col2:
            if st.button("← Dashboard'a Dön", use_container_width=True, type="primary"):
                st.session_state.page = "dashboard"
                st.rerun()


# =============================================================================
# SIDEBAR
# =============================================================================

def render_sidebar():
    """Sidebar."""
    with st.sidebar:
        if st.session_state.user:
            user = st.session_state.user
            um = UserManager()
            
            st.markdown(f"### 👤 {user.username}")
            
            # Tüm müfredatları göster
            all_curriculums = um.get_all_curriculums(user.user_id)
            active_curriculums = [c for c in all_curriculums if c.get("status") == "active"]
            
            if len(active_curriculums) > 1:
                st.markdown("---")
                st.markdown("**📚 Müfredatlarım**")
                
                curriculum_options = {}
                for curr in active_curriculums:
                    goal = curr.get("goal_input", {}).get("goal", "Müfredat")[:30]
                    curr_id = curr.get("id")
                    curriculum_options[f"{goal}..."] = curr_id
                
                current_curriculum_id = st.session_state.get("curriculum_id", user.active_curriculum_id)
                current_label = None
                for label, cid in curriculum_options.items():
                    if cid == current_curriculum_id:
                        current_label = label
                        break
                
                selected = st.selectbox(
                    "Aktif Müfredat",
                    options=list(curriculum_options.keys()),
                    index=list(curriculum_options.keys()).index(current_label) if current_label else 0,
                    key="curriculum_selector"
                )
                
                if curriculum_options[selected] != current_curriculum_id:
                    # Müfredat değişti, yükle
                    um.set_active_curriculum(user.user_id, curriculum_options[selected])
                    st.session_state.curriculum_id = curriculum_options[selected]
                    st.rerun()
            
            # Seviye göster
            if st.session_state.curriculum:
                level_tr = st.session_state.curriculum.get("level_tr", "")
                level = st.session_state.curriculum.get("level", "beginner")
                if level_tr:
                    st.markdown(f'<span class="level-badge level-{level}">{level_tr}</span>', unsafe_allow_html=True)
                
                # İlerleme özeti
                total_days = len(st.session_state.curriculum.get("daily_lessons", []))
                completed = len(st.session_state.completed_days)
                current = st.session_state.current_day
                
                st.markdown("---")
                st.markdown("**📊 İlerleme**")
                st.progress(completed / total_days if total_days > 0 else 0)
                st.caption(f"Gün {current} / {total_days}")
                st.caption(f"✅ {completed} ders tamamlandı")
                
                # İstatistikler
                stats = um.get_user_stats(user.user_id)
                
                if stats.get("quiz_count", 0) > 0:
                    st.caption(f"📝 Quiz Ort: %{int(stats.get('average_quiz_score', 0))}")
                if stats.get("total_hours", 0) > 0:
                    st.caption(f"⏱️ Toplam: {stats.get('total_hours', 0)} saat")
            
            # API durumu
            st.markdown("---")
            if check_api_status():
                st.success("✅ AI Aktif")
            else:
                st.warning("⚠️ AI Mock")
            
            st.markdown("---")
            
            # Navigasyon
            if st.button("🏠 Dashboard", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()
            
            if st.button("📚 Ders", use_container_width=True):
                st.session_state.page = "lesson"
                st.session_state.daily_content = None
                st.rerun()
            
            if st.button("📝 Quiz", use_container_width=True):
                st.session_state.page = "quiz"
                st.session_state.quiz_submitted = False
                st.session_state.quiz_questions = None
                st.rerun()
            
            st.markdown("---")
            
            if st.button("🎯 Yeni Hedef Ekle", use_container_width=True):
                # Yeni müfredat oluştur - eskiler kaybolmaz
                st.session_state.curriculum = None
                st.session_state.goal_input = None
                st.session_state.user_level = None
                st.session_state.assessment_questions = None
                st.session_state.assessment_answers = {}
                st.session_state.assessment_submitted = False
                st.session_state.completed_days = []
                st.session_state.current_day = 1
                st.session_state.day_quiz_completed = {}
                st.session_state.page = "set_goal"
                st.rerun()
            
            if st.button("📊 Seviye Testi", use_container_width=True):
                if st.session_state.goal_input:
                    st.session_state.assessment_questions = None
                    st.session_state.assessment_answers = {}
                    st.session_state.assessment_submitted = False
                    st.session_state.page = "level_test"
                    st.rerun()
                else:
                    st.warning("Önce hedef belirleyin")
            
            if st.button("🚪 Çıkış", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Ana uygulama."""
    init_session()
    
    if st.session_state.user:
        render_sidebar()
    
    page = st.session_state.page
    user = st.session_state.user
    
    if page == "login" or not user:
        render_login_page()
    elif page == "set_goal":
        render_goal_setting()
    elif page == "level_test":
        render_level_test()
    elif page == "create_curriculum":
        render_create_curriculum()
    elif page == "dashboard":
        if not st.session_state.curriculum:
            render_goal_setting()
        else:
            render_dashboard()
    elif page == "lesson":
        render_lesson_page()
    elif page == "quiz":
        render_quiz_page()
    else:
        render_dashboard() if st.session_state.curriculum else render_goal_setting()


if __name__ == "__main__":
    main()
