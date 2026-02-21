import streamlit as st
import time
from utils.sim import simulation_tick

st.title("🤝 Trusted Volunteer Network")
st.markdown("Community-driven disaster intelligence. Highly rated users become trusted reporters.")

simulation_tick()

st.subheader("Top Ranked Volunteers (Your Area)")

# Filters
all_skills = set()
for s in st.session_state['volunteers']['Skills']:
    all_skills.update(s.split(', '))

selected_skills = st.multiselect("Filter by Skill:", options=list(all_skills))

# Filter dataframe
df_vol = st.session_state['volunteers'].copy()
if selected_skills:
    # Keep row if it has AT LEAST one of the selected skills
    mask = df_vol['Skills'].apply(lambda x: any(skill in x for skill in selected_skills))
    df_vol = df_vol[mask]

# Display Volunteer Roster
st.dataframe(
    df_vol,
    column_config={
        "Trust_Score": st.column_config.ProgressColumn("Trust Score", format="%f", min_value=0, max_value=100),
        "Status": st.column_config.TextColumn("Availability"),
        "Last_Active": st.column_config.TextColumn("Last Active"),
        "Location": st.column_config.TextColumn("Current Location"),
        "lat": None,
        "lon": None
    },
    hide_index=True,
    use_container_width=True
)

st.markdown("---")
col_mission, col_ai = st.columns([1, 1])

with col_mission:
    st.subheader("📋 Mission Task Board")
    st.info("Medical Assistance needed at Dharavi (Priority: HIGH)")
    st.warning("Supply Logistical Support needed at Connaught Place (Priority: MEDIUM)")
    st.error("Search & Rescue needed at Howrah Bridge (Priority: CRITICAL)")

with col_ai:
    st.subheader("🧠 AI Smart Assignment System")
    st.markdown("""
    **Auto-Routing Active...**
    * AI scanning for 🟢 *Available* status.
    * Matching proximity and `Skills` required for open tasks.
    """)
    if st.button("Run Smart Assignment Route"):
        st.success("🤖 Assigned @SarahO (Medical) to Dharavi.")
        st.success("🤖 Assigned @MikeT (Logistics) to Connaught Place.")

st.markdown("---")
st.subheader("My Volunteer Status")
col1, col2 = st.columns(2)
with col1:
    st.info("Current Trust Score: **65/100**")
    st.markdown("Submit more accurate reports via the Citizen Portal to increase your rank and gain *Trusted Reporter* status.")
with col2:
     st.warning("⚠️ Status: **Standard User** (Requires score 80+ for Trusted)")

if st.session_state.get('sim_running', False):
    time.sleep(1)
    st.rerun()
