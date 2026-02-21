import streamlit as st
import time
import pandas as pd
from utils.sim import simulation_tick

st.title("📡 Citizen Action Portal")
st.markdown("Your active crisis response tools and intelligence reporting hub.")

current_user_name = st.session_state.get('current_user_name', 'Unknown User')

simulation_tick()

st.subheader("Current Safety Status")
with st.spinner("Scanning regional perimeter and cross-referencing active threat intel..."):
    time.sleep(1.0)
    
# State variables to manage the persistent display
if 'danger_acknowledged' not in st.session_state:
     st.session_state['danger_acknowledged'] = False
     
# The user is in danger, and they haven't explicitly marked safe or dismissed it
if st.session_state.get('user_in_danger_zone', False) and not st.session_state.get('user_safe', False) and not st.session_state['danger_acknowledged']:
    
    # Initialize the timer if this is the first time seeing it
    if st.session_state.get('danger_alert_time') is None:
        st.session_state['danger_alert_time'] = time.time()
        
    time_elapsed = time.time() - st.session_state['danger_alert_time']
    
    # 10 second timeout logic
    if time_elapsed > 10:
        st.session_state['danger_acknowledged'] = True
        current_time = pd.Timestamp.now().strftime("%H:%M:%S")
        st.session_state['survival_history'].append(f"⚠️ **Incident {current_time}** - No Response (Timeout)")
        st.rerun()
        
    time_remaining = int(10 - time_elapsed)
        
    disaster_type = st.session_state.get('current_disaster_type', 'Unknown Hazard')
    safe_zone = st.session_state.get('current_safe_zone', 'Nearest Designated Shelter')
    
    st.markdown(f"""
    <div class="danger-zone" style="background: rgba(255, 75, 75, 0.1); border: 2px solid #ff4b4b; padding: 20px; border-radius: 12px; margin-bottom: 20px;">
        <h3 style='color: #ff4b4b; margin: 0 0 10px 0;'>⚠️ EXTREME DANGER DETECTED IN YOUR ZONE</h3>
        <p>We are detecting severe crowd anomalies and panic levels near your location due to a suspected <b>{disaster_type}</b>.</p>
        
        <div style="background: #111; padding: 15px; border-left: 4px solid #00e5ff; margin: 15px 0; border-radius: 4px;">
            <p style="color: #00e5ff; font-weight: bold; margin: 0 0 5px 0;">🤖 AI Evacuation Recommendation</p>
            <p style="margin: 0;">Cross-referencing disaster type and current crowd density, your safest route is to proceed immediately to: <br>
            <span style="font-size: 1.2em; font-weight: bold; color: white;">📍 {safe_zone}</span></p>
        </div>
        
        <p>Evacuate if possible, or mark yourself safe to help authorities coordinate.</p>
        <p style='color: #ff4b4b; font-weight: bold;'>Time remaining to respond: {time_remaining}s</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action Buttons
    col_safe, col_dismiss = st.columns(2)
    with col_safe:
        if st.button("🚨 MARK AS SAFE", use_container_width=True, type="primary"):
            st.session_state['user_safe'] = True
            current_time = pd.Timestamp.now().strftime("%H:%M:%S")
            st.session_state['survival_history'].append(f"🛡️ **Incident {current_time}** - Marked Safe")
            st.session_state['danger_alert_time'] = None # Reset timer
            st.rerun()
    with col_dismiss:
         if st.button("Dismiss Alert", use_container_width=True):
             st.session_state['danger_acknowledged'] = True
             st.session_state['danger_alert_time'] = None # Reset timer
             st.rerun()
             
# They clicked Mark Safe
elif st.session_state.get('user_safe', False):
    st.markdown("""
    <div style='background-color: #00cc96; color: white; padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px;'>
        <h3>✅ YOU ARE MARKED SAFE</h3>
        <p>Thank you for reporting. Your status helps authorities prioritize resources to those in need.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Reset Status (Demo)", use_container_width=True):
         st.session_state['user_safe'] = False
         st.session_state['danger_acknowledged'] = False
         st.session_state['user_in_danger_zone'] = False
         st.session_state['danger_alert_time'] = None
         
# Not in danger, or they dismissed the prompt
else:
     st.success("✅ No immediate threats detected in your area.")
     if st.session_state.get('history') is not None and len(st.session_state['history']) > 0 and st.session_state['history'].iloc[-1]['Panic_Score'] > 75:
           if st.button("Re-evaluate Threat Level", use_container_width=True):
               st.session_state['danger_acknowledged'] = False
               st.session_state['user_in_danger_zone'] = True 
               st.session_state['danger_alert_time'] = None
               st.rerun()

st.markdown("---")
st.subheader("🌍 Global Active Alerts & Evacuation")
st.markdown("Based on current active alerts, the AI recommends the following safe zones for affected regions.")

st.markdown("""
<style>
.alert-card-custom {
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease;
}
.alert-card-custom:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 15px 30px rgba(0,0,0,0.15) !important;
}
</style>
""", unsafe_allow_html=True)

def render_alert_card(title, location, risk, time, color_hex, emotion, badge_text, safe_zone):
    html = f"""
    <div class="alert-card-custom" style="background-color: #ffffff; border-radius: 16px; padding: 24px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); color: #1a1a1a; font-family: 'Inter', sans-serif; margin-bottom: 20px; border: 1px solid #f0f0f0;">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 16px;">
            <div style="background-color: {color_hex}15; height: 40px; width: 40px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px;">
                {emotion}
            </div>
            <span style="color: {color_hex}; font-weight: 800; font-size: 11px; letter-spacing: 0.5px;">{badge_text}</span>
        </div>
        <h3 style="margin: 0 0 4px 0; font-size: 18px; font-weight: 700; color: #111;">{title}</h3>
        <div style="color: #666; font-size: 13px; margin-bottom: 24px;">📍 {location}</div>
        <div style="margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 13px; color: #555; font-weight: 500;">Risk Probability</span>
            <span style="font-size: 14px; color: {color_hex}; font-weight: 700;">{risk}%</span>
        </div>
        <div style="background-color: #f0f0f0; height: 6px; width: 100%; border-radius: 4px; margin-bottom: 16px; overflow: hidden;">
            <div style="background-color: {color_hex}; height: 100%; width: {risk}%; border-radius: 4px;"></div>
        </div>
        <div style="color: #888; font-size: 12px; margin-bottom: 10px;">🕒 {time}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    
    # Adding interactive Streamlit buttons right below the card
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        details_clicked = st.button("View Details", key=f"details_{title}_{location}", use_container_width=True)
    with btn_col2:
        safe_clicked = st.button("✔️ Mark Safe", key=f"safe_{title}_{location}", use_container_width=True)
        
    if safe_clicked:
        entry = f"🛡️ **{title} ({location})** - Marked Safe"
        if entry not in st.session_state['survival_history']:
            st.session_state['survival_history'].append(entry)
        st.toast(f"You have been marked safe in {location}!")
        
    if details_clicked:
        with st.expander(f"Intelligence Report: {title}", expanded=True):
            st.write(f"**Location:** {location}")
            st.write(f"**Last Update:** {time}")
            st.write(f"**AI Risk Consensus:** {risk}%")
            st.markdown(f"**AI Recommended Evacuation Route:** ➡️ <span style='color:#00cc96; font-weight:bold;'>{safe_zone}</span>", unsafe_allow_html=True)
            st.info("Emergency services and volunteer networks have been notified. Evacuation protocols are on standby.")


active_disasters = st.session_state.get('active_disasters', [])
if not active_disasters:
    st.info("Waiting for the first intelligence batch from the simulation engine...")
else:
    # Create Grid Layout
    col1, col2, col3 = st.columns(3)

    for i, alert in enumerate(active_disasters):
        with [col1, col2, col3][i % 3]:
            render_alert_card(
                title=alert.get("title", "Hazard"),
                location=alert.get("loc", "Unknown"),
                risk=alert.get("risk", 0),
                time=alert.get("time", "Now"),
                color_hex=alert.get("color", "#ff4b4b"),
                emotion=alert.get("icon", "⚠️"),
                badge_text=alert.get("badge", "ALERT"),
                safe_zone=alert.get("safe_zone", "Nearest Configured Shelter")
            )
         

if st.session_state.get('sim_running', False):
    time.sleep(5)
    st.rerun()
