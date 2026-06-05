import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from reportlab.pdfgen import canvas
import io

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="POSTURE IQ V5",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION INIT (SAFE) ----------------

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

# ---------------- PDF FUNCTION ----------------

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

    st.title("🧠 POSTURE IQ V5")

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

    st.title("ERGOGUARD PRO")

    st.markdown("AI Powered Ergonomic Health System")

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

# ---------------- DASHBOARD (V5 FULL UPGRADE) ----------------

elif st.session_state.page == "Dashboard":

    st.title("📊 POSTURE IQ DASHBOARD V5")

    # ---------------- METRICS ----------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Health Score", st.session_state.health_score)

    with col2:
        st.metric("Badge", st.session_state.badge)

    with col3:
        st.metric("Risk", st.session_state.risk_level)

    with col4:
        st.metric("Streak", st.session_state.streak)

    # ---------------- GAUGE ----------------

    st.subheader("⛽ Health Gauge")

    gauge = go.Figure(go.Indicator(
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

    st.plotly_chart(gauge, use_container_width=True)

    # ---------------- TREND ----------------

    st.subheader("📈 Health Trend")

    st.session_state.history.append(st.session_state.health_score)

    trend = go.Figure()
    trend.add_trace(go.Scatter(
        y=st.session_state.history,
        mode="lines+markers"
    ))

    st.plotly_chart(trend, use_container_width=True)

    # ---------------- AI COACH ----------------

    st.subheader("🤖 AI Coach")

    if st.session_state.health_score >= 80:
        st.success("Excellent posture")
        st.session_state.badge = "Elite"

    elif st.session_state.health_score >= 60:
        st.warning("Moderate risk")
        st.session_state.badge = "Healthy"

    else:
        st.error("High risk detected")
        st.session_state.badge = "Beginner"

    # ---------------- IMAGE UPLOAD ----------------

    st.subheader("📷 Workstation Scan (AI Ready)")

    img = st.file_uploader("Upload workstation image", type=["png", "jpg", "jpeg"])

    if img:
        st.image(img, use_container_width=True)

    # ---------------- WEEKLY REPORT ----------------

    st.subheader("📄 Weekly Report")

    if st.button("Generate Report"):

        avg = sum(st.session_state.history[-7:]) / len(st.session_state.history[-7:])

        report = f"""
User: {st.session_state.username}
Score: {st.session_state.health_score}
Average: {avg:.2f}
Badge: {st.session_state.badge}
Risk: {st.session_state.risk_level}
Date: {datetime.now()}
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

    st.subheader("🏆 Achievements")

    if st.session_state.health_score >= 80:
        st.balloons()
        st.success("Elite Level Unlocked")

    elif st.session_state.health_score >= 60:
        st.info("Healthy Level")

    else:
        st.warning("Beginner Level")

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

    st.title("📄 REPORT HISTORY")

    if len(st.session_state.reports) == 0:
        st.info("No reports yet")
    else:
        for r in st.session_state.reports:
            st.text(r)
