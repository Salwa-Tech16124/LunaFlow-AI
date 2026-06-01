with open('s:/LunaFlow AI/app.py', 'a', encoding='utf-8') as f:
    f.write('''
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
        
        st.markdown('<br>### 💧 Water Reminder', unsafe_allow_html=True)
        water_int = st.selectbox("Reminder Interval", ["Off", "Every 2 Hours", "Every 4 Hours", "Custom"], index=["Off", "Every 2 Hours", "Every 4 Hours", "Custom"].index(settings['water_reminder_interval']))
        
        st.markdown('<br>### ✨ Wellness Reminders', unsafe_allow_html=True)
        well_rem = st.checkbox("Daily Self-Care and Wellness Tips", value=settings['wellness_reminder'])
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Save Preferences", use_container_width=True):
            active_p = []
            if p_7: active_p.append('7')
            if p_3: active_p.append('3')
            if p_1: active_p.append('1')
            save_notification_settings(user_id, active_p, water_int, well_rem)
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
            
        if not has_reminders:
            st.write("You have no upcoming active reminders.")
            
        st.markdown('</div>', unsafe_allow_html=True)
''')
