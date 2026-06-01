import re

with open("s:/LunaFlow AI/app.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add imports
content = content.replace("from database.wellness_db", "from database.users_db import init_users_db\nfrom auth.login import render_login\nfrom auth.signup import render_signup\nfrom database.wellness_db")

# Add init_users_db()
content = content.replace("init_db()", "init_users_db()\ninit_db()")

# Add Auth block after Apply Theme
auth_block = """# Apply Theme
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
"""

content = content.replace("# Apply Theme\napply_theme(is_dark=(st.session_state.theme == 'dark'))", auth_block)

# Replace all DB calls
db_calls = [
    "get_latest_wellness_log(",
    "get_latest_cycle(",
    "get_water_log(",
    "save_water_log(",
    "save_cycle(",
    "get_all_cycles(",
    "save_symptoms(",
    "get_all_symptoms(",
    "save_wellness_log(",
    "get_all_wellness_logs(",
    "get_chat_history(",
    "save_chat_message(",
    "clear_chat_history("
]

for call in db_calls:
    content = content.replace(call, call + "user_id, ")
    
content = content.replace("(user_id, )", "(user_id)")

with open("s:/LunaFlow AI/app.py", "w", encoding="utf-8") as f:
    f.write(content)
