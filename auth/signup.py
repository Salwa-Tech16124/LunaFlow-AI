import streamlit as st
import re
from database.users_db import create_user

def check_password_strength(password):
    if len(password) < 8:
        return False
    if not re.search("[a-z]", password):
        return False
    if not re.search("[A-Z]", password):
        return False
    if not re.search("[0-9]", password):
        return False
    return True

def render_signup():
    st.markdown("""
        <div style="text-align: center; margin-bottom: 30px;">
            <div style="font-size: 3.5rem; margin-bottom: 10px; text-shadow: 0 4px 15px rgba(255, 126, 182, 0.4);">✨</div>
            <h1 style="color: var(--primary) !important; font-size: 2.5rem; margin-bottom: 5px;">Join LunaFlow AI</h1>
            <p style="color: var(--text-sec); font-size: 1.1rem;">Create your personalized wellness account.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name = st.text_input("Full Name", placeholder="Jane Doe")
        email = st.text_input("Email", placeholder="you@example.com")
        password = st.text_input("Password", type="password", placeholder="8+ chars, uppercase, number")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign Up", use_container_width=True, key="signup_submit_btn"):
            if not name or not email or not password or not confirm_password:
                st.error("Please fill in all fields.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            elif not check_password_strength(password):
                st.error("Password must be at least 8 characters long and include an uppercase letter, lowercase letter, and number.")
            else:
                success = create_user(name, email, password)
                if success:
                    st.success("Account created successfully! Please Log In.")
                else:
                    st.error("An account with this email already exists.")
