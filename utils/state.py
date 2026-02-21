import streamlit as st
import pandas as pd

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'current_user_name' not in st.session_state:
        st.session_state['current_user_name'] = ""
    if 'current_user_blood' not in st.session_state:
        st.session_state['current_user_blood'] = ""
        
    if 'history' not in st.session_state:
        st.session_state['history'] = pd.DataFrame(columns=['Time', 'Panic_Score', 'Sentiment', 'Movement', 'Comms'])
    if 'alerts' not in st.session_state:
        st.session_state['alerts'] = []
    if 'help_messages' not in st.session_state:
        st.session_state['help_messages'] = []
    if 'sim_running' not in st.session_state:
        st.session_state['sim_running'] = True
    if 'user_safe' not in st.session_state:
        st.session_state['user_safe'] = False
    if 'user_in_danger_zone' not in st.session_state:
        st.session_state['user_in_danger_zone'] = False
    if 'volunteers' not in st.session_state:
        st.session_state['volunteers'] = pd.DataFrame({
            'Name': ['@SarahO', '@MikeT', '@EmmaW', '@DavidL', '@RajP'],
            'Contact_Number': ['+1-555-0101', '+1-555-0102', '+1-555-0103', '+1-555-0104', '+1-555-0105'],
            'Trust_Score': [98, 95, 88, 82, 79],
            'Reports_Verified': [142, 115, 89, 64, 41],
            'Region': ['Mumbai', 'Delhi', 'Mumbai', 'Bangalore', 'Chennai'],
            'Skills': ['Medical, CPR', 'Logistics', 'Search & Rescue', 'Medical', 'Logistics, Search & Rescue'],
            'Status': ['🟢 Available', '🟢 Available', '🟡 Busy', '🔴 Offline', '🟢 Available'],
            'Last_Active': ['2 mins ago', '5 mins ago', '12 mins ago', '1 day ago', '1 hr ago'],
            'Location': ['Dharavi', 'Connaught Place', 'Bandra Kurla', 'Indiranagar', 'T Nagar'],
            'lat': [19.0380, 28.6315, 19.0596, 12.9784, 13.0405],
            'lon': [72.8538, 77.2167, 72.8295, 77.6408, 80.2337]
        })
    if 'danger_acknowledged' not in st.session_state:
        st.session_state['danger_acknowledged'] = False
    if 'danger_alert_time' not in st.session_state:
        st.session_state['danger_alert_time'] = None
    if 'survival_history' not in st.session_state:
        st.session_state['survival_history'] = [
            "🛡️ **Hurricane Delta (2024)** - Marked Safe",
            "🛡️ **Sector B Grid Failure (2025)** - Marked Safe"
        ]
    if 'active_disasters' not in st.session_state:
        st.session_state['active_disasters'] = [
            {"title": "Flash Flood", "loc": "Mumbai, Maharashtra", "risk": 92, "time": "12 mins ago", "color": "#f43f5e", "icon": "🌊", "badge": "CRITICAL", "safe_zone": "Bandra Kurla Complex (BKC) Shelter"},
            {"title": "Industrial Fire", "loc": "Delhi NCR", "risk": 78, "time": "45 mins ago", "color": "#f97316", "icon": "🔥", "badge": "HIGH", "safe_zone": "Community Center Alpha"},
            {"title": "Earthquake", "loc": "Guwahati, Assam", "risk": 45, "time": "2 hours ago", "color": "#eab308", "icon": "🌍", "badge": "MEDIUM", "safe_zone": "Underground Metro Station 4"},
            {"title": "Cyclone Warning", "loc": "Chennai, Tamil Nadu", "risk": 88, "time": "5 mins ago", "color": "#f43f5e", "icon": "🌪️", "badge": "CRITICAL", "safe_zone": "City Hall Basement"},
            {"title": "Heatwave", "loc": "Jaipur, Rajasthan", "risk": 65, "time": "3 hours ago", "color": "#f97316", "icon": "☀️", "badge": "HIGH", "safe_zone": "Central Hospital Emergency Wing"},
            {"title": "Landslide", "loc": "Shimla, Himachal Pradesh", "risk": 30, "time": "5 hours ago", "color": "#22c55e", "icon": "⛰️", "badge": "LOW", "safe_zone": "Evacuation Center Beta"}
        ]

def inject_custom_css():
    st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    /* Base Styling */
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Global App Background Fade (SVG Style) */
    .stApp {
        background: linear-gradient(135deg, #090a0f 0%, #1a1525 50%, #05161e 100%) !important;
        background-attachment: fixed !important;
    }

    .reportview-container {
        background: transparent !important;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Global Animations */
    @keyframes fadeInSlideUp {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulseGlowRed {
        0% { box-shadow: 0 0 10px rgba(255, 75, 75, 0.2); }
        50% { box-shadow: 0 0 25px rgba(255, 75, 75, 0.6); transform: scale(1.01); }
        100% { box-shadow: 0 0 10px rgba(255, 75, 75, 0.2); }
    }

    /* Apply animations to main container */
    .block-container {
        animation: fadeInSlideUp 0.7s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
    }

    /* Original Styling Rules to preserve padding/text layout */
    .metric-card {
        background: linear-gradient(145deg, rgba(20, 22, 28, 0.8) 0%, rgba(30, 33, 39, 0.5) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        padding: 25px;
        border-radius: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px 0 rgba(0, 229, 255, 0.3), 0 0 20px rgba(0, 229, 255, 0.2);
        border: 1px solid rgba(0, 229, 255, 0.5);
    }
    
    .danger-zone {
        animation: pulseGlowRed 2.5s infinite;
        transition: all 0.4s ease-in-out;
    }

    .feed-item-fake, .feed-item-real, .feed-item-alert, .feed-item-help {
        padding: 18px;
        margin-bottom: 15px;
        color: #f8f9fa;
        font-size: 0.95em;
        background: linear-gradient(135deg, rgba(20, 22, 28, 0.8) 0%, rgba(30, 33, 39, 0.5) 100%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease;
    }
    
    .feed-item-fake:hover, .feed-item-real:hover, .feed-item-alert:hover, .feed-item-help:hover {
        transform: translateX(8px) scale(1.01);
        box-shadow: -5px 8px 20px rgba(0,0,0,0.4);
    }
    
    .feed-item-fake { border-left: 5px solid #ff2a2a; }
    .feed-item-real { border-left: 5px solid #00e5ff; }
    .feed-item-alert { border-left: 4px solid #ff2a2a; }
    .feed-item-help { border-left: 4px solid #00e5ff; }
    
    /* Interactive Streamlit Buttons */
    div.stButton > button {
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
    }
    div.stButton > button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 6px 20px rgba(0, 229, 255, 0.25) !important;
        border-color: rgba(0, 229, 255, 0.4) !important;
    }
    div.stButton > button:active {
        transform: translateY(1px) !important;
    }

    /* Keep streamit components above the raw background but below the darkness layer */
    .appview-container, .stApp {
        z-index: 1;
        position: relative;
        background-color: transparent !important;
    }
</style>
""", unsafe_allow_html=True)
