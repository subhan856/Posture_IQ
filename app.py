import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="POSTURE IQ",
    page_icon="🧠",
    layout="wide"
)

# ---------------- SAFE CSS ----------------

st.markdown("""
<style>
.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION DEFAULTS ----------------

defaults = {
    "logged_in": False,
    "username": "",
    "page": "Home",
    "health_score": 75,
    "badge": "Beginner",
    "risk_level": "Unknown",
    "history": [75],
    "reports": []
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- PDF FUNCTION ----------------

def generate_pdf(username, score, badge, risk):

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.drawString(100, 750, "POSTURE IQ REPORT")
    c.drawString(100, 720, f"User: {username}")
    c.drawString(100, 700, f"Health Score: {score}")
    c.drawString(100, 680, f"Badge: {badge}")
    c.drawString(100, 660, f"Risk Level: {risk}")
    c.drawString(100, 640, f"Date: {datetime.now()}")

    c.save()
    buffer.seek(0)
    return buffer

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🧠 POSTURE IQ")

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

    st.markdown("<div class='card'><h1>ERGOGUARD PRO</h1></div>", unsafe_allow_html=True)

    st.info("AI Powered Ergonomic System")

    st.write("Health Score:", st.session_state.health_score)

# ---------------- DASHBOARD ----------------

elif st.session_state.page == "Dashboard":

    st.title("📊 DASHBOARD")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Score", st.session_state.health_score)

    with col2:
        st.metric("Badge", st.session_state.badge)

    with col3:
        st.metric("Risk", st.session_state.risk_level)

    # ---------------- GAUGE ----------------

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

    st.markdown("## 📈 Trend")

    st.session_state.history.append(st.session_state.health_score)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(y=st.session_state.history, mode="lines+markers"))

    st.plotly_chart(fig2, use_container_width=True)

    # ---------------- IMAGE ----------------

    st.markdown("## 📷 Upload Workstation")

    img = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

    if img:
        st.image(img, use_container_width=True)

    # ---------------- AUTO SAVE REPORT ----------------

    if st.button("💾 Save Snapshot Report"):

        report = {
            "time": str(datetime.now()),
            "score": st.session_state.health_score,
            "badge": st.session_state.badge,
            "risk": st.session_state.risk_level
        }

        st.session_state.reports.append(report)
        st.success("Report saved!")

    # ---------------- PDF DOWNLOAD ----------------

    st.markdown("## 📄 Download PDF Report")

    pdf = generate_pdf(
        st.session_state.username,
        st.session_state.health_score,
        st.session_state.badge,
        st.session_state.risk_level
    )

    st.download_button(
        "⬇ Download Report PDF",
        pdf,
        file_name="posture_iq_report.pdf",
        mime="application/pdf"
    )

    # ---------------- ACHIEVEMENTS ----------------

    st.markdown("## 🏆 Achievements")

    if st.session_state.health_score >= 80:
        st.balloons()
        st.success("Pro Master Unlocked")
        st.session_state.badge = "Pro Master"

    elif st.session_state.health_score >= 60:
        st.info("Healthy User")
        st.session_state.badge = "Healthy User"

    else:
        st.warning("Beginner")
        st.session_state.badge = "Beginner"

# ---------------- ASSESSMENT ----------------

elif st.session_state.page == "Assessment":

    st.title("ASSESSMENT")

    q = [st.slider(f"Q{i}", 1, 5, 3) for i in range(1, 11)]

    if st.button("CALCULATE"):

        score = int((sum(q) / 50) * 100)

        st.session_state.health_score = score

        if score >= 80:
            st.session_state.risk_level = "Low"

        elif score >= 60:
            st.session_state.risk_level = "Medium"

        else:
            st.session_state.risk_level = "High"

        st.session_state.history.append(score)

        st.rerun()

# ---------------- REPORTS PAGE ----------------

elif st.session_state.page == "Reports":

    st.title("📄 SAVED REPORTS")

    if len(st.session_state.reports) == 0:
        st.info("No reports yet")
    else:
        for r in st.session_state.reports:
            st.markdown(f"""
            ---
            ⏰ {r['time']}  
            📊 Score: {r['score']}  
            🏅 Badge: {r['badge']}  
            ⚠ Risk: {r['risk']}
            """)
