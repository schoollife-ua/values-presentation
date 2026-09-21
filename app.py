import streamlit as st
from content import SLIDES, SCIENCE_SLIDE, QUOTES_SLIDE
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

/* Прогресс-бар */
div[data-testid="stProgress"] > div > div { background-color: #3a3a3a !important; }
.stProgress > div > div { background-color: #3a3a3a !important; }
div[role="progressbar"] { background-color: #3a3a3a !important; }
div[data-testid="stProgress"] > div > div > div { background-color: #ffffff !important; }
.stProgress > div > div > div { background-color: #ffffff !important; }
div[role="progressbar"] > div { background-color: #ffffff !important; }

/* Кнопки */
.stButton > button,
div[data-testid="stButton"] > button {
    background-color: #ffffff !important;
    color: #0a0a0a !important;
    border: 1px solid #ffffff !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}
.stButton > button:hover,
div[data-testid="stButton"] > button:hover {
    background-color: #d0d0d0 !important;
    color: #0a0a0a !important;
    border-color: #d0d0d0 !important;
}
.stButton > button:focus,
div[data-testid="stButton"] > button:focus {
    background-color: #ffffff !important;
    color: #0a0a0a !important;
    box-shadow: none !important;
}

/* Таблица науки */
.sci-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
    font-size: 0.9rem;
}
.sci-table th {
    background: #2a2a2a;
    color: #f0f0f0;
    padding: 0.6rem;
    text-align: left;
    border-bottom: 2px solid #3a3a3a;
}
.sci-table td {
    padding: 0.6rem;
    color: #b0b0b0;
    border-bottom: 1px solid #2a2a2a;
    text-align: left;
}
.sci-table tr:hover td { background: #222; }
.sci-conclusion {
    margin-top: 1.5rem;
    padding: 1rem;
    background: #222;
    border-left: 3px solid #ffffff;
    color: #f0f0f0;
    font-style: italic;
    text-align: left;
    border-radius: 8px;
}

/* Цитаты */
.quote-block {
    background: #222;
    border-left: 3px solid #ffffff;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin: 1rem 0;
    text-align: left;
}
.quote-text { color: #d0d0d0; font-size: 1rem; line-height: 1.6; font-style: italic; margin-bottom: 0.6rem; }
.quote-author { color: #f0f0f0; font-weight: 700; font-size: 0.95rem; }
.quote-role { color: #888; font-size: 0.85rem; }
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

# Общее число слайдов: 6 обычных + наука + цитаты = 8
TOTAL_SLIDES = len(SLIDES) + 2

# ===== СЛАЙДЫ =====
if st.session_state.stage == "slides":
    current = st.session_state.slide

    st.markdown(f'<p class="progress-text">Слайд {current + 1} з {TOTAL_SLIDES}</p>', unsafe_allow_html=True)
    st.progress((current + 1) / TOTAL_SLIDES)

    # Слайды 0..5 — обычные
    if current < len(SLIDES):
        slide = SLIDES[current]
        st.markdown(f'<div class="slide-card">'
                    f'<div class="slide-emoji">{slide["emoji"]}</div>'
                    f'<div class="slide-title">{slide["title"]}</div>'
                    f'<div class="slide-subtitle">{slide["subtitle"]}</div>'
                    f'<div class="slide-text">{slide["text"]}</div>'
                    f'</div>', unsafe_allow_html=True)

    # Слайд 6 — наука
    elif current == len(SLIDES):
        sci = SCIENCE_SLIDE
        rows_html = "".join(
            f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>'
            for a, b, c in sci["rows"]
        )
        st.markdown(f'<div class="slide-card">'
                    f'<div class="slide-emoji">{sci["emoji"]}</div>'
                    f'<div class="slide-title">{sci["title"]}</div>'
                    f'<div class="slide-subtitle">{sci["subtitle"]}</div>'
                    f'<table class="sci-table">'
                    f'<tr><th>Джерело</th><th>Вік</th><th>Що відбувається</th></tr>'
                    f'{rows_html}'
                    f'</table>'
                    f'<div class="sci-conclusion">💡 {sci["conclusion"]}</div>'
                    f'</div>', unsafe_allow_html=True)

    # Слайд 7 — цитаты
    else:
        q = QUOTES_SLIDE
        quotes_html = "".join(
            f'<div class="quote-block">'
            f'<div class="quote-text">«{text}»</div>'
            f'<div class="quote-author">{author}</div>'
            f'<div class="quote-role">{role}</div>'
            f'</div>'
            for author, role, text in q["quotes"]
        )
        st.markdown(f'<div class="slide-card">'
                    f'<div class="slide-emoji">{q["emoji"]}</div>'
                    f'<div class="slide-title">{q["title"]}</div>'
                    f'<div class="slide-subtitle">{q["subtitle"]}</div>'
                    f'{quotes_html}'
                    f'</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if current > 0:
            if st.button("← Назад", use_container_width=True):
                st.session_state.slide -= 1
                st.rerun()
    with col3:
        if current < TOTAL_SLIDES - 1:
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
