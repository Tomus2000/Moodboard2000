"""Main Streamlit app for Student Moodmeter."""
import sys
import os
from pathlib import Path

# Add the project root to Python path (for Streamlit Cloud)
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Student Moodmeter",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import modules after page config
try:
    from core.styles import apply_beach_theme
    from core.db import init_db
    from core.auth import check_auth, login_page
    from core.config import APP_AUTH_PIN
except ImportError as e:
    st.error(f"Import error: {e}")
    st.error(f"Python path: {sys.path}")
    st.error(f"Current directory: {os.getcwd()}")
    st.error(f"Project root: {project_root}")
    st.stop()

# Apply theme
try:
    apply_beach_theme()
except Exception as e:
    st.warning(f"Theme error: {e}")

# Initialize database
try:
    init_db()
except Exception as e:
    st.error(f"Database error: {e}")
    st.stop()

# Initialize authentication state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Handle authentication
if not st.session_state.authenticated:
    # Show login page
    st.title("Student Moodmeter")
    st.markdown("### Welcome! Please log in to continue.")
    
    pin = st.text_input("Enter PIN", type="password", placeholder="0000", key="pin_input")
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Login", type="primary", use_container_width=True):
            if pin == APP_AUTH_PIN:
                st.session_state.authenticated = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Incorrect PIN. Please try again.")
else:
    # Main app content (authenticated)
    st.title("Student Moodmeter")
    st.markdown("### A calm, beach-themed space to check in with your mood")
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### Navigation")
        try:
            st.page_link("pages/1_Check_in.py", label="Check-in", icon="🌊")
            st.page_link("pages/2_Journal.py", label="Journal", icon="📔")
            st.page_link("pages/3_Analytics.py", label="Analytics", icon="📊")
            st.page_link("pages/4_Cohort_Compare.py", label="Cohort Compare", icon="👥")
            st.page_link("pages/5_Settings.py", label="Settings", icon="⚙️")
        except Exception as e:
            st.warning(f"Navigation error: {e}")
        
        st.divider()
        st.markdown("### Quick Stats")
        try:
            from core.db import get_or_create_user, get_entries, get_streak
            user = get_or_create_user(username="default", role="student")
            entries = get_entries(user_id=user.id, limit=100)
            streak = get_streak(user.id)
            
            if entries:
                avg_mood = sum(e.mood_score for e in entries) / len(entries)
                st.metric("Average Mood", f"{avg_mood:.1f}/100")
                st.metric("Total Entries", len(entries))
                st.metric("Current Streak", f"{streak} days")
            else:
                st.info("No entries yet. Check in to get started!")
        except Exception as e:
            st.info("Stats will appear after your first check-in.")
    
    # Welcome message
    st.markdown("""
    ### Welcome to Student Moodmeter!
    
    This is a safe space to:
    - **Check in** with your mood and get AI-powered insights
    - **Journal** your thoughts and feelings
    - **Analyze** your mood patterns over time
    - **Track** your emotional well-being
    
    Get started by checking in with your mood today!
    """)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666;">
        <p>Built with ❤️ using Streamlit</p>
        <p>Student Moodmeter v1.0.0</p>
    </div>
    """, unsafe_allow_html=True)
