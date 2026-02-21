import streamlit as st
from utils.state import init_session_state, inject_custom_css

# Page config MUST be the first Streamlit command
st.set_page_config(page_title="PanicShield & Predictor | SafeSync", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

# Initialize global state and inject styling
init_session_state()
inject_custom_css()

import streamlit.components.v1 as components
components.html("""
<script>
    const doc = window.parent.document;
    if (!doc.getElementById('custom-cursor-glow-js')) {
        // Inject the exact CSS the user provided
        const style = doc.createElement('style');
        style.id = 'custom-cursor-glow-js';
        style.innerHTML = `
        :root {
          --mouse-x: 50%;
          --mouse-y: 50%;
        }
        .cursor-glow {
          position: fixed;
          top: 0;
          left: 0;
          width: 100vw;
          height: 100vh;
          pointer-events: none;
          z-index: 999999;
          background: radial-gradient(
            circle 400px at var(--mouse-x) var(--mouse-y), 
            rgba(0, 229, 255, 0.15),
            transparent 80%
          );
        }
        `;
        doc.head.appendChild(style);
        
        // Inject the html div the user provided
        const glow = doc.createElement('div');
        glow.className = 'cursor-glow';
        doc.body.appendChild(glow);
        
        // Inject the javascript listener the user provided
        doc.addEventListener('mousemove', (e) => {
            glow.style.setProperty('--mouse-x', `${e.clientX}px`);
            glow.style.setProperty('--mouse-y', `${e.clientY}px`);
        });
    }
</script>
""", height=0, width=0)

# Pages define setup
launch_page = st.Page("views/launch.py", title="Launch", icon="🚀", default=True)
login_page = st.Page("views/login.py", title="Log In", icon="🔑")
register_page = st.Page("views/register.py", title="Register", icon="📝")
dashboard_page = st.Page("views/dashboard.py", title="Emergency Dashboard", icon="🚨")
map_page = st.Page("views/map.py", title="Smart Interactive Map", icon="🗺️")
portal_page = st.Page("views/portal.py", title="Citizen Action & Alerts", icon="🌐")
profile_page = st.Page("views/profile.py", title="My Profile", icon="👤")
volunteer_page = st.Page("views/volunteer.py", title="Volunteer Network", icon="🤝")
community_page = st.Page("views/community.py", title="Community Hub", icon="🏘️")

if st.session_state['logged_in']:
    pg = st.navigation([dashboard_page, map_page, portal_page, volunteer_page, community_page, profile_page])
    
    # Hide the last nav item (Profile) from sidebar
    st.markdown("""
        <style>
        [data-testid="stSidebarNav"] ul li:last-child {
            display: none !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Profile button at top right of the main page
    c1, c2, c3 = st.columns([8, 1, 1])
    with c3:
        if st.button("👤 Profile", use_container_width=True):
            st.switch_page(profile_page)
    
    # Custom Sidebar content for authenticated users
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/813/813250.png", width=50) # simple shield icon
    st.sidebar.title(f"PanicShield & Predictor Hub")
    st.sidebar.markdown(f"**User**: {st.session_state['current_user_name']}")
    
    if st.sidebar.button("Log Out"):
         st.session_state['logged_in'] = False
         st.rerun()
else:
    # Unauthenticated router
    # Add login and register to the router but hide them from the sidebar
    pg = st.navigation([launch_page, login_page, register_page], position="hidden")

# Execute current page
pg.run()

