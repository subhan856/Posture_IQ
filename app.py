import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from reportlab.pdfgen import canvas
import io

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="POSTURE IQ AI PRO",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# MODERN UI (SAFE ADDITION ONLY)
# =========================================================

st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

.card {
    background: rgba(255,255,255,0.06);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    backdrop-filter: blur(10px);
}

h1,h2,h3 { color:white; }

div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    padding: 10px;
    border-radius: 10px;
}

.stButton button {
    background: linear-gradient(90deg,#00c6ff,#0072ff);
    color:white;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE (FULL SAFE INIT)
# =========================================================

defaults = {
    "logged_in": False,
    "username": "",
    "page": "Home",
    "health_score": 75,
    "badge": "Beginner",
    "risk": "Unknown",
    "streak": 1,
    "history": [75],
    "ai_questions": [],
    "reports": []
}

for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =========================================================
# PDF SYSTEM (UNCHANGED + SAFE)
# =========================================================

def create_pdf(user, score, badge, risk):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)

    c.drawString(100, 750, "POSTURE IQ FULL REPORT")
    c.drawString(100, 720, f"User: {user}")
    c.drawString(100, 700, f"Score: {score}")
    c.drawString(100, 680, f"Badge: {badge}")
    c.drawString(100, 660, f"Risk: {risk}")
    c.drawString(100, 640, str(datetime.now()))

    c.save()
    buffer.seek(0)
    return buffer

# =========================================================
# AI HYBRID QUESTION ENGINE (NEW ADDITION)
# =========================================================

def generate_ai_questions(score):

    base = [
        "Do you sit more than 2 hours continuously?",
        "Is your screen at eye level?",
        "Do you take breaks regularly?"
    ]

    if score < 60:
        extra = [
            "Do you feel neck pain?",
            "Do you slouch often?",
            "Do you ignore breaks?"
        ]

    elif score < 80:
        extra = [
            "Is your wrist straight while typing?",
            "Do you lean forward while working?"
        ]

    else:
        extra = [
            "Do you maintain posture even when tired?",
            "Do you still stretch regularly?"
        ]

    return base + extra

# =========================================================
# SIDEBAR (ORIGINAL STYLE PRESERVED)
# =========================================================

with st.sidebar:

    st.title("🧠 POSTURE IQ AI")

    if st.button("🏠 Home"):
        st.session_state.page = "Home"

    if st.button("📊 Dashboard"):
        st.session_state.page = "Dashboard"

    if st.button("📝 Assessment"):
        st.session_state.page = "Assessment"

    if st.button("👤 Profile"):
        st.session_state.page = "Profile"

    if st.button("📄 Reports"):
        st.session_state.page = "Reports"

# =========================================================
# HOME PAGE (UNCHANGED + POLISHED)
# =========================================================

if st.session_state.page == "Home":

    st.markdown("""
    <div class='card'>
        <h1>🧠 POSTURE IQ AI SYSTEM</h1>
        <p>AI Powered Ergonomic Health Analyzer</p>
    </div>
    """, unsafe_allow_html=True)

    st.info("Smart posture tracking + AI adaptive assessment system")

# =========================================================
# LOGIN
# =========================================================

elif st.session_state.page == "Login":

    st.title("LOGIN")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("LOGIN"):
        if email and password:
            st.session_state.logged_in = True
            st.session_state.username = email.split("@")[0]
            st.session_state.page = "Dashboard"
            st.rerun()

# =========================================================
# SIGNUP
# =========================================================

elif st.session_state.page == "Signup":

    st.title("SIGNUP")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password")

    if st.button("CREATE"):
        if name and email and password:
            st.session_state.logged_in = True
            st.session_state.username = name
            st.session_state.page = "Dashboard"
            st.rerun()

# =========================================================
# DASHBOARD (FULL ORIGINAL + AI + GRAPH UPGRADE)
# =========================================================

elif st.session_state.page == "Dashboard":

    st.markdown("<div class='card'><h1>📊 DASHBOARD AI PRO</h1></div>", unsafe_allow_html=True)

    # ---------------- METRICS ----------------

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric("Score", st.session_state.health_score)

    with c2:
        st.metric("Badge", st.session_state.badge)

    with c3:
        st.metric("Risk", st.session_state.risk)

    with c4:
        st.metric("Streak", st.session_state.streak)

    # ---------------- GAUGE ----------------

    st.subheader("⛽ Health Meter")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=st.session_state.health_score,
        gauge={
            "axis":{"range":[0,100]},
            "steps":[
                {"range":[0,60],"color":"red"},
                {"range":[60,80],"color":"orange"},
                {"range":[80,100],"color":"green"}
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- TREND GRAPH ----------------

    st.subheader("📈 Health Trend")

    st.session_state.history.append(st.session_state.health_score)

    df = pd.DataFrame({"score": st.session_state.history})

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(y=df["score"], mode="lines+markers"))

    st.plotly_chart(fig2, use_container_width=True)

    # ---------------- AI QUESTIONS (HYBRID SYSTEM) ----------------

    st.subheader("🧠 AI Adaptive Questions")

    if st.button("Generate AI Questions"):
        st.session_state.ai_questions = generate_ai_questions(st.session_state.health_score)

    for i,q in enumerate(st.session_state.ai_questions):
        st.radio(q, ["Yes","No"], key=f"ai_{i}")

    # ---------------- IMAGE UPLOAD ----------------

    st.subheader("📷 Workstation Scan")

    img = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])

    if img:
        st.image(img, use_container_width=True)

    # ---------------- BADGE SYSTEM ----------------

    if st.session_state.health_score >= 80:
        st.session_state.badge = "Elite"
        st.success("Elite Level")

    elif st.session_state.health_score >= 60:
        st.session_state.badge = "Healthy"
        st.warning("Healthy Level")

    else:
        st.session_state.badge = "Beginner"
        st.error("Beginner Level")

    # ---------------- PDF ----------------

    pdf = create_pdf(
        st.session_state.username,
        st.session_state.health_score,
        st.session_state.badge,
        st.session_state.risk
    )

    st.download_button(
        "⬇ Download PDF Report",
        pdf,
        file_name="posture_iq_report.pdf",
        mime="application/pdf"
    )

# =========================================================
# PROFILE
# =========================================================

elif st.session_state.page == "Profile":

    st.title("PROFILE")

    st.write("User:", st.session_state.username)
    st.write("Badge:", st.session_state.badge)
    st.write("Score:", st.session_state.health_score)

# =========================================================
# ASSESSMENT (HYBRID QUESTIONS ADDED HERE TOO)
# =========================================================

elif st.session_state.page == "Assessment":

    st.title("ASSESSMENT SYSTEM")

    q = generate_ai_questions(st.session_state.health_score)

    answers = []

    for i, question in enumerate(q):
        answers.append(st.slider(question, 1, 5, 3, key=f"q_{i}"))

    if st.button("CALCULATE SCORE"):

        score = int((sum(answers) / (len(answers)*5)) * 100)

        st.session_state.health_score = score
        st.session_state.history.append(score)

        if score >= 80:
            st.session_state.risk = "Low"

        elif score >= 60:
            st.session_state.risk = "Medium"

        else:
            st.session_state.risk = "High"

        st.rerun()

# =========================================================
# REPORTS
# =========================================================

elif st.session_state.page == "Reports":

    st.title("REPORT HISTORY")

    for r in st.session_state.history:
        st.write("Score:", r)
