import streamlit as st
from database.users_db import verify_user

def render_login():
    st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <div style="font-size: 3.5rem; margin-bottom: 10px; text-shadow: 0 4px 15px rgba(255, 126, 182, 0.4);">🌙</div>
            <h1 style="color: var(--primary) !important; font-size: 2.5rem; margin-bottom: 5px;">Welcome Back</h1>
            <p style="color: var(--text-sec); font-size: 1.1rem;">Log in to continue your wellness journey.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("<h3 style='text-align: center; color: var(--primary); margin-bottom: 20px;'>Sign In</h3>", unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Log In", use_container_width=True, key="login_submit_btn"):
                if not email or not password:
                    st.error("Please enter both email and password.")
                else:
                    user = verify_user(email, password)
                    if user:
                        st.session_state.user_id = user['id']
                        st.session_state.user_name = user['name']
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")
            
        st.markdown('<div style="text-align: center; margin-top: 15px;"><p style="color: var(--text-sec);">Don\'t have an account? <b>Click Sign Up</b> above.</p></div>', unsafe_allow_html=True)
