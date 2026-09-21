import streamlit as st
from content import SLIDES

# --- Настройки страницы ---
st.set_page_config(
    page_title="Що формує наші цінності?",
    page_icon="🎯",
    layout="centered",
)

# --- Кастомный CSS ---
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
}

.slide-card {
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 3rem 2.5rem;
    backdrop-filter: blur(12px);
    text-align: center;
    margin-top: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
}

.slide-emoji {
    font-size: 4rem;
    margin-bottom: 1rem;
}

.slide-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.5rem;
    line-height: 1.2;
}

.slide-subtitle {
    font-size: 1.2rem;
    color: #A78BFA;
    margin-bottom: 1.5rem;
    font-weight: 600;
}

.slide-text {
    font-size: 1.05rem;
    color: #D1D5DB;
    line-height: 1.7;
    max-width: 600px;
    margin: 0 auto;
}

.progress-text {
    text-align: center;
    color: #9CA3AF;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# --- Состояние ---
if "slide" not in st.session_state:
    st.session_state.slide = 0

total = len(SLIDES)
current = st.session_state.slide
slide = SLIDES[current]

# --- Прогресс ---
st.markdown(f'<p class="progress-text">Слайд {current + 1} з {total}</p>', unsafe_allow_html=True)
st.progress((current + 1) / total)

# --- Карточка слайда ---
st.markdown(f"""
<div class="slide-card">
    <div class="slide-emoji">{slide['emoji']}</div>
    <div class="slide-title">{slide['title']}</div>
    <div class="slide-subtitle">{slide['subtitle']}</div>
    <div class="slide-text">{slide['text']}</div>
</div>
""", unsafe_allow_html=True)

# --- Навигация ---
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if current > 0:
        if st.button("← Назад", use_container_width=True):
            st.session_state.slide -= 1
            st.rerun()

with col3:
    if current < total - 1:
        if st.button("Далі →", use_container_width=True):
            st.session_state.slide += 1
            st.rerun()
    else:
        if st.button("🚀 Пройти тест", use_container_width=True, type="primary"):
            st.info("Тест з'явиться на наступному етапі 🚧")