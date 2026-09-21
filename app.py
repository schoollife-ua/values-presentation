import streamlit as st
from content import SLIDES
from questions import QUESTIONS, SCORES, RESULTS

st.set_page_config(
    page_title="Що формує наші цінності?",
    page_icon="🎯",
    layout="centered",
)

st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp { background: #0a0a0a; }

.slide-card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 24px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin: 1.5rem 0;
}
.slide-emoji { font-size: 3.5rem; margin-bottom: 1rem; }
.slide-title { font-size: 2rem; font-weight: 800; color: #f0f0f0; margin-bottom: 0.5rem; }
.slide-subtitle { font-size: 1.1rem; color: #888; margin-bottom: 1.5rem; font-weight: 600; }
.slide-text { font-size: 1rem; color: #b0b0b0; line-height: 1.8; text-align: left; white-space: pre-line; }

.progress-text { text-align: center; color: #666; font-size: 0.9rem; margin-bottom: 0.5rem; }
.question-text { font-size: 1.3rem; color: #f0f0f0; font-weight: 600; line-height: 1.5; text-align: center; }
</style>
""", unsafe_allow_html=True)

if "stage" not in st.session_state:
    st.session_state.stage = "slides"
if "slide" not in st.session_state:
    st.session_state.slide = 0
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_class" not in st.session_state:
    st.session_state.user_class = ""

# ===== СЛАЙДЫ =====
if st.session_state.stage == "slides":
    total = len(SLIDES)
    current = st.session_state.slide
    slide = SLIDES[current]

    st.markdown(f'<p class="progress-text">Слайд {current + 1} з {total}</p>', unsafe_allow_html=True)
    st.progress((current + 1) / total)

    st.markdown(f'<div class="slide-card">'
                f'<div class="slide-emoji">{slide["emoji"]}</div>'
                f'<div class="slide-title">{slide["title"]}</div>'
                f'<div class="slide-subtitle">{slide["subtitle"]}</div>'
                f'<div class="slide-text">{slide["text"]}</div>'
                f'</div>', unsafe_allow_html=True)

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
            if st.button("🚀 Почати тест", use_container_width=True, type="primary"):
                st.session_state.stage = "register"
                st.rerun()

# ===== РЕЄСТРАЦІЯ =====
elif st.session_state.stage == "register":
    st.markdown('<p class="progress-text">Крок 1 з 2 — Знайомство</p>', unsafe_allow_html=True)
    st.progress(0.5)
    st.markdown('<div class="slide-card">'
                '<div class="slide-emoji">📝</div>'
                '<div class="slide-title">Як тебе звати?</div>'
                '<div class="slide-subtitle">Це потрібно, щоб показати твій результат</div>'
                '</div>', unsafe_allow_html=True)

    name = st.text_input("Твоє ім'я", value=st.session_state.user_name, placeholder="Наприклад: Марія")
    klass = st.text_input("Клас", value=st.session_state.user_class, placeholder="Наприклад: 10-А")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Назад", use_container_width=True):
            st.session_state.stage = "slides"
            st.rerun()
    with col2:
        if st.button("Почати тест →", use_container_width=True, type="primary"):
            if name.strip() == "":
                st.warning("Введи своє ім'я")
            else:
                st.session_state.user_name = name.strip()
                st.session_state.user_class = klass.strip() if klass.strip() else "—"
                st.session_state.stage = "quiz"
                st.session_state.q_index = 0
                st.session_state.answers = []
                st.rerun()

# ===== ТЕСТ =====
elif st.session_state.stage == "quiz":
    total_q = len(QUESTIONS)
    q_index = st.session_state.q_index
    question = QUESTIONS[q_index]

    st.markdown(f'<p class="progress-text">Питання {q_index + 1} з {total_q}</p>', unsafe_allow_html=True)
    st.progress((q_index + 1) / total_q)
    st.markdown(f'<div class="slide-card"><div class="question-text">{question["text"]}</div></div>', unsafe_allow_html=True)

    for i, option in enumerate(question["options"]):
        if st.button(option, use_container_width=True, key=f"q{q_index}_o{i}"):
            st.session_state.answers.append({"category": question["category"], "score": SCORES[i]})
            st.session_state.q_index += 1
            if st.session_state.q_index >= total_q:
                st.session_state.stage = "result"
            st.rerun()

    if q_index > 0:
        if st.button("← Попереднє питання"):
            st.session_state.q_index -= 1
            st.session_state.answers.pop()
            st.rerun()

# ===== РЕЗУЛЬТАТ =====
elif st.session_state.stage == "result":
    totals = {"family": 0, "friends": 0, "school": 0, "society": 0}
    for ans in st.session_state.answers:
        totals[ans["category"]] += ans["score"]

    winner = max(totals, key=totals.get)
    result = RESULTS[winner]
    grand_total = sum(totals.values()) or 1
    percents = {k: round(v / grand_total * 100) for k, v in totals.items()}

    st.markdown(f'<div class="slide-card">'
                f'<div class="slide-emoji">{result["emoji"]}</div>'
                f'<div class="slide-title">{st.session_state.user_name}, твій результат:</div>'
                f'<div class="slide-subtitle">Тебе найбільше формують: {result["title"]}</div>'
                f'<div class="slide-text">{result["description"]}</div>'
                f'</div>', unsafe_allow_html=True)

    st.markdown("### 📊 Твій розподіл")
    for key, label in [("family", "👨‍👩‍👧 Сім'я"), ("friends", "🧑‍🤝‍🧑 Друзі"), ("school", "🏫 Школа"), ("society", "🌍 Суспільство")]:
        st.markdown(f"**{label} — {percents[key]}%**")
        st.progress(percents[key] / 100)

    st.markdown("---")
    if st.button("🔄 Пройти ще раз", use_container_width=True, type="primary"):
        st.session_state.stage = "slides"
        st.session_state.slide = 0
        st.session_state.q_index = 0
        st.session_state.answers = []
        st.session_state.user_name = ""
        st.session_state.user_class = ""
        st.rerun()
