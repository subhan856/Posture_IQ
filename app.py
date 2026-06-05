import streamlit as st

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="ErgoGuard Pro",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

    st.markdown("# ⚡ ErgoGuard Pro")

    if st.button("🏠 Home"):
        st.session_state.page = "Home"

    if st.button("🔐 Login"):
        st.session_state.page = "Login"

    if st.button("📝 Sign Up"):
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
        st.markdown("""
        <div class='feature'>
            <h2>🧠 AI Coach</h2>
            <p>Smart posture recommendations.</p>
        </div>
        """, unsafe_allow_html=True)

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
    <h2>🚀 Why ErgoGuard Pro?</h2>

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
    <h1>LOGIN</h1>
    </div>
    """, unsafe_allow_html=True)

    email = st.text_input("Email")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("LOGIN"):
        st.success(
            "Firebase Login Coming In Part 2"
        )

# ---------------- SIGNUP ----------------

elif st.session_state.page == "Signup":

    st.markdown("""
    <div class='hero'>
    <h1>SIGN UP</h1>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input("Full Name")

    email = st.text_input("Email Address")

    password = st.text_input(
        "Create Password",
        type="password"
    )

    confirm = st.text_input(
        "Confirm Password",
        type="password"
    )

    if st.button("CREATE ACCOUNT"):
        st.success(
            "Firebase Signup Coming In Part 2"
        )

# ---------------- FOOTER ----------------

st.markdown("""
<div class='footer'>
© 2026 ErgoGuard Pro | ICT Health & Ergonomics Project
</div>
""", unsafe_allow_html=True)
