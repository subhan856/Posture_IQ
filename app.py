import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="POSTURE IQ",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
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

# ---------------- SESSION STATE ----------------

defaults = {
    "logged_in": False,
    "username": "",
    "page": "Home",
    "health_score": 75,
    "badge": "Beginner",
    "risk_level": "Unknown",
    "streak": 1,
    "assessment_done": False,
    "history": [75],
    "uploaded_image": None
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🧠 POSTURE IQ")

    if st.session_state.logged_in:

        st.success(f"Welcome {st.session_state.username}")

        if st.button("🏠 Home"):
            st.session_state.page = "Home"

        if st.button("📊 Dashboard"):
            st.session_state.page = "Dashboard"

        if st.button("📝 Assessment"):
            st.session_state.page = "Assessment"

        if st.button("👤 Profile"):
            st.session_state.page = "Profile"

        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.page = "Home"
            st.rerun()

    else:

        if st.button("🏠 Home"):
            st.session_state.page = "Home"

        if st.button("🔐 Login"):
            st.session_state.page = "Login"

        if st.button("📝 Signup"):
            st.session_state.page = "Signup"

# ---------------- HOME ----------------

if st.session_state.page == "Home":

    st.markdown("""
    <div class="card">
        <h1>ERGOGUARD PRO</h1>
        <p>AI Powered Workstation Health Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🤖 AI Coach")

    if st.session_state.health_score >= 80:
        st.success("Excellent posture detected")
    elif st.session_state.health_score >= 60:
        st.warning("Moderate risk detected")
    else:
        st.error("High risk detected")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Health Score", st.session_state.health_score)

    with col2:
        st.metric("Badge", st.session_state.badge)

    with col3:
        st.metric("Risk", st.session_state.risk_level)

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

        else:
            st.error("Fill all fields")

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

# ---------------- DASHBOARD (FULL V3 UPGRADE) ----------------

elif st.session_state.page == "Dashboard":

    st.title("📊 POSTURE IQ DASHBOARD")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Health Score", st.session_state.health_score)

    with c2:
        st.metric("Badge", st.session_state.badge)

    with c3:
        st.metric("Risk Level", st.session_state.risk_level)

    with c4:
        st.metric("Streak", st.session_state.streak)

    # ---------------- GAUGE ----------------

    st.markdown("## ⛽ Health Gauge")

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=st.session_state.health_score,
        gauge={
            "axis": {"range": [0, 100]},
            "steps": [
                {"range": [0, 60], "color": "red"},
                {"range": [60, 80], "color": "orange"},
                {"range": [80, 100], "color": "green"},
            ],
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- HISTORY GRAPH ----------------

    st.markdown("## 📈 Health Trend")

    st.session_state.history.append(st.session_state.health_score)

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        y=st.session_state.history,
        mode="lines+markers"
    ))

    st.plotly_chart(fig2, use_container_width=True)

    # ---------------- IMAGE UPLOAD ----------------

    st.markdown("## 📷 Workstation Analysis")

    img = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

    if img:
        st.image(img, use_container_width=True)

    # ---------------- WEEKLY REPORT ----------------

    st.markdown("## 📄 Weekly Report")

    if st.button("Generate Report"):

        avg = sum(st.session_state.history[-7:]) / len(st.session_state.history[-7:])

        st.text_area(
            "Report",
            f"Average Score: {avg:.2f}\nBadge: {st.session_state.badge}\nRisk: {st.session_state.risk_level}",
            height=200
        )

    # ---------------- ACHIEVEMENTS ----------------

    st.markdown("## 🏆 Achievements")

    if st.session_state.health_score >= 80:
        st.balloons()
        st.success("🥇 Pro Master Unlocked")

        st.session_state.badge = "Pro Master"

    elif st.session_state.health_score >= 60:
        st.info("🥈 Healthy User")

        st.session_state.badge = "Healthy User"

    else:
        st.warning("🥉 Beginner")

        st.session_state.badge = "Beginner"

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

        if score >= 80:
            st.session_state.badge = "Pro Master"
            st.session_state.risk_level = "Low"

        elif score >= 60:
            st.session_state.badge = "Healthy User"
            st.session_state.risk_level = "Moderate"

        else:
            st.session_state.badge = "Beginner"
            st.session_state.risk_level = "High"

        st.session_state.history.append(score)

        st.rerun()
