"""
🎓 AI Öğrenme Koçu - Web Arayüzü
================================
Streamlit ile oluşturulmuş interaktif web arayüzü.

Çalıştırmak için: streamlit run app.py
"""

import streamlit as st
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

from agents.orchestrator_agent import OrchestratorAgent
from tools.google_search import GoogleSearchTool
from tools.ai_service import AIService, get_ai_service
from tools.quiz_scoring import QuizScorer, QuizQuestion
from memory.memory_bank import MemoryBank

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
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .status-box {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .status-success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
    }
    .status-warning {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
    }
    .task-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .quiz-option {
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
        border-radius: 5px;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)


def check_api_status():
    """API durumlarını kontrol eder."""
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    gemini_ok = bool(gemini_key and "your_" not in gemini_key.lower())
    
    search_key = os.getenv("GOOGLE_SEARCH_API_KEY", "")
    search_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID", "")
    search_ok = bool(search_key and search_id)
    
    return {
        "gemini": gemini_ok,
        "search": search_ok,
        "gemini_key": gemini_key[:20] + "..." if gemini_ok else None
    }


def init_session_state():
    """Session state'i başlatır."""
    if "profile" not in st.session_state:
        st.session_state.profile = None
    if "plan" not in st.session_state:
        st.session_state.plan = None
    if "day" not in st.session_state:
        st.session_state.day = 1
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False
    if "evaluation" not in st.session_state:
        st.session_state.evaluation = None


def render_sidebar():
    """Sidebar'ı render eder."""
    with st.sidebar:
        st.markdown("## ⚙️ API Durumu")
        
        status = check_api_status()
        
        if status["gemini"]:
            st.success("✅ Gemini API: Aktif")
            st.caption(f"Key: {status['gemini_key']}")
        else:
            st.warning("⚠️ Gemini API: Mock Mod")
            st.caption("Gerçek AI için .env dosyasına GEMINI_API_KEY ekleyin")
        
        if status["search"]:
            st.success("✅ Google Search: Aktif")
        else:
            st.info("ℹ️ Google Search: Mock Mod")
        
        st.markdown("---")
        
        st.markdown("## 📊 Oturum Bilgisi")
        if st.session_state.profile:
            st.write(f"**Hedef:** {st.session_state.profile.get('goal', '-')}")
            st.write(f"**Seviye:** {st.session_state.profile.get('level', '-')}")
            st.write(f"**Gün:** {st.session_state.day}")
        else:
            st.caption("Henüz profil oluşturulmadı")
        
        st.markdown("---")
        
        if st.button("🔄 Sıfırla", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        return status


def render_profile_form():
    """Profil oluşturma formunu render eder."""
    st.markdown("## 👤 Profil Oluştur")
    
    col1, col2 = st.columns(2)
    
    with col1:
        goal = st.text_input(
            "🎯 Öğrenme Hedefiniz",
            placeholder="Örn: Python programlama öğrenmek",
            value="Python programlama öğrenmek"
        )
        
        level = st.selectbox(
            "📊 Mevcut Seviyeniz",
            options=["başlangıç", "orta", "ileri"],
            index=0
        )
    
    with col2:
        daily_time = st.slider(
            "⏰ Günlük Çalışma Süresi (saat)",
            min_value=0.5,
            max_value=4.0,
            value=1.0,
            step=0.5
        )
        
        style = st.selectbox(
            "📚 Öğrenme Stili",
            options=["teori + uygulama", "teori ağırlıklı", "pratik ağırlıklı"],
            index=0
        )
    
    if st.button("🚀 Planımı Oluştur", type="primary", use_container_width=True):
        with st.spinner("Plan oluşturuluyor..."):
            user_input = {
                "goal": goal,
                "current_level": level,
                "daily_available_time": daily_time,
                "preferred_learning_style": style
            }
            
            memory = MemoryBank()
            search_tool = GoogleSearchTool()
            orchestrator = OrchestratorAgent(search_tool=search_tool, memory_service=memory)
            
            result = orchestrator.run_initial_flow(user_input)
            
            st.session_state.profile = result["profile"]
            st.session_state.plan = result["plan"]
            st.session_state.resources = result.get("resources", [])
            st.session_state.orchestrator = orchestrator
            st.session_state.memory = memory
            
            st.rerun()


def render_daily_plan():
    """Günlük planı render eder."""
    plan = st.session_state.plan
    
    st.markdown(f"## 📅 {plan.get('theme', f'Gün {st.session_state.day}')}")
    
    # Metrikler
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="📆 Gün",
            value=st.session_state.day
        )
    
    with col2:
        total_min = plan.get("total_duration_min", 60)
        st.metric(
            label="⏱️ Toplam Süre",
            value=f"{total_min} dk"
        )
    
    with col3:
        task_count = len(plan.get("tasks", []))
        st.metric(
            label="📋 Görev Sayısı",
            value=task_count
        )
    
    st.markdown("---")
    
    # Görevler
    st.markdown("### 📋 Günün Görevleri")
    
    tasks = plan.get("tasks", [])
    completed_tasks = []
    
    for i, task in enumerate(tasks):
        col1, col2, col3 = st.columns([0.1, 0.6, 0.3])
        
        with col1:
            is_done = st.checkbox("", key=f"task_{i}", label_visibility="collapsed")
            if is_done:
                completed_tasks.append(i)
        
        with col2:
            task_type_emoji = {"theory": "📖", "quiz": "📝", "practice": "💻"}.get(task.get("type", ""), "📌")
            st.markdown(f"**{task_type_emoji} {task.get('task', 'Görev')}**")
            st.caption(task.get("description", ""))
        
        with col3:
            st.write(f"⏱️ {task.get('duration_min', 0)} dk")
    
    st.session_state.completed_tasks = len(completed_tasks)
    
    # İpucu
    if plan.get("tips"):
        st.info(f"💡 **İpucu:** {plan.get('tips')}")
    
    # Kaynaklar
    st.markdown("### 📚 Önerilen Kaynaklar")
    
    resources = plan.get("resources", [])[:3]
    
    for res in resources:
        with st.expander(f"🔗 {res.get('title', 'Kaynak')}"):
            st.write(f"**URL:** {res.get('url', '#')}")
            if res.get("snippet"):
                st.write(res.get("snippet"))
            st.caption(f"Kaynak tipi: {res.get('resource_type', 'website')} | Mod: {res.get('source', 'unknown')}")


def render_quiz():
    """Quiz bölümünü render eder."""
    st.markdown("### 📝 Mini Quiz")
    
    quiz_scorer = QuizScorer()
    domain = st.session_state.profile.get("domain", "python")
    
    # Quiz sorularını oluştur (sadece bir kez)
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = quiz_scorer.generate_sample_quiz(domain, 3)
    
    questions = st.session_state.quiz_questions
    
    if not st.session_state.quiz_submitted:
        for i, q in enumerate(questions):
            st.markdown(f"**Soru {i+1}:** {q.question}")
            
            answer = st.radio(
                f"Cevabınız:",
                options=q.options,
                key=f"quiz_q_{i}",
                label_visibility="collapsed"
            )
            st.session_state.quiz_answers[q.question_id] = answer
            st.markdown("---")
        
        if st.button("✅ Quiz'i Tamamla", type="primary"):
            st.session_state.quiz_submitted = True
            st.rerun()
    
    else:
        # Sonuçları göster
        key_answers = {q.question_id: q.correct_answer for q in questions}
        score = quiz_scorer.score_quiz(st.session_state.quiz_answers, key_answers)
        
        st.session_state.quiz_score = score
        
        if score >= 80:
            st.success(f"🌟 Harika! Puanınız: %{score}")
        elif score >= 50:
            st.warning(f"👍 İyi! Puanınız: %{score}")
        else:
            st.error(f"📚 Tekrar gerekli. Puanınız: %{score}")
        
        # Doğru cevapları göster
        with st.expander("📋 Cevap Anahtarı"):
            for q in questions:
                user_ans = st.session_state.quiz_answers.get(q.question_id, "")
                correct = q.correct_answer
                is_correct = user_ans == correct
                
                icon = "✅" if is_correct else "❌"
                st.write(f"{icon} **{q.question}**")
                st.write(f"   Sizin cevabınız: {user_ans}")
                if not is_correct:
                    st.write(f"   Doğru cevap: {correct}")


def render_evaluation():
    """Gün sonu değerlendirmesini render eder."""
    st.markdown("### 📊 Gün Sonu Değerlendirmesi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        completed = st.number_input(
            "Tamamlanan görev sayısı",
            min_value=0,
            max_value=5,
            value=st.session_state.get("completed_tasks", 0)
        )
    
    with col2:
        difficulty = st.slider(
            "Algılanan zorluk (1-5)",
            min_value=1,
            max_value=5,
            value=3
        )
    
    quiz_score = st.session_state.get("quiz_score", 0)
    st.write(f"📝 Quiz Puanı: %{quiz_score}")
    
    if st.button("📈 Değerlendir ve Sonraki Güne Geç", type="primary", use_container_width=True):
        with st.spinner("Değerlendirme yapılıyor..."):
            day_report = {
                "day": st.session_state.day,
                "completed_tasks": completed,
                "perceived_difficulty": difficulty,
                "quiz_score": quiz_score
            }
            
            orchestrator = st.session_state.get("orchestrator")
            if orchestrator:
                result = orchestrator.run_daily_cycle(
                    user_id="web_user",
                    day_report=day_report
                )
                
                st.session_state.evaluation = result["evaluation"]
                st.session_state.plan = result["next_plan"]
                st.session_state.day += 1
                st.session_state.quiz_submitted = False
                st.session_state.quiz_answers = {}
                if "quiz_questions" in st.session_state:
                    del st.session_state["quiz_questions"]
                
                st.rerun()


def render_evaluation_results():
    """Değerlendirme sonuçlarını gösterir."""
    if st.session_state.evaluation:
        eval_data = st.session_state.evaluation
        
        st.markdown("### ✅ Son Değerlendirme")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="📊 Günlük Puan",
                value=eval_data.get("daily_score", 0)
            )
        
        with col2:
            level = eval_data.get("performance_level", "average")
            level_emoji = {
                "excellent": "🌟",
                "good": "👍",
                "average": "📊",
                "needs_improvement": "📚"
            }.get(level, "📊")
            st.metric(
                label="📈 Performans",
                value=f"{level_emoji} {level}"
            )
        
        suggestions = eval_data.get("suggestions", [])
        if suggestions:
            st.markdown("**💡 Öneriler:**")
            for s in suggestions:
                st.write(f"• {s}")


def render_ai_assistant():
    """AI asistan bölümünü render eder."""
    st.markdown("### 🤖 AI Asistan")
    
    status = check_api_status()
    
    if not status["gemini"]:
        st.warning("⚠️ AI Asistan için .env dosyasına GEMINI_API_KEY ekleyin")
        return
    
    topic = st.text_input(
        "Bir konu sorun:",
        placeholder="Örn: Python'da listeler nasıl çalışır?"
    )
    
    if st.button("🔍 Açıkla") and topic:
        with st.spinner("AI düşünüyor..."):
            ai_service = get_ai_service()
            level = st.session_state.profile.get("level", "beginner") if st.session_state.profile else "beginner"
            explanation = ai_service.explain_topic(topic, level)
            
            st.markdown("**📚 Açıklama:**")
            st.write(explanation)


def main():
    """Ana uygulama."""
    init_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🎓 AI Öğrenme Koçu</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666;">Kişiselleştirilmiş öğrenme deneyiminiz</p>', unsafe_allow_html=True)
    
    # Sidebar
    status = render_sidebar()
    
    # Ana içerik
    if st.session_state.profile is None:
        render_profile_form()
    else:
        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📅 Günlük Plan", "📝 Quiz", "📊 Değerlendirme", "🤖 AI Asistan"])
        
        with tab1:
            render_daily_plan()
        
        with tab2:
            render_quiz()
        
        with tab3:
            render_evaluation_results()
            st.markdown("---")
            render_evaluation()
        
        with tab4:
            render_ai_assistant()


if __name__ == "__main__":
    main()

