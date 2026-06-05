import streamlit as st

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="POSTURE IQ",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION VARIABLES ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "health_score" not in st.session_state:
    st.session_state.health_score = 75

if "badge" not in st.session_state:
    st.session_state.badge = "Beginner"

if "streak" not in st.session_state:
    st.session_state.streak = 1

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "assessment_done" not in st.session_state:
    st.session_state.assessment_done = False

if "risk_level" not in st.session_state:
    st.session_state.risk_level = "Unknown"
# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp{
    background: linear-gradient(
        135deg,
        #050816,
        #0a0f2c,
        #111827
    );
    color:white;
}

/* HERO */
.hero{
    text-align:center;
    padding:40px;
    border-radius:25px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(15px);
    border:1px solid rgba(255,255,255,0.1);
    box-shadow:0px 0px 40px rgba(0,255,255,0.15);
}

.hero h1{
    font-family:'Orbitron';
    font-size:60px;
    color:#00F5FF;
}

.hero h3{
    color:white;
}

/* GLASS CARD */

.card{
    background:rgba(255,255,255,0.05);
    padding:25px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.1);
    margin-top:20px;
    transition:0.3s;
}

.card:hover{
    transform:translateY(-5px);
    box-shadow:0 0 25px cyan;
}

/* Feature */
.feature{
    text-align:center;
    padding:25px;
    border-radius:20px;
    background:rgba(255,255,255,0.04);
    border:1px solid rgba(255,255,255,0.08);
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#060b1d;
}

/* Buttons */

.stButton button{
    width:100%;
    border-radius:12px;
    height:55px;
    background:#00F5FF;
    color:black;
    font-weight:bold;
}

/* Inputs */

.stTextInput input{
    border-radius:10px;
}

/* Footer */
.footer{
    text-align:center;
    color:gray;
    margin-top:50px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------

if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("# 🧠 POSTURE IQ")

    if st.session_state.logged_in:

        st.success(
            f"Welcome {st.session_state.username}"
        )

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
    <div class='hero'>
        <h1>ERGOGUARD PRO</h1>
        <h3>AI Powered Workstation Safety & Ergonomic Health Assistant</h3>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    c1,c2,c3 = st.columns(3)

    with c1:
       with right:

    st.markdown("### 🤖 AI Coach")

    if st.session_state.health_score >= 80:

        st.success("""
        Excellent posture detected.

        ✔ Maintain current setup

        ✔ Continue stretching

        ✔ Keep taking breaks
        """)

    elif st.session_state.health_score >= 60:

        st.warning("""
        Moderate ergonomic risk.

        • Improve monitor height

        • Adjust chair support

        • Take more breaks
        """)

    else:

        st.error("""
        High ergonomic risk.

        • Improve workstation setup

        • Reduce continuous sitting

        • Follow posture exercises
        """)

    with c2:
        st.markdown("""
        <div class='feature'>
            <h2>📈 Analytics</h2>
            <p>Track your ergonomic progress.</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class='feature'>
            <h2>📄 PDF Reports</h2>
            <p>Professional downloadable reports.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    st.markdown("""
    <div class='card'>
    <h2>🚀 Why POSTURE IQ?</h2>

    <ul>
    <li>AI Ergonomic Assessment</li>
    <li>Photo Upload Analysis</li>
    <li>Daily Health Tasks</li>
    <li>Progress Tracking</li>
    <li>Achievement System</li>
    <li>Professional Reports</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

# ---------------- LOGIN ----------------

elif st.session_state.page == "Login":

    st.markdown("""
    <div class='hero'>
    <h1>POSTURE IQ LOGIN</h1>
    </div>
    """, unsafe_allow_html=True)

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("LOGIN"):

        if email and password:

            st.session_state.logged_in = True

            st.session_state.username = email.split("@")[0]

            st.session_state.page = "Dashboard"

            st.rerun()

        else:

            st.error("Enter Email & Password")

# ---------------- SIGNUP ----------------
elif st.session_state.page == "Signup":

    st.markdown("""
    <div class='hero'>
    <h1>CREATE ACCOUNT</h1>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input("Full Name")

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("CREATE ACCOUNT"):

        if name and email and password:

            st.session_state.logged_in = True

            st.session_state.username = name

            st.session_state.page = "Dashboard"

            st.rerun()

        else:

            st.error("Fill All Fields")

        
elif st.session_state.page == "Dashboard":

    st.markdown("""
    <div class='hero'>
    <h1>POSTURE IQ DASHBOARD</h1>
    </div>
    """, unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.metric(
            "Health Score",
            f"{st.session_state.health_score}%"
        )

    with c2:
        st.metric(
            "Current Badge",
            st.session_state.badge
        )

    with c3:
        st.metric(
            "Daily Streak",
            st.session_state.streak
        )

    with c4:
        st.metric(
            "Risk Level",
            "Low"
        )

    st.divider()

    left,right = st.columns(2)

    with left:

        st.markdown("""
        ### 🎯 Today's Mission

        ✅ Drink 2L Water

        ✅ Take 5 Stretch Breaks

        ✅ Maintain Eye Level Screen

        ✅ Walk For 15 Minutes
        """)

    with right:

        st.markdown("""
        ### 🤖 AI Coach

        Your workstation posture is
        currently good.

        Focus on:

        • Neck alignment

        • Wrist position

        • Screen distance

        • Regular stretching
        """)

    st.divider()

    st.markdown("## 🏆 Achievements")

    st.write(advice)

    a,b,c = st.columns(3)

    with a:
        st.success("🥉 Beginner")

    with b:
        st.info("🥈 Healthy User")

    with c:
        st.warning("🥇 Ergonomic Master")

elif st.session_state.page == "Profile":

    st.markdown("""
    <div class='hero'>
    <h1>USER PROFILE</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    ### 👤 Username

    {st.session_state.username}

    ### 🏆 Badge

    {st.session_state.badge}

    ### 🔥 Streak

    {st.session_state.streak} Days

    ### ❤️ Health Score

    {st.session_state.health_score}%
    """)

elif st.session_state.page == "Assessment":

    st.title("📝 POSTURE IQ Assessment")

    q1 = st.slider(
        "Monitor Height",
        1,5,3
    )

    q2 = st.slider(
        "Chair Comfort",
        1,5,3
    )

    q3 = st.slider(
        "Screen Distance",
        1,5,3
    )

    q4 = st.slider(
        "Lighting Quality",
        1,5,3
    )

    q5 = st.slider(
        "Break Frequency",
        1,5,3
    )

    q6 = st.slider(
        "Back Support",
        1,5,3
    )

    q7 = st.slider(
        "Keyboard Position",
        1,5,3
    )

    q8 = st.slider(
        "Mouse Position",
        1,5,3
    )

    q9 = st.slider(
        "Neck Posture",
        1,5,3
    )

    q10 = st.slider(
        "Workstation Organization",
        1,5,3
    )

    if st.button("🚀 Calculate Score"):

        total = (
            q1+q2+q3+q4+q5+
            q6+q7+q8+q9+q10
        )

        score = int((total/50)*100)

        st.session_state.health_score = score

        if score >= 80:

            st.session_state.risk_level = "Low Risk"

            st.session_state.badge = "Ergonomic Master"

        elif score >= 60:

            st.session_state.risk_level = "Moderate Risk"

            st.session_state.badge = "Healthy User"

        else:

            st.session_state.risk_level = "High Risk"

            st.session_state.badge = "Beginner"

        st.session_state.assessment_done = True

        st.rerun()
# ---------------- FOOTER ----------------

st.markdown("""
<div class='footer'>
© 2026 ErgoGuard Pro | ICT Health & Ergonomics Project
</div>
""", unsafe_allow_html=True)
