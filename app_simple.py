"""Main Streamlit app for Student Moodmeter - Simplified version."""
import streamlit as st

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Student Moodmeter 🌊",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import after page config
from core.styles import apply_beach_theme
from core.db import init_db
from core.auth import check_auth, login_page

# Apply theme
apply_beach_theme()

# Initialize database
try:
    init_db()
except Exception as e:
    st.error(f"Database error: {str(e)}")
    st.stop()

# Handle authentication
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Show login if not authenticated
if not st.session_state.authenticated:
    login_page()
else:
    # Main app content
    st.title("🌊 Student Moodmeter")
    st.markdown("### A calm, beach-themed space to check in with your mood")
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### Navigation")
        st.page_link("pages/1_Check_in.py", label="🌊 Check-in", icon="🌊")
        st.page_link("pages/2_Journal.py", label="📔 Journal", icon="📔")
        st.page_link("pages/3_Analytics.py", label="📊 Analytics", icon="📊")
        st.page_link("pages/4_Cohort_Compare.py", label="👥 Cohort Compare", icon="👥")
        st.page_link("pages/5_Settings.py", label="⚙️ Settings", icon="⚙️")
        
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
                st.info("No entries yet. Check in to get started! 🌊")
        except Exception as e:
            st.warning(f"Stats unavailable: {str(e)}")
    
    # Welcome message
    st.markdown("""
    ### Welcome to Student Moodmeter! 🌊
    
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


