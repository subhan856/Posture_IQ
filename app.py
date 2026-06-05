import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from reportlab.pdfgen import canvas
import io

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="POSTURE IQ PRO",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- MODERN UI (V6 GRAPHICS) ----------------

st.markdown("""
<style>

/* Background */
.main {
    background: linear-gradient(135deg, #0f172a, #1e293b);
}

/* Glass card */
.card {
    background: rgba(255,255,255,0.06);
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 15px;
}

/* Titles */
h1, h2, h3 {
    color: white;
}

/* Metrics */
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 10px;
    box-shadow: 0 0 15px rgba(0,255,200,0.08);
}

/* Buttons */
.stButton button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    border: none;
}

.stButton button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 15px #00c6ff;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------

defaults = {
    "logged_in": False,
    "username": "",
    "page": "Home",
    "health_score": 75,
    "badge": "Beginner",
    "risk_level": "Unknown",
    "streak": 1,
    "history": [75],
    "reports": [],
    "assessment_done": False
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- PDF SYSTEM ----------------

def create_pdf(user, score, badge, risk):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer)

    c.drawString(100, 750, "POSTURE IQ REPORT")
    c.drawString(100, 720, f"User: {user}")
    c.drawString(100, 700, f"Score: {score}")
    c.drawString(100, 680, f"Badge: {badge}")
    c.drawString(100, 660, f"Risk: {risk}")
    c.drawString(100, 640, f"Date: {datetime.now()}")

    c.save()
    buffer.seek(0)
    return buffer

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🧠 POSTURE IQ PRO")

    if st.button("🏠 Home"):
        st.session_state.page = "Home"

    if st.button("📊 Dashboard"):
        st.session_state.page = "Dashboard"

    if st.button("📝 Assessment"):
        st.session_state.page = "Assessment"

    if st.button("📄 Reports"):
        st.session_state.page = "Reports"

# ---------------- HOME ----------------

if st.session_state.page == "Home":

    st.markdown("""
    <div class='card'>
        <h1>🧠 POSTURE IQ PRO</h1>
        <h3 style='color:#00c6ff;'>AI Ergonomic Intelligence System</h3>
        <p style='color:#aaa;'>Smart posture tracking & AI health insights</p>
    </div>
    """, unsafe_allow_html=True)

    st.info("Track posture, improve health, unlock achievements")

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

# ---------------- DASHBOARD (FULL UPGRADED UI + FEATURES) ----------------

elif st.session_state.page == "Dashboard":

    st.markdown("""
    <div class='card'>
        <h2>📊 Smart Health Dashboard</h2>
        <p style='color:#aaa;'>Real-time AI posture analytics</p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- METRICS ----------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("💪 Health Score", st.session_state.health_score)

    with c2:
        st.metric("🏆 Badge", st.session_state.badge)

    with c3:
        st.metric("⚠ Risk", st.session_state.risk_level)

    with c4:
        st.metric("🔥 Streak", st.session_state.streak)

    # ---------------- GAUGE ----------------

    st.markdown("### ⛽ Health Gauge")

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

    st.markdown("### 📈 Health Trend")

    st.session_state.history.append(st.session_state.health_score)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        y=st.session_state.history,
        mode="lines+markers"
    ))

    st.plotly_chart(fig2, use_container_width=True)

    # ---------------- IMAGE UPLOAD ----------------

    st.markdown("### 📷 Workstation Scan")

    img = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

    if img:
        st.image(img, use_container_width=True)

    # ---------------- AI COACH ----------------

    st.markdown("### 🤖 AI Coach")

    if st.session_state.health_score >= 80:
        st.success("Elite posture detected")
        st.session_state.badge = "Elite"

    elif st.session_state.health_score >= 60:
        st.warning("Moderate risk detected")
        st.session_state.badge = "Healthy"

    else:
        st.error("High risk detected")
        st.session_state.badge = "Beginner"

    # ---------------- WEEKLY REPORT ----------------

    st.markdown("### 📄 Weekly Report")

    if st.button("Generate Report"):

        avg = sum(st.session_state.history[-7:]) / len(st.session_state.history[-7:])

        report = f"""
User: {st.session_state.username}
Score: {st.session_state.health_score}
Average: {avg:.2f}
Badge: {st.session_state.badge}
Risk: {st.session_state.risk_level}
"""

        st.session_state.reports.append(report)
        st.text_area("Report", report, height=200)

    # ---------------- PDF DOWNLOAD ----------------

    pdf = create_pdf(
        st.session_state.username,
        st.session_state.health_score,
        st.session_state.badge,
        st.session_state.risk_level
    )

    st.download_button(
        "⬇ Download PDF Report",
        pdf,
        file_name="posture_iq_report.pdf",
        mime="application/pdf"
    )

    # ---------------- ACHIEVEMENTS ----------------

    st.markdown("### 🏆 Achievements")

    if st.session_state.health_score >= 80:
        st.balloons()
        st.success("ELITE LEVEL UNLOCKED")

    elif st.session_state.health_score >= 60:
        st.info("HEALTHY LEVEL")

    else:
        st.warning("BEGINNER LEVEL")

# ---------------- PROFILE ----------------

elif st.session_state.page == "Profile":

    st.title("PROFILE")

    st.write("User:", st.session_state.username)
    st.write("Badge:", st.session_state.badge)
    st.write("Score:", st.session_state.health_score)

# ---------------- ASSESSMENT ----------------

elif st.session_state.page == "Assessment":

    st.title("ASSESSMENT")

    q = [st.slider(f"Q{i}", 1, 5, 3) for i in range(1, 11)]

    if st.button("CALCULATE"):

        score = int((sum(q) / 50) * 100)

        st.session_state.health_score = score
        st.session_state.history.append(score)

        if score >= 80:
            st.session_state.risk_level = "Low"

        elif score >= 60:
            st.session_state.risk_level = "Medium"

        else:
            st.session_state.risk_level = "High"

        st.rerun()

# ---------------- REPORTS ----------------

elif st.session_state.page == "Reports":

    st.title("REPORT HISTORY")

    if len(st.session_state.reports) == 0:
        st.info("No reports yet")
    else:
        for r in st.session_state.reports:
            st.text(r)
