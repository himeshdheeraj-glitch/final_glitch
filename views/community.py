import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.title("🏘️ Community Hub & Resource Exchange")
st.markdown("Connect directly with your local PanicShield community. Request resources, offer help, and coordinate directly with registered users.")

# --- Tab Setup ---
tab_board, tab_directory = st.tabs(["📢 Resource Message Board", "👥 Community Directory"])

# --- 1. Resource Message Board ---
with tab_board:
    st.subheader("Active Resource Requests & Offers")
    
    if 'community_posts' not in st.session_state:
        # Initialize with some mock data for the demo
        st.session_state['community_posts'] = [
            {"author": "Jane Doe", "type": "Need", "item": "Clean Water", "time": "10:15 AM", "contact": "jane@example.com", "desc": "We are out of clean water in Sector B. Can anyone safely deliver?"},
            {"author": "David L", "type": "Offer", "item": "First Aid Kit", "time": "09:30 AM", "contact": "david.l@panicshield.org", "desc": "I have a spare trauma kit and can travel within 2 miles of the City Center."}
        ]
        
    # --- New Post Form ---
    with st.expander("➕ Create a New Post", expanded=False):
        with st.form("new_post_form", clear_on_submit=True):
            post_type = st.radio("Post Type", ["Need Help / Request Resource", "Offer Help / Provide Resource"], horizontal=True)
            item_name = st.text_input("What is the primary resource? (e.g. Water, Blankets, Shelter)")
            description = st.text_area("Details and location instructions:")
            
            submitted = st.form_submit_button("Post to Community", type="primary")
            if submitted and item_name:
                new_post = {
                    "author": st.session_state.get('current_user_name', 'Unknown User'),
                    "type": "Need" if "Need" in post_type else "Offer",
                    "item": item_name,
                    "time": datetime.now().strftime("%I:%M %p"),
                    "contact": "Check Directory", # Simplification to encourage using directory
                    "desc": description
                }
                st.session_state['community_posts'].insert(0, new_post)
                st.success("Post successfully added to the board!")
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- Display Posts ---
    for post in st.session_state['community_posts']:
        bg_color = "#3b0711" if post['type'] == 'Need' else "#003325"
        border_color = "#ff4b4b" if post['type'] == 'Need' else "#00cc96"
        icon = "🆘 NEED" if post['type'] == 'Need' else "✅ OFFER"
        
        st.markdown(f"""
        <div style="background-color: {bg_color}; border-left: 5px solid {border_color}; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span style="font-weight: bold; color: {border_color};">{icon}: {post['item']}</span>
                <span style="font-size: 0.8em; color: #aaa;">{post['time']}</span>
            </div>
            <p style="margin: 5px 0;">{post['desc']}</p>
            <div style="font-size: 0.85em; color: #888; display: flex; justify-content: space-between; align-items: center;">
                <span>👤 <b>{post['author']}</b></span>
                <span style="background: rgba(255,255,255,0.1); padding: 3px 8px; border-radius: 4px;">Contact via Directory</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# --- 2. Community Directory ---
with tab_directory:
    st.subheader("Registered Community Members")
    
    try:
        from utils.auth import get_all_users
        users_list = get_all_users()
        
        if len(users_list) > 0:
            df_users = pd.DataFrame(users_list)
            # Cleanup the dataframe for display
            df_users = df_users.rename(columns={
                "username": "Full Name",
                "email": "Contact Email",
                "blood_type": "Medical/Blood Type"
            })
            
            st.dataframe(df_users, use_container_width=True, hide_index=True)
        else:
            st.info("No other users are currently registered in the database.")
    except Exception as e:
        st.error(f"Error fetching community members: {str(e)}")
