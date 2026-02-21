import streamlit as st
import time

# Inject Launch Page specific CSS (Full Screen, Hide Sidebar, Background Image)
st.markdown("""
<style>
    /* Hide the Streamlit Sidebar solely and completely for the Launch Page */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    
    /* Global modifications for launch page */
    .stApp {
        background: transparent !important;
        animation: none !important; /* disabled global animated gradient */
    }
    
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        background: linear-gradient(180deg, rgba(9, 10, 15, 0.2) 0%, rgba(9, 10, 15, 0.6) 100%), 
                    url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=2000&auto=format&fit=crop') repeat center center !important;
        background-size: 200% 200% !important;
        animation: moveBackground 40s linear infinite alternate !important;
    }
    
    @keyframes moveBackground {
        0% { background-position: 0% 0%; }
        100% { background-position: 100% 100%; }
    }
    
    .reportview-container {
        padding: 0 !important;
    }

    /* Launch Page Title Animations */
    .launch-title-container {
font-family:'poppins',sans-serif;
        text-align: center;
        margin-top: 5vh;
        margin-bottom: 5vh;
        animation: zoomIn 1.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    .launch-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #00e5ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
        text-shadow: 0 0 40px rgba(0, 229, 255, 0.4);
    }
    
    .launch-tagline {
        font-size: 1.5rem;
        color: #e2e8f0;
        font-weight: 400;
        letter-spacing: 2px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.8);
    }
    
    @keyframes zoomIn {
        from { opacity: 0; transform: scale(0.9); }
        to { opacity: 1; transform: scale(1); }
    }
    
    /* Glassmorphism Card for Location & Buttons */
    .launch-card {
        background: rgba(20, 22, 28, 0.65);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        padding: 50px 40px;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 30px 60px rgba(0,0,0,0.6), inset 0 1px 0 rgba(255,255,255,0.2);
        text-align: center;
        animation: slideInUp 1s cubic-bezier(0.16, 1, 0.3, 1) 0.5s forwards;
        opacity: 0; /* starts hidden for animation */
        max-width: 650px;
        margin: 0 auto;
        color: white;
    }
    
    .launch-card h2 {
        color: #ffffff;
        font-weight: 700;
        margin-bottom: 20px;
        font-size: 1.8rem;
    }
    
    .launch-card p {
        color: #cbd5e1;
        margin-bottom: 30px;
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    /* Customising the GeoLocation Component container */
    iframe {
        background: transparent !important;
        border: none !important;
    }
    
    /* Hide the geolocation text and just leave the button */
    div[data-testid="stMarkdown"] p {
        margin-bottom: 0 !important;
    }
    
    /* Standard Auth Buttons & Custom Wrapper styling */
    div[data-testid="stButton"] button {
        border-radius: 12px !important;
        border: 1px solid #00e5ff !important;
        background: rgba(0, 229, 255, 0.1) !important;
        color: #00e5ff !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        font-weight: 600 !important;
        letter-spacing: 1px !important;
        height: 60px !important;
        font-size: 1.2rem !important;
    }
    
    /* Make both primary and secondary identical neon blue glow for auth */
    div[data-testid="stButton"] button {
        background: linear-gradient(90deg, #00f5ff, #00bcd4) !important;
        color: #000000 !important; /* Dark text for contrast */
        border: none !important;
        box-shadow: 0 0 15px rgba(0, 229, 255, 0.4) !important;
    }
    
    div[data-testid="stButton"] button:disabled {
        background: rgba(255, 255, 255, 0.1) !important;
        color: rgba(255, 255, 255, 0.3) !important;
        box-shadow: none !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        cursor: not-allowed !important;
    }
    
    div[data-testid="stButton"] button:disabled:hover {
        transform: none !important;
        box-shadow: none !important;
    }
    
    div[data-testid="stButton"] button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 10px 25px rgba(0, 229, 255, 0.6) !important;
        border-color: #00e5ff !important;
    }
    
    div[data-testid="stButton"] button:active {
        transform: scale(0.95) !important;
    }

</style>
""", unsafe_allow_html=True)

# ----- UI STRUCTURE -----

# Title Section
st.markdown("""
<div class="launch-title-container">
    <div class="launch-title">Panic Shield</div>
    <div class="launch-tagline">AI Disaster Intelligence & Safety Platform</div>
</div>
""", unsafe_allow_html=True)

# Main Launch Card Layout
st.markdown('<div class="launch-card">', unsafe_allow_html=True)



c1, c2, c3, c4 = st.columns([1, 4, 4, 1])

with c2:
    if st.button("SIGN IN", use_container_width=True): 
        st.switch_page("views/login.py")
with c3:
    if st.button("SIGN UP", use_container_width=True): 
        st.switch_page("views/register.py")

st.markdown('</div>', unsafe_allow_html=True) # End card