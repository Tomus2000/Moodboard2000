"""Simple authentication using PIN or username/password."""
import streamlit as st
from core.config import APP_AUTH_PIN
from core.styles import apply_beach_theme
import os


def check_auth() -> bool:
    """Check if user is authenticated."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    return st.session_state.authenticated


def login_page():
    """Show login page and handle authentication."""
    st.title("🌊 Student Moodmeter")
    st.markdown("### Welcome! Please log in to continue.")
    
    # PIN-based authentication (simpler)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        pin = st.text_input("Enter PIN", type="password", placeholder="0000", key="pin_input")
        
        if st.button("Login", type="primary", use_container_width=True):
            if pin == APP_AUTH_PIN:
                st.session_state.authenticated = True
                st.success("Login successful! 🌊")
                st.rerun()
            else:
                st.error("Incorrect PIN. Please try again.")
    
    # Alternative: Username/password (if configured)
    username_auth = os.getenv("APP_USERNAME", "")
    password_auth = os.getenv("APP_PASSWORD", "")
    
    if username_auth and password_auth:
        st.divider()
        st.markdown("### Or login with username/password")
        with col2:
            username = st.text_input("Username", key="username_input")
            password = st.text_input("Password", type="password", key="password_input")
            
            if st.button("Login with Username", use_container_width=True):
                if username == username_auth and password == password_auth:
                    st.session_state.authenticated = True
                    st.success("Login successful! 🌊")
                    st.rerun()
                else:
                    st.error("Incorrect credentials. Please try again.")


def logout():
    """Logout user."""
    st.session_state.authenticated = False
    st.rerun()


def require_auth(func):
    """Decorator to require authentication for a page."""
    def wrapper(*args, **kwargs):
        if not check_auth():
            login_page()
            return
        return func(*args, **kwargs)
    return wrapper

