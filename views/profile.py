import streamlit as st

st.title("👤 My Profile")
st.markdown("Your personal details and survival history.")

# Fetch Data
current_user_name = st.session_state.get('current_user_name', 'Unknown User')
current_blood = st.session_state.get('current_user_blood', 'Unknown')

# Top Gamified Stats
st.markdown("### 👋 Guardian Dashboard")
cols = st.columns(3)
with cols[0]:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color: #00e5ff;">Citizen Alias</p>
        <h3 style="margin: 0;">{current_user_name}</h3>
    </div>
    """, unsafe_allow_html=True)
with cols[1]:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color: #00cc96;">Trust Score</p>
        <h3 style="margin: 0;">92/100</h3>
    </div>
    """, unsafe_allow_html=True)
with cols[2]:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color: #ffbb00;">Reports Verified</p>
        <h3 style="margin: 0;">14</h3>
    </div>
    """, unsafe_allow_html=True)

st.write("") # Spacer

# Boxed Layouts
col_info, col_history = st.columns([1, 1.5])

with col_info:
    with st.container(border=True):
        st.subheader("📋 Identity & Health")
        st.divider()
        st.markdown(f"**Full Name:**<br>{current_user_name}", unsafe_allow_html=True)
        st.markdown(f"**Blood/Medical Type:**<br><span style='color: #ff4b4b; font-weight: bold;'>{current_blood}</span>", unsafe_allow_html=True)
        st.markdown("**Emergency Contact:**<br>+91 98765 43210 (Local Response Team)", unsafe_allow_html=True)
        st.markdown("**Primary Zone:**<br>Sector 4, Main Grid", unsafe_allow_html=True)

with col_history:
    with st.container(border=True):
        st.subheader("🛡️ Survival & Action Log")
        st.divider()
        history = st.session_state.get('survival_history', [])
        if not history:
             st.info("No recorded emergencies in your sector.")
        for event in reversed(history):
            if "Safe" in event:
                st.markdown(f"<div class='feed-item-real' style='margin-bottom: 10px;'>{event}</div>", unsafe_allow_html=True)
            else:
                 st.markdown(f"<div class='feed-item-alert' style='margin-bottom: 10px;'>{event}</div>", unsafe_allow_html=True)

