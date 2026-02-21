import streamlit as st
import requests
import base64
import streamlit.components.v1 as components

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

bg_img = get_base64_of_bin_file('/Users/himeshdheeraj/.gemini/antigravity/brain/452c3977-9c19-4aa8-a240-c81579b67f21/media__1771638023418.jpg')

components.html(f"""
<script>
    const doc = window.parent.document;
    if (!doc.getElementById('login-bg-style')) {{
        const style = doc.createElement('style');
        style.id = 'login-bg-style';
        style.innerHTML = `
            /* Full-Screen Login Background */
            .stApp > header {{
                background-color: transparent !important;
            }}
            .stApp {{
                background: url("data:image/jpeg;base64,{bg_img}") no-repeat !important;
                background-position: center center !important;
                background-size: cover !important;
                background-attachment: fixed !important;
            }}
        `;
        doc.head.appendChild(style);
    }}
</script>
""", height=0, width=0)

st.markdown("""
<style>
    /* Darken main container for readability */
    .block-container {
        background: rgba(10, 15, 25, 0.85) !important;
        border-radius: 20px !important;
        padding: 40px !important;
        margin-top: 50px !important;
        box-shadow: 0 0 50px rgba(0, 229, 255, 0.2) !important;
        max-width: 800px !important;
    }
</style>
""", unsafe_allow_html=True)
st.title("🛡️ PanicShield & Predictor Login")
st.markdown("Community-driven disaster intelligence network. Please log in to access your Citizen Portal and Emergency feeds.")

with st.form("login_form"):
    st.subheader("Login to your account")
    username = st.text_input("Full Name / Citizen ID", placeholder="e.g. Jane Doe")
    password = st.text_input("Password", type="password", help="Use any password for demo")
    
    submitted = st.form_submit_button("Enter PanicShield & Predictor", type="primary", use_container_width=True)
    if submitted:
        if username.strip() == "" or password.strip() == "":
            st.error("Please enter both Username and Password.")
        else:
            try:
                import requests
                import time
                response = requests.post("http://localhost:3001/login", json={
                    "username": username,
                    "password": password
                })
                
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"Welcome back, {data['user']['username']}! Initializing secure connection...")
                    st.session_state['logged_in'] = True
                    st.session_state['current_user_name'] = data['user']['username']
                    st.session_state['current_user_blood'] = data['user']['blood_type']
                    time.sleep(1)
                    st.rerun()
                elif response.status_code == 401:
                    st.error("Invalid credentials. Please check your spelling or Register.")
                else:
                    st.error(f"Login failed: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error("Could not connect to Authentication Server. Is it running?")

st.markdown("---")
cols = st.columns(3)
cols[0].info("🧠 AI-Powered Panic Detection")
cols[1].warning("🗺️ Real-Time Crowd Heatmaps")
cols[2].success("🤝 Verified Volunteer Networking")
