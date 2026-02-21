import streamlit as st
import plotly.express as px
import time
from utils.sim import simulation_tick

st.title("🚨 PanicShield & Predictor Emergency Dashboard")
st.markdown("Central authority view for real-time panic prediction and response coordination.")

metrics_placeholder = st.empty()
charts_placeholder = st.empty()

# Run a tick
res = simulation_tick()
if res:
     panic_score, sentiment_score, movement_score, raw_calls = res
else:
    # Get latest from history if exists, else defaults
    if len(st.session_state['history']) > 0:
        latest = st.session_state['history'].iloc[-1]
        panic_score, sentiment_score, movement_score, raw_calls = latest['Panic_Score'], latest['Sentiment'], latest['Movement'], 200
    else:
         panic_score, sentiment_score, movement_score, raw_calls = 0, 0, 0, 0

with metrics_placeholder.container():
    cols = st.columns(4)
    
    with cols[0]:
        st.markdown(f"""
        <div class="metric-card">
            <p>Social Fear Index</p>
            <p class="metric-value" style="color: {'#ff4b4b' if sentiment_score > 70 else '#00cc96'}">{int(sentiment_score)}/100</p>
        </div>
        """, unsafe_allow_html=True)
        
    with cols[1]:
        st.markdown(f"""
        <div class="metric-card">
            <p>Crowd Anomaly</p>
            <p class="metric-value" style="color: {'#ff4b4b' if movement_score > 70 else '#00cc96'}">{int(movement_score)}/100</p>
        </div>
        """, unsafe_allow_html=True)
        
    with cols[2]:
         st.markdown(f"""
        <div class="metric-card">
            <p>Comm Spikes (calls/s)</p>
            <p class="metric-value" style="color: {'#ff4b4b' if raw_calls > 300 else '#00cc96'}">{int(raw_calls)}</p>
        </div>
        """, unsafe_allow_html=True)

    with cols[3]:
        alert_class = "red-alert" if panic_score > 75 else ""
        st.markdown(f"""
        <div class="metric-card" style="border-color: {'#ff4b4b' if panic_score > 75 else '#333'}">
            <p style="color: {'#ff4b4b' if panic_score > 75 else 'white'}">GLOBAL PANIC SCORE</p>
            <p class="metric-value {alert_class}" style="color: {'#ff4b4b' if panic_score > 75 else '#00cc96'}">{int(panic_score)}</p>
        </div>
        """, unsafe_allow_html=True)

with charts_placeholder.container():
    st.markdown("<br>", unsafe_allow_html=True)
    col_chart, col_feed = st.columns([2, 1])
    
    with col_chart:
        st.subheader("Panic Escalation Trend (Last 5 Seconds)")
        
        # Region Filter selector
        valid_regions = ['Global Simulator (India)', 'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata']
        selected_region = st.selectbox("Select Regional Lens:", valid_regions, index=0, key="region_filter")
        
        if len(st.session_state['history']) > 1:
            # Filter the dataframe for the chart based on the dropdown
            plot_df = st.session_state['history'].copy()
            if selected_region != "Global Simulator (India)":
                plot_df = plot_df[plot_df['Region'] == selected_region]
                
            if len(plot_df) > 1:
                fig = px.line(plot_df, x='Time', y='Panic_Score', 
                              range_y=[0, 100], 
                              color_discrete_sequence=['#ff4b4b'])
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                                  font_color='white', margin=dict(l=0, r=0, t=10, b=0),
                                  xaxis_title="", yaxis_title="Score")
                fig.add_hline(y=75, line_dash="dash", line_color="red", annotation_text="RED ALERT")
                st.plotly_chart(fig, use_container_width=True, key=f"line_chart_{time.time()}_{selected_region}")
            else:
                 st.info(f"Gathering intel for {selected_region}... waiting for next simulation tick.")
            
    with col_feed:
        st.subheader("Crisis Intelligence Feed")
        if st.session_state['alerts']:
            for alert in st.session_state['alerts'][:5]:
                st.markdown(f"<div class='feed-item-alert'>{alert}</div>", unsafe_allow_html=True)
        else:
            st.info("No active alerts.")
            
        if st.session_state['help_messages']:
            st.markdown("---")
            st.markdown("🆘 **Live Help Requests**")
            for msg in st.session_state['help_messages'][:3]:
                 st.markdown(f"<div class='feed-item-help'>{msg}</div>", unsafe_allow_html=True)
                 
        if st.session_state.get('viral_news'):
            st.markdown("---")
            st.markdown("""
            <div style='background: linear-gradient(90deg, rgba(66, 133, 244, 0.4) 0%, rgba(30,33,39,0.8) 100%); padding: 10px; border-radius: 8px; border-left: 5px solid #4285F4; margin-bottom: 15px;'>
                <h4 style='margin: 0; color: white;'>📱 AI Misinformation Radar</h4>
            </div>
            """, unsafe_allow_html=True)
            for news in st.session_state['viral_news']:
                 st.markdown(news, unsafe_allow_html=True)

st.markdown("---")
st.subheader("📝 Manual Intelligence Override")
st.markdown("Report localized or minor disasters that the AI simulation may not have detected yet.")
with st.expander("Submit a User-Sourced Disaster Report"):
    with st.form("manual_disaster_form", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            m_title = st.text_input("Disaster Type (e.g. Broken Water Main, Localized Fire)")
            m_loc = st.text_input("Specific Location")
        with col_f2:
            m_safe = st.text_input("Recommended Safe Zone", "Evacuate Immediate Area")
            m_risk = st.slider("Estimated Risk Level", 10, 100, 30)
            
        submitted = st.form_submit_button("Submit to Global Feed", type="primary")
        if submitted and m_title and m_loc:
            import datetime
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            color = "#f43f5e" if m_risk > 80 else ("#f97316" if m_risk > 50 else "#eab308")
            
            new_disaster = {
                "title": f"{m_title} (User Report)",
                "loc": m_loc,
                "risk": m_risk,
                "time": current_time,
                "color": color,
                "icon": "⚠️",
                "badge": "USER REPORT",
                "safe_zone": m_safe
            }
            if 'active_disasters' not in st.session_state:
                st.session_state['active_disasters'] = []
            st.session_state['active_disasters'].insert(0, new_disaster)
            st.session_state['active_disasters'] = st.session_state['active_disasters'][:12]
            st.success("Disaster successfully added to the global active alerts feed!")

if st.session_state.get('sim_running', False):
    time.sleep(5)
    st.rerun()
