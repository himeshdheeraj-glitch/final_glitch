import streamlit as st
import requests
import base64
import time
import streamlit.components.v1 as components

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

bg_img = get_base64_of_bin_file('/Users/himeshdheeraj/.gemini/antigravity/brain/452c3977-9c19-4aa8-a240-c81579b67f21/media__1771638115489.jpg')

components.html(f"""
<script>
    const doc = window.parent.document;
    if (!doc.getElementById('register-bg-style')) {{
        const style = doc.createElement('style');
        style.id = 'register-bg-style';
        style.innerHTML = `
            /* Full-Screen Register Background */
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
        background: rgba(10, 20, 15, 0.85) !important;
        border-radius: 20px !important;
        padding: 40px !important;
        margin-top: 50px !important;
        box-shadow: 0 0 50px rgba(0, 255, 150, 0.2) !important;
        max-width: 800px !important;
    }
</style>
""", unsafe_allow_html=True)
st.title("📝 PanicShield & Predictor Registration")
st.markdown("Join the community-driven disaster intelligence network.")

with st.form("register_form"):
    st.subheader("Create a new account")
    username = st.text_input("Full Name", placeholder="e.g. John Smith")
    email = st.text_input("Email Address", placeholder="name@example.com")
    blood_type = st.selectbox("Medical Info: Blood Type (Optional)", ["Unknown", "O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"])
    password = st.text_input("Create Password", type="password")
    
    submitted = st.form_submit_button("Create Account", type="primary", use_container_width=True)
    if submitted:
        if username.strip() == "":
            st.error("Please enter a valid Name.")
        else:
            try:
                import requests
                response = requests.post("http://localhost:3001/register", json={
                    "username": username,
                    "email": email,
                    "blood_type": blood_type,
                    "password": password
                })
                
                if response.status_code == 201:
                    data = response.json()
                    st.success(f"Account created for {username}! You can now access the system.")
                    st.session_state['logged_in'] = True
                    st.session_state['current_user_name'] = data['user']['username']
                    st.session_state['current_user_blood'] = data['user']['blood_type']
                    time.sleep(1) # small delay to show success message
                    st.rerun()
                elif response.status_code == 409:
                    st.error("This username or email is already registered. Please Log In.")
                else:
                    st.error(f"Registration failed: {response.json().get('error', 'Unknown error')}")
            except requests.exceptions.RequestException as e:
                st.error("Could not connect to Authentication Server. Is it running?")

st.markdown("Already have an account? Use the Navigation to go to **Log In**.")
