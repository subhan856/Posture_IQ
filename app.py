import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from reportlab.pdfgen import canvas
import io

# ---------------- CONFIG ----------------

st.set_page_config(
    page_title="POSTURE IQ V7 FULL",
    page_icon="🧠",
    layout="wide"
)

# ---------------- UI ----------------

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
}

h1,h2,h3 { color:white; }

div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------

defaults = {
    "logged_in": False,
    "username": "",
    "page": "Home",
    "health_score": 75,
    "badge": "Beginner",
    "risk": "Unknown",
    "history": [75],
    "ai_questions": [],
    "answers": [],
    "reports": []
}

for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- PDF ----------------

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

# ---------------- AI ENGINE ----------------

def generate_ai_questions(score):

    base = [
        "Do you sit more than 2 hours continuously?",
        "Is your screen at eye level?",
        "Do you take breaks regularly?"
    ]

    if score < 60:
        return base + [
            "Do you feel neck pain?",
            "Do you slouch often?",
            "Is your chair uncomfortable?"
        ]

    elif score < 80:
        return base + [
            "Is your wrist position correct?",
            "Do you lean forward while typing?"
        ]

    else:
        return base + [
            "Do you maintain posture even while tired?",
            "Do you still stretch regularly?"
        ]

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🧠 POSTURE IQ V7")

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

# ---------------- HOME ----------------

if st.session_state.page == "Home":

    st.markdown("""
    <div class='card'>
        <h1>🧠 POSTURE IQ PRO</h1>
        <p>AI Ergonomic Intelligence System</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- LOGIN ----------------

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

# ---------------- SIGNUP ----------------

elif st.session_state.page == "Signup":

    st.title("SIGNUP")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("CREATE ACCOUNT"):
        if name and email and password:
            st.session_state.logged_in = True
            st.session_state.username = name
            st.session_state.page = "Dashboard"
            st.rerun()

# ---------------- DASHBOARD (FULL RESTORED + AI + GRAPHICS) ----------------

elif st.session_state.page == "Dashboard":

    st.markdown("<div class='card'><h1>📊 POSTURE IQ DASHBOARD</h1></div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Score", st.session_state.health_score)

    with col2:
        st.metric("Badge", st.session_state.badge)

    with col3:
        st.metric("Risk", st.session_state.risk)

    with col4:
        st.metric("Streak", len(st.session_state.history))

    # ---------------- GAUGE ----------------

    st.subheader("⛽ Health Meter")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=st.session_state.health_score,
        gauge={
            "axis": {"range": [0, 100]},
            "steps": [
                {"range": [0, 60], "color": "red"},
                {"range": [60, 80], "color": "orange"},
                {"range": [80, 100], "color": "green"}
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- TREND ----------------

    st.subheader("📈 Health Trend")

    st.session_state.history.append(st.session_state.health_score)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        y=st.session_state.history,
        mode="lines+markers"
    ))

    st.plotly_chart(fig2, use_container_width=True)

    # ---------------- AI HYBRID QUESTIONS ----------------

    st.subheader("🧠 AI Hybrid Question System")

    if st.button("Generate AI Questions"):
        st.session_state.ai_questions = generate_ai_questions(st.session_state.health_score)

    for i, q in enumerate(st.session_state.ai_questions):
        st.radio(q, ["Yes", "No"], key=f"q_{i}")

    # ---------------- IMAGE ----------------

    st.subheader("📷 Workstation Scan")

    img = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    if img:
        st.image(img, use_container_width=True)

    # ---------------- BADGE ----------------

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
        file_name="posture_report_v7.pdf",
        mime="application/pdf"
    )

# ---------------- PROFILE ----------------

elif st.session_state.page == "Profile":
    st.title("PROFILE")
    st.write(st.session_state.username)
    st.write(st.session_state.badge)

# ---------------- ASSESSMENT ----------------

elif st.session_state.page == "Assessment":

    st.title("ASSESSMENT")

    q = [st.slider(f"Q{i}", 1, 5, 3) for i in range(1, 11)]

    if st.button("CALCULATE"):

        score = int((sum(q)/50)*100)
        st.session_state.health_score = score
        st.session_state.history.append(score)

        if score >= 80:
            st.session_state.risk = "Low"
        elif score >= 60:
            st.session_state.risk = "Medium"
        else:
            st.session_state.risk = "High"

        st.rerun()

# ---------------- REPORTS ----------------

elif st.session_state.page == "Reports":

    st.title("REPORTS")

    for r in st.session_state.history:
        st.write(r)
