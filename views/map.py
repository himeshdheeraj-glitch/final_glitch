import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import random
import time
from utils.sim import simulation_tick

st.title("🗺️ Smart Interactive Map")
st.markdown("Visualizing crowd density and identifying abnormal gatherings via mobile signal density.")

simulation_tick() # Keep data moving

# Extract a global risk and density proxy from the simulation state
global_risk = 0
active_signals_density = 0

if len(st.session_state['history']) > 0:
    global_risk = int(st.session_state['history'].iloc[-1]['Panic_Score'])
    
# Estimate a daily density (just scaling the base simulation factor)
daily_density = int(global_risk * 1500) + random.randint(1000, 5000)

# Display Top Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="📊 Active Spot Density", value=f"{int(global_risk * 45)} signals", delta=f"{random.randint(-15, 30)} in last hour")
with col2:
    st.metric(label="⚠️ Aggregate Zone Risk", value=f"{global_risk}%", delta=f"{global_risk - 20}% vs avg", delta_color="inverse")
with col3:
    st.metric(label="📈 Daily Density (Est.)", value=f"{daily_density:,}", delta=f"+{random.randint(100, 500)} today")

st.markdown("---")

# Static Zones (India)
zones = [
    {"name": "Mumbai", "lat": 19.0596, "lon": 72.8295, "base_risk": 30},
    {"name": "Delhi", "lat": 28.6315, "lon": 77.2167, "base_risk": 25},
    {"name": "Bangalore", "lat": 12.9784, "lon": 77.6408, "base_risk": 15},
    {"name": "Chennai", "lat": 13.0405, "lon": 80.2337, "base_risk": 10},
    {"name": "Kolkata", "lat": 22.5513, "lon": 88.3524, "base_risk": 20}
]

_run_interval = 0.2 if st.session_state.get('sim_running', False) else None

@st.fragment(run_every=_run_interval)
def render_live_map():
    # Calculate live risk for each zone based on the global panic score modifier
    global_modifier = 1.0
    if len(st.session_state['history']) > 0:
         # Use the global panic score to affect the primary zone (e.g. Sector A) more than others
         global_score = st.session_state['history'].iloc[-1]['Panic_Score']
         global_modifier = global_score / 50.0 
         
    map_data = []
    for i, z in enumerate(zones):
         # Primary zone takes the brunt of the global score for demo
         live_risk = min(100, z['base_risk'] * (global_modifier if i == 0 else random.uniform(0.8, 1.2)))
         
         # Color Logic: RGB array
         if live_risk > 75:
             color = [255, 75, 75, 200]  # RED (Critical)
         elif live_risk > 40:
             color = [255, 204, 0, 200]  # YELLOW (Medium)
         else:
             color = [0, 204, 150, 200]  # GREEN (Safe)
             
         map_data.append({
             "zone": z['name'],
             "lat": z['lat'],
             "lon": z['lon'],
             "risk_score": int(live_risk),
             "color": color,
             "radius": 50000 + (live_risk * 1500) # Reverted to India-scale circle radius
         })
         
    df_map = pd.DataFrame(map_data)

    # Layer 1: Scatterplot circles
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        df_map,
        get_position=["lon", "lat"],
        get_color="color",
        get_radius="radius",
        pickable=True,
        opacity=0.8,
        filled=True,
    )

    # Set view state to focus strictly on India
    view_state = pdk.ViewState(
        latitude=20.5937,
        longitude=78.9629,
        zoom=4.0,
        pitch=0,
    )

    st.pydeck_chart(pdk.Deck(
        layers=[scatter_layer],
        initial_view_state=view_state,
        api_keys=None, # Ensure it doesn't try to look for missing mapbox keys
        map_style=pdk.map_styles.CARTO_DARK, # Use open source Carto style
        tooltip={"text": "Zone: {zone}\nRisk Score: {risk_score}/100"}
    ))

# Call the fragment to render
render_live_map()
st.info("💡 **Heatmap Legend**: Red/Yellow areas indicate high mobile signal density and potential stampede zones.")
