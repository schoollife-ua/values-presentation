import streamlit as st
import qrcode
from io import BytesIO
from content import SLIDES, SCIENCE_SLIDE, QUOTES_SLIDE, ACTION_SLIDE, QR_SLIDE
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

.block-container { padding-top: 1.5rem !important; padding-bottom: 1rem !important; max-width: 1100px !important; }

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}

.slide-card {
    background: #1a1a1a;
    border: 1px solid #2a2a2a;
    border-radius: 20px;
    padding: 1.5rem 1.8rem;
    text-align: center;
    margin: 0.8rem 0;
    animation: fadeInUp 0.6s ease-out;
}
.slide-emoji { font-size: 2.5rem; margin-bottom: 0.5rem; animation: fadeInUp 0.8s ease-out; }
.slide-title { font-size: 1.6rem; font-weight: 800; color: #f0f0f0; margin-bottom: 0.3rem; animation: fadeInUp 0.7s ease-out; }
.slide-subtitle { font-size: 1rem; color: #888; margin-bottom: 1rem; font-weight: 600; animation: fadeInUp 0.8s ease-out; }
.slide-text { font-size: 0.95rem; color: #b0b0b0; line-height: 1.6; text-align: left; white-space: pre-line; animation: fadeInUp 0.9s ease-out; }
.progress-text { text-align: center; color: #666; font-size: 0.85rem; margin-bottom: 0.3rem; }
.question-text { font-size: 1.2rem; color: #f0f0f0; font-weight: 600; line-height: 1.4; text-align: center; }

div[data-testid="stProgress"] > div > div { background-color: #3a3a3a !important; }
.stProgress > div > div { background-color: #3a3a3a !important; }
div[role="progressbar"] { background-color: #3a3a3a !important; }
div[data-testid="stProgress"] > div > div > div { background-color: #ffffff !important; }
.stProgress > div > div > div { background-color: #ffffff !important; }
div[role="progressbar"] > div { background-color: #ffffff !important; }

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

.sci-table { width: 100%; border-collapse: collapse; margin-top: 0.6rem; font-size: 0.82rem; }
.sci-table th { background: #2a2a2a; color: #f0f0f0; padding: 0.45rem; text-align: left; border-bottom: 2px solid #3a3a3a; }
.sci-table td { padding: 0.45rem; color: #b0b0b0; border-bottom: 1px solid #2a2a2a; text-align: left; }
.sci-conclusion { margin-top: 0.8rem; padding: 0.7rem; background: #222; border-left: 3px solid #ffffff; color: #f0f0f0; font-style: italic; text-align: left; border-radius: 8px; font-size: 0.85rem; }

.quotes-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; margin-top: 0.6rem; }
.quote-block { background: #222; border-left: 3px solid #ffffff; border-radius: 10px; padding: 0.8rem 1rem; text-align: left; margin: 0; animation: fadeInUp 0.6s ease-out; }
.quote-text { color: #d0d0d0; font-size: 0.85rem; line-height: 1.45; font-style: italic; margin-bottom: 0.4rem; }
.quote-author { color: #f0f0f0; font-weight: 700; font-size: 0.85rem; }
.quote-role { color: #888; font-size: 0.75rem; }

.actions-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; margin-top: 0.8rem; }
.action-block { background: #222; border-radius: 12px; padding: 1rem 1.1rem; text-align: left; border: 1px solid #2a2a2a; animation: fadeInUp 0.6s ease-out; }
.action-emoji { font-size: 1.8rem; margin-bottom: 0.4rem; }
.action-title { color: #f0f0f0; font-weight: 700; font-size: 1rem; margin-bottom: 0.3rem; }
.action-text { color: #b0b0b0; font-size: 0.88rem; line-height: 1.5; }

.qr-box { display: flex; justify-content: center; margin: 1rem 0; }
.qr-message { background: #222; border-left: 3px solid #ffffff; border-radius: 10px; padding: 1rem 1.2rem; text-align: left; color: #d0d0d0; font-size: 0.95rem; line-height: 1.7; white-space: pre-line; }
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

# 6 обычных + наука + цитаты + действия + QR = 10 слайдов
TOTAL_SLIDES = len(SLIDES) + 4

# ===== СЛАЙДЫ =====
if st.session_state.stage == "slides":
    current = st.session_state.slide

    st.markdown(f'<p class="progress-text">Слайд {current + 1} з {TOTAL_SLIDES}</p>', unsafe_allow_html=True)
    st.progress((current + 1) / TOTAL_SLIDES)

    if current < len(SLIDES):
        slide = SLIDES[current]
        st.markdown(f'<div class="slide-card">'
                    f'<div class="slide-emoji">{slide["emoji"]}</div>'
                    f'<div class="slide-title">{slide["title"]}</div>'
                    f'<div class="slide-subtitle">{slide["subtitle"]}</div>'
                    f'<div class="slide-text">{slide["text"]}</div>'
                    f'</div>', unsafe_allow_html=True)

    elif current == len(SLIDES):
        sci = SCIENCE_SLIDE
        rows_html = "".join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in sci["rows"])
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

    elif current == len(SLIDES) + 1:
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
                    f'<div class="quotes-grid">{quotes_html}</div>'
                    f'</div>', unsafe_allow_html=True)

    elif current == len(SLIDES) + 2:
        a = ACTION_SLIDE
        items_html = "".join(
            f'<div class="action-block">'
            f'<div class="action-emoji">{emoji}</div>'
            f'<div class="action-title">{title}</div>'
            f'<div class="action-text">{text}</div>'
            f'</div>'
            for emoji, title, text in a["items"]
        )
        st.markdown(f'<div class="slide-card">'
                    f'<div class="slide-emoji">{a["emoji"]}</div>'
                    f'<div class="slide-title">{a["title"]}</div>'
                    f'<div class="slide-subtitle">{a["subtitle"]}</div>'
                    f'<div class="actions-grid">{items_html}</div>'
                    f'</div>', unsafe_allow_html=True)

    else:
        qr = QR_SLIDE
        img = qrcode.make(qr["message"])
        buf = BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        st.markdown(f'<div class="slide-card">'
                    f'<div class="slide-emoji">{qr["emoji"]}</div>'
                    f'<div class="slide-title">{qr["title"]}</div>'
                    f'<div class="slide-subtitle">{qr["subtitle"]}</div>'
                    f'<div class="qr-box">', unsafe_allow_html=True)
        st.image(buf, width=220)
        st.markdown(f'<div class="qr-message">{qr["message"]}</div>'
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
