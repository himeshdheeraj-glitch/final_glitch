import streamlit as st
import random
import pandas as pd

def generate_social_media_sentiment():
    scenarios = ['Help', 'Fire', 'Running', 'Trapped', 'Scared', 'Evacuating', 'Stampede', 'Water rising', 'Gas leak']
    if random.random() > 0.7:
        sentiment = random.randint(60, 100)
        tweet = f"URGENT: {random.choice(scenarios)} in the city center! #crisis"
    else:
        sentiment = random.randint(10, 50)
        tweet = f"We are {random.choice(['Safe', 'Okay', 'waiting for help', 'sheltered'])} for now. #update"
    return sentiment, tweet

def generate_crowd_movement():
    if random.random() > 0.8:
        return random.randint(70, 100)
    else:
        return random.randint(10, 40)

def generate_comm_spikes():
    calls_per_sec = random.randint(10, 500)
    normalized = min((calls_per_sec / 500) * 100, 100)
    return normalized, calls_per_sec

def generate_viral_media():
    # Simulate a viral reel or news post popping up
    subjects = [
        "Massive explosion reported", "Free water distribution", "Armed forces arriving", 
        "All flights cancelled", "Shelter is full", "Bridge collapsed", "Power grid failure",
        "Tsunami warning sirens", "Toxic smoke spreading", "Looting at the supermarket"
    ]
    locations = [
        "Bandra Kurla Complex", "Connaught Place", "Indiranagar", "T Nagar", "Park Street",
        "Howrah Bridge", "Marine Drive", "Old Delhi", "Cyber City", "Andheri West"
    ]
    
    msg = f"VIRAL REEL: {random.choice(subjects)} near {random.choice(locations)}!"
    
    # AI Classification Mock
    is_fake = random.random() > 0.4 # 60% chance it's flagged as fake news in chaos
    confidence = random.randint(70, 99)
    
    classification = "FAKE NEWS DETECTED" if is_fake else "VERIFIED REAL"
    return msg, classification, confidence

def calculate_panic_score(sentiment, movement, comms):
    # Base formula
    raw_score = (0.35 * sentiment) + (0.40 * movement) + (0.15 * comms) + (0.10 * random.randint(20, 80))
    
    # Store raw score in session state for moving average calculation
    if 'raw_scores_history' not in st.session_state:
        st.session_state['raw_scores_history'] = []
    
    st.session_state['raw_scores_history'].append(raw_score)
    # Keep last 5 ticks for a smooth 5-second moving average
    st.session_state['raw_scores_history'] = st.session_state['raw_scores_history'][-5:]
    
    # Calculate smoothed score
    smoothed_score = sum(st.session_state['raw_scores_history']) / len(st.session_state['raw_scores_history'])
    
    # *** THE WOW FACTOR LOGIC ***
    # If the user marked themselves safe, drastically reduce the simulated panic score
    # to show the "Ripple Effect" of community reporting
    if st.session_state.get('user_safe', False):
         smoothed_score = smoothed_score * 0.4 # Reduce score by 60%
        
    return min(100, round(smoothed_score, 2))

def simulation_tick():
    if not st.session_state.get('sim_running', False):
        return None
        
    current_time = pd.Timestamp.now().strftime("%H:%M:%S")
    sentiment_score, latest_tweet = generate_social_media_sentiment()
    movement_score = generate_crowd_movement()
    comm_score_norm, raw_calls = generate_comm_spikes()
    
    panic_score = calculate_panic_score(sentiment_score, movement_score, comm_score_norm)
    
    # Update History
    regions = ['Global Simulator (India)', 'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata']
    # For simulation, we'll assign this tick's primary action to a random region
    active_region = random.choice(regions[1:])
    
    new_data = pd.DataFrame({
        'Time': [current_time],
        'Region': [active_region],
        'Panic_Score': [panic_score],
        'Sentiment': [sentiment_score],
        'Movement': [movement_score],
        'Comms': [comm_score_norm]
    })
    st.session_state['history'] = pd.concat([st.session_state['history'], new_data]).tail(100) # Increased tail to keep history across regions
    
    # Dynamic Danger Zone Logic
    if panic_score > 75:
        st.session_state['user_in_danger_zone'] = True
        
        # Generate an AI recommended safe zone if one isn't currently active
        if 'current_safe_zone' not in st.session_state or st.session_state.get('user_safe', False):
            safe_zones = ["Highland High School Gym", "Underground Metro Station 4", "City Hall Basement", "Community Center Alpha", "Westside Stadium", "Central Hospital Emergency Wing"]
            st.session_state['current_safe_zone'] = random.choice(safe_zones)
            st.session_state['current_disaster_type'] = latest_tweet.split(":")[1].split("in")[0].strip() if ":" in latest_tweet else "Unknown Hazard"
            
        if random.random() > 0.5: # Don't flood alerts
            trigger_msg = f"🔴 {current_time}: RED ALERT - Score {panic_score}! Tweet: '{latest_tweet}'"
            st.session_state['alerts'].insert(0, trigger_msg)
            
            # Map risk to aesthetic badge
            disaster_type = st.session_state['current_disaster_type']
            safe_zone = st.session_state['current_safe_zone']
            color = "#f43f5e" if panic_score > 85 else "#f97316"
            badge = "CRITICAL" if panic_score > 85 else "HIGH"
            
            icon = "⚠️"
            if "Fire" in disaster_type: icon = "🔥"
            elif "Flood" in disaster_type or "Water" in disaster_type: icon = "🌊"
            elif "Stampede" in disaster_type or "Running" in disaster_type: icon = "🏃"
            
            new_disaster = {
                "title": disaster_type,
                "loc": active_region,
                "risk": panic_score,
                "time": current_time,
                "color": color,
                "icon": icon,
                "badge": badge,
                "safe_zone": safe_zone
            }
            # Maintain a rolling list of the top active disasters globally
            if 'active_disasters' not in st.session_state: st.session_state['active_disasters'] = []
            st.session_state['active_disasters'].insert(0, new_disaster)
            st.session_state['active_disasters'] = st.session_state['active_disasters'][:12] # Keep UI clean
            
    st.session_state['alerts'] = st.session_state['alerts'][:10]
    
    # Occasionally generate a viral news item
    if 'viral_news' not in st.session_state:
        st.session_state['viral_news'] = []
        
    if random.random() > 0.85: # 15% chance per tick
         msg, classification, confidence = generate_viral_media()
         
         style_class = "feed-item-fake" if "FAKE" in classification else "feed-item-real"
         color = "#ff4b4b" if "FAKE" in classification else "#00cc96"
         
         formatted_news = f"""
         <div class='{style_class}' style='border-left-color: {color};'>
            <div style='display:flex; justify-content:space-between; margin-bottom: 5px;'>
                <span style='font-size: 0.8em; color: #888;'>{current_time}</span>
                <span style='font-size: 0.8em; font-weight: bold; color: {color};'>AI STATUS: {classification} ({confidence}%)</span>
            </div>
            <strong>{msg}</strong>
         </div>
         """
         st.session_state['viral_news'].insert(0, formatted_news)
         st.session_state['viral_news'] = st.session_state['viral_news'][:4] # Keep last 4
         
    return panic_score, sentiment_score, movement_score, raw_calls
