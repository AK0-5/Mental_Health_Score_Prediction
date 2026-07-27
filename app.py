import streamlit as st
import requests
import plotly.graph_objects as go

st.set_page_config(page_title="Student Wellbeing Lab", page_icon="✦", layout="wide")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
DEFAULT_API_URL = "https://mental-health-score-prediction-0wql.onrender.com"

PLATFORMS = ['Instagram', 'Facebook', 'LinkedIn', 'Snapchat', 'Twitter',
             'YouTube', 'TikTok', 'LINE', 'KakaoTalk', 'VKontakte', 'WhatsApp', 'WeChat']

PURPOSES = ['Entertainment', 'Networking', 'Education', 'News']

ACADEMIC_LEVELS = ['Undergraduate', 'Graduate', 'High School']

STRESS_LEVELS = ['Low', 'Medium', 'High', 'Very High']

SCORE_MIN, SCORE_MAX = 0, 10

if "score" not in st.session_state:
    st.session_state.score = None
if "error" not in st.session_state:
    st.session_state.error = None

# ---------------------------------------------------------------------------
# Styling
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital@0;1&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Top badge row */
.mh-badge-row { display:flex; align-items:center; gap:0.5rem; margin-bottom: 0.8rem; }
.mh-dot { width:8px; height:8px; border-radius:50%; background:#ec6f9b; display:inline-block; }
.mh-badge-text { text-transform:uppercase; letter-spacing:2px; font-size:0.72rem; color:#9a9cb5; font-weight:600; }

/* Header */
.mh-title { font-family:'Playfair Display', serif; font-size:2.5rem; line-height:1.15; color:#eceafb; margin:0; }
.mh-title em { font-style:italic; color:#a78bfa; }
.mh-subtitle { color:#9a9cb5; font-size:0.95rem; margin-top:0.8rem; margin-bottom:1.8rem; max-width:640px; }

/* Card containers */
div.st-key-left_card, div.st-key-right_panel {
    background:#151830;
    border-radius:18px;
    padding:1.8rem 2rem;
    border:1px solid #262a4a;
}

/* Section labels */
.mh-section-label {
    text-transform:uppercase; letter-spacing:1.5px; font-size:0.72rem;
    color:#7d7fa0; font-weight:600; margin:1.2rem 0 0.7rem 0;
}
.mh-section-label:first-child { margin-top:0; }
hr.mh-divider { border:none; border-top:1px solid #262a4a; margin:1.1rem 0; }

/* Inputs */
div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-baseweb="select"] > div {
    border-radius:10px !important;
    border:1px solid #2c2f52 !important;
    background-color:#0f1224 !important;
    color:#e6e5f2 !important;
}
div[data-testid="stNumberInput"] button { display:none !important; }

/* Labels always visible */
[data-testid="stWidgetLabel"] p { color:#c7c8de !important; font-size:0.85rem; }

/* Slider value bubble + track use theme primaryColor automatically */

/* Submit button - not full width, pill shaped */
.stFormSubmitButton button {
    background:#8b7cf6 !important; color:#100f1e !important;
    border:none !important; border-radius:999px !important;
    padding:0.55rem 1.6rem !important; font-weight:600 !important;
}
.stFormSubmitButton button:hover { background:#a294ff !important; }

/* Right panel text */
.mh-score-big { text-align:center; font-family:'Playfair Display', serif; font-size:3rem; color:#a78bfa; margin:0.4rem 0 0; }
.mh-score-outof { text-align:center; text-transform:uppercase; letter-spacing:1.5px; font-size:0.7rem; color:#7d7fa0; margin-bottom:0.9rem; }
.mh-pill { display:block; width:fit-content; margin:0 auto 1rem auto; background:rgba(139,124,246,0.15);
    color:#c9bfff; border:1px solid rgba(139,124,246,0.4); border-radius:999px; padding:0.3rem 1rem;
    font-size:0.75rem; letter-spacing:1px; text-transform:uppercase; font-weight:600; }
.mh-panel-caption { text-align:center; color:#9a9cb5; font-size:0.85rem; line-height:1.4; margin-top:0.3rem; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
st.markdown(
    '<div class="mh-badge-row"><span class="mh-dot"></span>'
    '<span class="mh-badge-text">Student Wellbeing Lab</span></div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="mh-title">How\'s your digital <em>rhythm</em> treating you?</div>',
    unsafe_allow_html=True
)
st.markdown(
    f'<div class="mh-subtitle">Answer a few questions about your habits, sleep, and screen time. '
    f'A model trained on student profiles will estimate a Mental Health Score from {SCORE_MIN}-{SCORE_MAX}.</div>',
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("⚙️ API Settings")
    api_url = st.text_input("FastAPI base URL", value=DEFAULT_API_URL)
    if st.button("Check API connection"):
        try:
            r = requests.get(api_url + "/", timeout=5)
            st.success("Connected ✅") if r.status_code == 200 else st.error(f"Status {r.status_code}")
        except requests.exceptions.RequestException as e:
            st.error(f"Could not reach API: {e}")
    st.caption(f"Score gauge assumes a {SCORE_MIN}-{SCORE_MAX} scale. Edit SCORE_MIN / SCORE_MAX in app.py if different.")

left_col, right_col = st.columns([1.4, 1], gap="medium")

# ---------------------------------------------------------------------------
# Left card - form
# ---------------------------------------------------------------------------
with left_col:
    with st.container(key="left_card"):
        with st.form("prediction_form"):

            st.markdown('<div class="mh-section-label">About You</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                age = st.number_input("Age", min_value=10, max_value=100, value=21, step=1)
            with c2:
                gender = st.selectbox("Gender", ["Male", "Female"], index=0)

            c3, c4 = st.columns(2)
            with c3:
                country = st.text_input("Country", value="India")
            with c4:
                academic_level = st.selectbox("Academic level", ACADEMIC_LEVELS, index=0)

            st.markdown('<hr class="mh-divider">', unsafe_allow_html=True)
            st.markdown('<div class="mh-section-label">Daily Rhythm</div>', unsafe_allow_html=True)
            sleep_hours_per_night = st.slider("Sleep per night (hours)", 0.0, 24.0, 7.0, step=0.5)
            study_hours = st.slider("Study time (hours/day)", 0.0, 24.0, 4.0, step=0.5)
            physical_activity_hours = st.slider("Physical activity (hours/day)", 0.0, 24.0, 2.0, step=0.5)
            stress_level = st.selectbox("Stress level", STRESS_LEVELS, index=1)

            st.markdown('<hr class="mh-divider">', unsafe_allow_html=True)
            st.markdown('<div class="mh-section-label">Digital Habits</div>', unsafe_allow_html=True)
            c5, c6 = st.columns(2)
            with c5:
                most_used_platform = st.selectbox("Most-used platform", PLATFORMS, index=0)
            with c6:
                purpose_of_use = st.selectbox("Main purpose", PURPOSES, index=0)

            avg_daily_usage_hours = st.slider("Social media use (hours/day)", 0.0, 24.0, 4.0, step=0.5)
            daily_unlocks = st.number_input("Phone unlocks (per day)", min_value=0, value=100, step=1)

            st.write("")
            submitted = st.form_submit_button("Predict my score")

    if submitted:
        payload = {
            "age": int(age), "gender": gender, "country": country,
            "academic_level": academic_level, "most_used_platform": most_used_platform,
            "purpose_of_use": purpose_of_use, "avg_daily_usage_hours": float(avg_daily_usage_hours),
            "daily_unlocks": int(daily_unlocks), "study_hours": float(study_hours),
            "physical_activity_hours": float(physical_activity_hours),
            "sleep_hours_per_night": float(sleep_hours_per_night), "stress_level": stress_level,
        }
        try:
            with st.spinner("Reading your rhythm..."):
                response = requests.post(f"{api_url}/predict", json=payload, timeout=10)
            if response.status_code == 200:
                st.session_state.score = response.json()["predicted_mental_health_score"]
                st.session_state.error = None
            else:
                st.session_state.error = f"API error {response.status_code}: {response.text}"
                st.session_state.score = None
        except requests.exceptions.RequestException as e:
            st.session_state.error = f"Could not reach the API: {e}"
            st.session_state.score = None
        st.rerun()

# ---------------------------------------------------------------------------
# Right panel - gauge
# ---------------------------------------------------------------------------
with right_col:
    with st.container(key="right_panel"):
        score = st.session_state.score
        display_value = score if score is not None else 0

        fig = go.Figure(go.Indicator(
            mode="gauge",
            value=display_value,
            gauge={
                "axis": {"range": [SCORE_MIN, SCORE_MAX], "visible": False},
                "bar": {"color": "#a78bfa" if score is not None else "rgba(167,139,250,0.2)", "thickness": 0.28},
                "bgcolor": "rgba(255,255,255,0.04)",
                "borderwidth": 0,
            },
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=20, b=0),
            height=190,
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        if st.session_state.error:
            st.markdown(f'<div class="mh-panel-caption" style="color:#f0a; ">{st.session_state.error}</div>',
                        unsafe_allow_html=True)
        elif score is None:
            st.markdown('<div class="mh-score-big">—</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mh-score-outof">out of {SCORE_MAX}</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="mh-panel-caption">Fill in your details and click "Predict my score" '
                'to see your result here.</div>',
                unsafe_allow_html=True
            )
        else:
            pct = max(SCORE_MIN, min(SCORE_MAX, score)) / SCORE_MAX
            st.markdown(f'<div class="mh-score-big">{score:.1f}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mh-score-outof">out of {SCORE_MAX}</div>', unsafe_allow_html=True)
            if pct >= 0.7:
                tag, caption = "Doing well", "Your lifestyle inputs line up with healthier patterns in the data."
            elif pct >= 0.4:
                tag, caption = "Mixed signals", "Some habits look solid, others may be worth a closer look."
            else:
                tag, caption = "Needs attention", "Sleep, stress, and screen time stand out as areas to revisit."
            st.markdown(f'<div class="mh-pill">{tag}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="mh-panel-caption">{caption}</div>', unsafe_allow_html=True)

st.markdown(
    '<div style="margin-top:2rem; color:#7d7fa0; font-size:0.78rem;">'
    '⚠️ This is a modeled estimate for reflection, not a clinical diagnosis. '
    'If you\'re struggling, please talk to a mental health professional.</div>',
    unsafe_allow_html=True
)
