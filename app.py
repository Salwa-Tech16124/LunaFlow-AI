import streamlit as st
from datetime import date
import plotly.express as px
import pandas as pd

import time
from database import init_db, save_cycle, get_latest_cycle, get_all_cycles, save_symptoms, get_all_symptoms, save_chat_message, get_chat_history, clear_chat_history, save_water_log, get_water_log, get_notification_settings, save_notification_settings
from prediction import calculate_predictions, get_current_cycle_day, get_cycle_phase
from ui import apply_theme, metric_card, get_logo_svg, render_splash_screen
from utils.ai_assistant import get_sarvam_response
from database.users_db import init_users_db, get_user_profile, update_user_profile, save_fcm_token
from auth.login import render_login
from auth.signup import render_signup
from database.wellness_db import init_wellness_db, save_wellness_log, get_all_wellness_logs, get_latest_wellness_log
from utils.wellness import calculate_wellness_score, get_wellness_category, generate_simple_insights
from utils.tips import generate_wellness_tip

def stream_data(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.04)


st.set_page_config(
    page_title="LunaFlow AI",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# Initialize Database
init_users_db()
init_db()
init_wellness_db()

# Splash Screen Logic
if 'splash_shown' not in st.session_state:
    render_splash_screen()
    st.session_state.splash_shown = True

# Top right theme toggle
top_c1, top_c2 = st.columns([9, 1])
with top_c2:
    if st.session_state.theme == 'light':
        if st.button("🌙 Dark", key="btn_dark"):
            st.session_state.theme = 'dark'
            st.rerun()
    else:
        if st.button("☀️ Light", key="btn_light"):
            st.session_state.theme = 'light'
            st.rerun()

# Apply Theme
apply_theme(is_dark=(st.session_state.theme == 'dark'))

if 'user_id' not in st.session_state:
    st.markdown("<br><br>", unsafe_allow_html=True)
    l_col1, l_col2 = st.columns(2)
    
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'login'
        
    with l_col1:
        if st.button("Log In", use_container_width=True):
            st.session_state.auth_mode = 'login'
            st.rerun()
    with l_col2:
        if st.button("Sign Up", use_container_width=True):
            st.session_state.auth_mode = 'signup'
            st.rerun()
            
    st.markdown("---")
    if st.session_state.auth_mode == 'login':
        render_login()
    else:
        render_signup()
        
    st.stop() # STOP EXECUTION HERE IF NOT LOGGED IN

user_id = st.session_state.user_id

with st.sidebar:
    st.markdown(f"**Welcome, {st.session_state.user_name}**")
    if st.button("🚪 Logout", use_container_width=True):
        del st.session_state.user_id
        del st.session_state.user_name
        if "messages" in st.session_state:
            del st.session_state.messages
        st.rerun()


# Premium Hero Section
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(255,126,182,0.1) 0%, rgba(200,162,255,0.1) 100%); 
            padding: 40px; border-radius: 25px; text-align: center; margin-bottom: 30px; position: relative; overflow: hidden;
            border: 1px solid var(--border); box-shadow: 0 8px 32px rgba(0,0,0,0.05); animation: fadeIn 0.8s ease-out forwards;">
    <div style="font-size: 3.5rem; margin-bottom: 10px; text-shadow: 0 4px 15px rgba(255, 126, 182, 0.4);">🌙</div>
    <h1 style="font-size: 3.5rem; letter-spacing: -1px; margin-bottom: 10px; color: var(--primary) !important;">LunaFlow AI</h1>
    <p style="font-size: 1.2rem; color: var(--primary) !important; font-weight: 600; letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 8px;">Track • Predict • Understand</p>
    <p style="font-size: 1.1rem; color: var(--text-sec) !important; font-style: italic; font-weight: 500;">Your AI-Powered Wellness Companion</p>
</div>
""", unsafe_allow_html=True)

# Navigation
tabs = st.tabs(["Dashboard", "Log Cycle", "Track Symptoms", "History", "🌸 Wellness Tracker", "🌙 AI Wellness Assistant", "🔔 Notifications", "👤 Profile"])

with tabs[0]:
    st.subheader("Your Dashboard")
    
    latest_wellness = get_latest_wellness_log(user_id)
    latest_cycle = get_latest_cycle(user_id)
    
    if latest_cycle:
        last_date = latest_cycle['last_period_start']
        cycle_length = latest_cycle['cycle_length']
        period_duration = latest_cycle['period_duration']
        
        preds = calculate_predictions(last_date, cycle_length)
        days_until = (preds['next_period_date'] - date.today()).days
        phase_name, phase_desc = get_cycle_phase(last_date, cycle_length, period_duration)
        
        # 1. Next Period Reminder (KEEP from Phase 4)
        if days_until == 1:
            st.markdown('<div class="metric-card" style="background: linear-gradient(135deg, #FF7EB6, #E0609B); color: white; border-radius: 25px;">⚠️ <strong>URGENT:</strong> Your next period is expected tomorrow. Keep your essentials ready!</div>', unsafe_allow_html=True)
        elif 1 < days_until <= 3:
            st.markdown('<div class="metric-card" style="background: rgba(255, 126, 182, 0.1); border-left: 5px solid #FF7EB6; border-radius: 25px;">⏳ <strong>HEADS UP:</strong> Your next period is expected in just a few days.</div>', unsafe_allow_html=True)
        elif 3 < days_until <= 7:
            st.markdown('<div class="metric-card" style="background: rgba(200, 162, 255, 0.1); border-left: 5px solid #C4A7F4; border-radius: 25px;">🌸 <strong>REMINDER:</strong> Your next period is expected soon. Prepare essentials and prioritize self-care.</div>', unsafe_allow_html=True)
            
        st.markdown("### ✨ Wellness Snapshot")
        snap_cols = st.columns(5)
        
        mood_val = latest_wellness['mood'].split(" ")[1] if latest_wellness and " " in latest_wellness['mood'] else "N/A"
        energy_val = f"{latest_wellness['energy']}/10" if latest_wellness else "N/A"
        sleep_val = f"{latest_wellness['sleep']}h" if latest_wellness else "N/A"
        water_val = get_water_log(user_id, date.today())
        phase_str = phase_name.split(" ")[1] if " " in phase_name else phase_name
        
        with snap_cols[0]:
            metric_card("💖 Mood", mood_val)
        with snap_cols[1]:
            metric_card("🌙 Phase", phase_str)
        with snap_cols[2]:
            metric_card("💧 Water", f"{water_val}/8")
        with snap_cols[3]:
            metric_card("⚡ Energy", energy_val)
        with snap_cols[4]:
            metric_card("😴 Sleep", sleep_val)
            
        st.markdown("---")
        
        # Cycle Phase Insights and Tip (Phase 4 requirement)
        raw_mood = latest_wellness['mood'] if latest_wellness else None
        raw_energy = latest_wellness['energy'] if latest_wellness else None
        tip = generate_wellness_tip(phase_name, raw_mood, raw_energy)
        st.markdown("### 🌸 Daily Phase Insights")
        phase_col1, phase_col2 = st.columns([1, 2])
        with phase_col1:
            st.markdown(f"<div class='metric-card' style='text-align:center; display: flex; align-items: center; justify-content: center;'><h2 style='margin:0;'>{phase_name}</h2></div>", unsafe_allow_html=True)
        with phase_col2:
            st.markdown(f"<div class='metric-card'><strong>Description:</strong> {phase_desc}<br><br><strong>✨ Tip of the Day:</strong> {tip}</div>", unsafe_allow_html=True)
            
        st.markdown("---")
        
        # Water Reminder Tracker
        st.markdown("### 💧 Water Intake Tracker")
        water_col1, water_col2 = st.columns([1, 2])
        with water_col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            water_input = st.number_input("Glasses of water today", min_value=0, max_value=12, value=water_val)
            if st.button("Log Water"):
                save_water_log(user_id, date.today(), water_input)
                st.success("Water logged successfully!")
            st.markdown('</div>', unsafe_allow_html=True)
        with water_col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='color: var(--text); margin-top:0;'>Goal: 8 glasses/day</h4>", unsafe_allow_html=True)
            st.markdown(f"**Progress:** 💧 {water_input}/8")
            st.progress(min(water_input / 8.0, 1.0))
            if water_input < 8:
                st.markdown("<p style='color: var(--primary); font-style: italic; margin-bottom:0;'>Stay hydrated today 🌸</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color: var(--text); font-weight: bold; margin-bottom:0;'>Goal reached! Great job! 🎉</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
    else:
        st.markdown('<div class="metric-card" style="text-align: center; padding: 40px;">', unsafe_allow_html=True)
        st.markdown('<h2>🌙 Welcome to LunaFlow AI</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color: var(--text-sec); font-size: 1.1em;">Log your first cycle to unlock personalized phase insights, wellness tips, and smart reminders.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with tabs[1]:
    st.subheader("Log a New Cycle")
    
    with st.container():
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            last_period = st.date_input("Last Period Start Date", max_value=date.today())
        with col2:
            avg_length = st.number_input("Average Cycle Length (Days)", min_value=15, max_value=45, value=28)
            period_duration = st.number_input("Period Duration (Days)", min_value=1, max_value=10, value=5)
            
        if st.button("Save Cycle"):
            save_cycle(user_id, last_period, avg_length, period_duration)
            st.success("Cycle saved successfully! Go to the History tab to see your updates.")
        st.markdown('</div>', unsafe_allow_html=True)

with tabs[2]:
    st.subheader("Track Symptoms")
    
    symptom_date = st.date_input("Date", value=date.today(), max_value=date.today())
    
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("### How are you feeling today?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cramps = st.checkbox("😫 Cramps")
        acne = st.checkbox("🌋 Acne")
    with col2:
        mood_swings = st.checkbox("🎭 Mood Swings")
        fatigue = st.checkbox("😴 Fatigue")
    with col3:
        headache = st.checkbox("🤕 Headache")
        bloating = st.checkbox("🎈 Bloating")
        
    if st.button("Save Symptoms"):
        save_symptoms(user_id, symptom_date, cramps, mood_swings, headache, acne, fatigue, bloating)
        st.success("Symptoms saved successfully!")
    st.markdown('</div>', unsafe_allow_html=True)

with tabs[3]:
    st.subheader("Your History & Trends")
    
    theme_font_color = "#FFFFFF" if st.session_state.get('theme') == 'dark' else "#4A3B52"
    
    cycles_df = get_all_cycles(user_id)
    if len(cycles_df) >= 2:
        st.markdown("### Cycle Length History")
        cycles_df['date_str'] = pd.to_datetime(cycles_df['last_period_start']).apply(lambda x: f"{x.strftime('%b')} {x.day}")
        fig = px.line(
            cycles_df, 
            x='date_str', 
            y='cycle_length', 
            markers=True,
            title="Cycle Length Over Time"
        )
        fig.update_traces(line_color="#FF7EB6", marker_color="#E6D8FF", marker_size=10, marker_line_color="#4A3B52", marker_line_width=2)
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color=theme_font_color,
            xaxis_title="",
            yaxis_title="Cycle Length (Days)"
        )
        st.plotly_chart(fig, use_container_width=True)
    elif not cycles_df.empty:
        st.info("Log at least 2 cycles to see your cycle length trends.")
    else:
        st.info("No cycle history available yet.")
        
    symptoms_df = get_all_symptoms(user_id)
    if not symptoms_df.empty:
        st.markdown("### Symptom Trends")
        
        # Melt dataframe to plot counts of symptoms over time or overall frequencies
        symptom_cols = ['cramps', 'mood_swings', 'headache', 'acne', 'fatigue', 'bloating']
        # Calculate total occurrences of each symptom
        symptom_counts = symptoms_df[symptom_cols].sum().reset_index()
        symptom_counts.columns = ['Symptom', 'Count']
        
        fig2 = px.bar(
            symptom_counts,
            x='Symptom',
            y='Count',
            title="Most Frequent Symptoms",
            color='Symptom',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig2.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color=theme_font_color
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No symptom history available yet.")

with tabs[4]:
    st.subheader("🌸 Mood & Wellness Tracker")
    
    well_col1, well_col2 = st.columns([2, 1])
    
    with well_col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        w_date = st.date_input("Date", value=date.today(), max_value=date.today(), key="w_date")
        
        mood_options = ["😊 Happy", "😌 Calm", "🤩 Energetic", "😴 Tired", "😔 Sad", "😡 Irritated", "😣 Stressed", "😰 Anxious"]
        w_mood = st.selectbox("How are you feeling?", mood_options)
        
        st.markdown("---")
        w_energy = st.slider("Energy Level (1=Low, 10=High)", min_value=1, max_value=10, value=5)
        w_stress = st.slider("Stress Level (1=Relaxed, 10=Highly Stressed)", min_value=1, max_value=10, value=3)
        
        st.markdown("---")
        w_sleep = st.number_input("Hours Slept", min_value=0.0, max_value=24.0, value=7.5, step=0.5)
        w_water = st.number_input("Water Intake (Glasses)", min_value=0, max_value=20, value=4)
        
        st.markdown("---")
        w_notes = st.text_area("Daily Notes (Feelings, journal, etc.)")
        
        if st.button("Save Wellness Log"):
            save_wellness_log(user_id, w_date, w_mood, w_energy, w_stress, w_sleep, w_water, w_notes)
            st.success("Wellness log saved successfully! Scroll down to see your updated trends.")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with well_col2:
        # Score and Insights
        latest = get_latest_wellness_log(user_id)
        if latest:
            score = calculate_wellness_score(latest['sleep'], latest['water'], latest['mood'], latest['energy'])
            category = get_wellness_category(score)
            
            st.markdown(f"### Wellness Score: {score}/100")
            st.markdown(f"**Status:** {category}")
            st.progress(score / 100.0)
            
            st.markdown("---")
            st.markdown("### AI Insights")
            all_w_logs = get_all_wellness_logs(user_id)
            insights = generate_simple_insights(all_w_logs)
            for ins in insights:
                st.info(ins)
        else:
            st.info("Log your wellness to see your score and insights!")
            
    # Charts below
    st.markdown("---")
    st.subheader("Wellness Trends")
    all_logs = get_all_wellness_logs(user_id)
    
    if len(all_logs) < 5:
        st.markdown('<div class="metric-card" style="text-align: center; padding: 40px; margin-top: 20px;">', unsafe_allow_html=True)
        st.markdown('<h2>🌸 Keep Tracking Daily</h2>', unsafe_allow_html=True)
        st.markdown('<p style="color: #887B8F; font-size: 1.1em;">Track your mood, energy, sleep, and wellness for a few days to unlock personalized insights and beautiful trend analytics.</p>', unsafe_allow_html=True)
        st.markdown('<p style="color: #FF7EB6; font-weight: bold; font-size: 1.2em;">Minimum required records: 5</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        all_logs['date_str'] = pd.to_datetime(all_logs['date']).apply(lambda x: f"{x.strftime('%b')} {x.day}")
        
        c1, c2 = st.columns(2)
        with c1:
            fig_e = px.line(all_logs, x='date_str', y='energy', title="Energy Trend", markers=True)
            fig_e.update_traces(line_color="#FF7EB6")
            fig_e.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="#4A3B52", xaxis_title="")
            st.plotly_chart(fig_e, use_container_width=True)
            
            fig_w = px.bar(all_logs, x='date_str', y='water', title="Water Intake Trend")
            fig_w.update_traces(marker_color="#C4A7F4")
            fig_w.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="#4A3B52", xaxis_title="")
            st.plotly_chart(fig_w, use_container_width=True)
            
        with c2:
            fig_s = px.line(all_logs, x='date_str', y='stress', title="Stress Trend", markers=True)
            fig_s.update_traces(line_color="#E0609B")
            fig_s.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="#4A3B52", xaxis_title="")
            st.plotly_chart(fig_s, use_container_width=True)
            
            fig_sl = px.line(all_logs, x='date_str', y='sleep', title="Sleep Trend (Hours)", markers=True)
            fig_sl.update_traces(line_color="#887B8F")
            fig_sl.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="#4A3B52", xaxis_title="")
            st.plotly_chart(fig_sl, use_container_width=True)

with tabs[5]:
    st.subheader("🌙 AI Assistant Online")
    
    # Init chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = get_chat_history(user_id)
        
    if not st.session_state.messages:
        # Add initial greeting
        greeting = "Hello! I'm Luna 🌙\nAsk me anything about periods, cycles, symptoms, wellness, nutrition, and self-care."
        st.session_state.messages.append({"role": "assistant", "content": greeting})
        save_chat_message(user_id, "assistant", greeting)
        
    # CSS for soft glassmorphism for chat
    st.markdown("""
    <style>
        .stChatMessage {
            background: var(--cards) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.5) !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05) !important;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("Clear Chat", use_container_width=True):
            clear_chat_history(user_id)
            st.session_state.messages = []
            st.rerun()
            
    # Suggested Questions Section
    st.markdown("**Suggested Questions:**")
    questions = [
        "Why do I get cramps?",
        "What foods help during periods?",
        "How can I reduce bloating?",
        "What is ovulation?",
        "Why is my cycle late?"
    ]
    
    # Create columns for the buttons
    q_cols = st.columns(len(questions))
    for i, q in enumerate(questions):
        with q_cols[i]:
            if st.button(q, key=f"q_btn_{i}"):
                st.session_state.messages.append({"role": "user", "content": q})
                save_chat_message(user_id, "user", q)
                st.rerun()
                
    st.markdown("---")
                
    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    # Check if we need to fetch a response for the last user message
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Luna is typing..."):
                api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                response = get_sarvam_response(api_messages)
            st.write_stream(stream_data(response))
            
        st.session_state.messages.append({"role": "assistant", "content": response})
        save_chat_message(user_id, "assistant", response)
            
    # Input
    if prompt := st.chat_input("Ask Luna anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        save_chat_message(user_id, "user", prompt)
        st.rerun()

with tabs[6]:
    st.subheader("🔔 Notification Center")
    
    settings = get_notification_settings(user_id)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('### 🌙 Period Reminders')
        
        st.write("**Enable Reminders for:**")
        p_7 = st.checkbox("7 days before period", value='7' in settings['period_reminder_days'])
        p_3 = st.checkbox("3 days before period", value='3' in settings['period_reminder_days'])
        p_1 = st.checkbox("1 day before period", value='1' in settings['period_reminder_days'])
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('### 💧 Water Reminder')
        water_int = st.selectbox("Reminder Interval", ["Off", "Every 2 Hours", "Every 4 Hours", "Custom"], index=["Off", "Every 2 Hours", "Every 4 Hours", "Custom"].index(settings['water_reminder_interval']))
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('### ✨ Wellness Reminders')
        well_rem = st.checkbox("Daily Self-Care and Wellness Tips", value=settings['wellness_reminder'])
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('### 🌸 Ovulation Reminder')
        ovu_rem = st.checkbox("Notify me near my fertile window", value=settings.get('ovulation_reminder', True))
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('### 💊 Medicine Reminder')
        med_rem = st.text_input("Medicine to remind (e.g. Vitamins)", value=settings.get('medicine_reminder', ''), placeholder="Leave empty for none")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Save Preferences", use_container_width=True):
            active_p = []
            if p_7: active_p.append('7')
            if p_3: active_p.append('3')
            if p_1: active_p.append('1')
            save_notification_settings(user_id, active_p, water_int, well_rem, ovu_rem, med_rem)
            st.success("Notification preferences saved!")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('### Upcoming Reminders')
        
        latest = get_latest_cycle(user_id)
        has_reminders = False
        
        if latest:
            preds = calculate_predictions(latest['last_period_start'], latest['cycle_length'])
            days_until = (preds['next_period_date'] - date.today()).days
            
            if days_until > 0 and days_until <= 7 and '7' in settings['period_reminder_days']:
                st.info("🌙 Your cycle is expected in 7 days.")
                has_reminders = True
            elif days_until > 0 and days_until <= 3 and '3' in settings['period_reminder_days']:
                st.info("💖 Your period may start in 3 days. Prepare essentials.")
                has_reminders = True
            elif days_until == 1 and '1' in settings['period_reminder_days']:
                st.error("🌸 Your predicted period starts tomorrow.")
                has_reminders = True
                
        if settings['water_reminder_interval'] != "Off":
            st.info(f"💧 Water reminder active: {settings['water_reminder_interval']}")
            has_reminders = True
            
        if settings['wellness_reminder']:
            st.info("✨ Daily wellness tip scheduled for morning.")
            has_reminders = True
            
        if settings.get('ovulation_reminder', True) and latest:
            fertile_start = preds['fertile_window_start']
            days_to_fertile = (fertile_start - date.today()).days
            if 0 < days_to_fertile <= 5:
                st.info(f"🌸 Your fertile window begins in {days_to_fertile} days.")
                has_reminders = True
                
        if settings.get('medicine_reminder', ''):
            st.info(f"💊 Medicine Reminder: {settings['medicine_reminder']}")
            has_reminders = True
            
        if not has_reminders:
            st.write("You have no upcoming active reminders.")
            
        st.markdown('</div>', unsafe_allow_html=True)

with tabs[7]:
    st.subheader("👤 Your Profile & Insights")
    
    profile = get_user_profile(user_id)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('### Edit Profile')
        
        new_name = st.text_input("Name", value=profile['name'])
        new_age = st.number_input("Age", min_value=10, max_value=100, value=profile['age'])
        
        if st.button("Save Profile", use_container_width=True):
            update_user_profile(user_id, new_name, new_age)
            st.session_state.user_name = new_name
            st.success("Profile updated!")
            st.rerun()
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('### Device Setup (Firebase)')
        fcm = st.text_input("FCM Device Token", value=profile['fcm_token'], type="password")
        if st.button("Link Device", use_container_width=True):
            save_fcm_token(user_id, fcm)
            st.success("Push Notifications Enabled!")
            
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.markdown('### ✨ AI Health Insights')
        
        all_cycles = pd.DataFrame(get_all_cycles(user_id))
        if not all_cycles.empty:
            avg_cycle = int(all_cycles['cycle_length'].mean())
            st.write(f"🌸 **Your average cycle length is {avg_cycle} days.**")
            
            latest = get_latest_cycle(user_id)
            if latest:
                preds = calculate_predictions(latest['last_period_start'], latest['cycle_length'])
                days_until = (preds['next_period_date'] - date.today()).days
                
                if 0 < days_until <= 5:
                    st.write("📉 **Insight:** Energy levels tend to drop before your period. Prioritize rest this week.")
                elif days_until > 15:
                    st.write("🔥 **Insight:** You are approaching your ovulation phase. Expect higher energy and mood!")
                else:
                    st.write("🌿 **Insight:** Keep tracking daily to build better personalized predictions.")
        else:
            st.write("Log more cycles to generate insights.")
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('### 📥 Data Export')
        st.write("Download your secure health data.")
        
        if not all_cycles.empty:
            csv_cycles = all_cycles.to_csv(index=False)
            st.download_button(
                label="Download Cycle History (CSV)",
                data=csv_cycles,
                file_name='lunaflow_cycles.csv',
                mime='text/csv',
                use_container_width=True
            )
        else:
            st.button("Download Cycle History (CSV)", disabled=True, help="No data to export", use_container_width=True)
        
        all_symp = pd.DataFrame(get_all_symptoms(user_id))
        if not all_symp.empty:
            csv_symp = all_symp.to_csv(index=False)
            st.download_button(
                label="Download Symptom History (CSV)",
                data=csv_symp,
                file_name='lunaflow_symptoms.csv',
                mime='text/csv',
                use_container_width=True
            )
        else:
            st.button("Download Symptom History (CSV)", disabled=True, help="No data to export", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
