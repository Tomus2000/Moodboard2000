"""Journal page for viewing and searching entries."""
import streamlit as st
from datetime import datetime, timedelta
from core.db import init_db, get_or_create_user, get_entries, search_entries, get_all_tags
from core.config import MOOD_EMOJI, MOOD_COLORS
from core.auth import check_auth
from core.styles import apply_beach_theme
import json

# Check authentication
if not check_auth():
    st.stop()

# Apply beach theme
apply_beach_theme()

# Initialize database
init_db()

# Get or create user
user = get_or_create_user(username="default", role="student")

# Title
st.title("📔 Your Journal")
st.markdown("View and search your mood entries.")

# Filters
col1, col2, col3 = st.columns(3)

with col1:
    date_range = st.date_input(
        "Date Range",
        value=(datetime.now().date() - timedelta(days=30), datetime.now().date()),
        help="Select date range for entries",
    )

with col2:
    all_tags = get_all_tags(user.id)
    selected_tags = st.multiselect(
        "Filter by Tags",
        options=all_tags,
        help="Select tags to filter entries",
    )

with col3:
    search_query = st.text_input(
        "Search",
        placeholder="Search in entries...",
        help="Search for text in entries",
    )

# Sentiment filter
sentiment_filter = st.selectbox(
    "Filter by Sentiment",
    options=["All", "Positive (0.0 to 1.0)", "Neutral (-0.3 to 0.3)", "Negative (-1.0 to -0.3)"],
    index=0,
)

# Get entries
if search_query:
    entries = search_entries(user.id, search_query)
else:
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date = date_range[0]
        end_date = date_range[1]
    elif isinstance(date_range, tuple) and len(date_range) == 1:
        start_date = date_range[0] - timedelta(days=30)
        end_date = date_range[0]
    else:
        start_date = date_range - timedelta(days=30)
        end_date = date_range
    
    entries = get_entries(
        user_id=user.id,
        start_date=datetime.combine(start_date, datetime.min.time()),
        end_date=datetime.combine(end_date, datetime.max.time()),
        tags=selected_tags if selected_tags else None,
    )

# Apply sentiment filter
if sentiment_filter != "All":
    if sentiment_filter == "Positive (0.0 to 1.0)":
        entries = [e for e in entries if 0.0 <= e.sentiment <= 1.0]
    elif sentiment_filter == "Neutral (-0.3 to 0.3)":
        entries = [e for e in entries if -0.3 <= e.sentiment <= 0.3]
    elif sentiment_filter == "Negative (-1.0 to -0.3)":
        entries = [e for e in entries if -1.0 <= e.sentiment <= -0.3]

# Display entries
st.divider()
st.subheader(f"Found {len(entries)} entries")

if entries:
    # Sort by date (newest first)
    entries = sorted(entries, key=lambda x: x.created_at, reverse=True)
    
    for entry in entries:
        date = datetime.fromtimestamp(entry.created_at).strftime("%Y-%m-%d %H:%M")
        mood_score = entry.mood_score
        
        # Determine emoji and color
        if mood_score < 40:
            emoji = MOOD_EMOJI["low"]
            color = MOOD_COLORS["low"]
        elif mood_score < 60:
            emoji = MOOD_EMOJI["medium_low"]
            color = MOOD_COLORS["medium_low"]
        elif mood_score < 80:
            emoji = MOOD_EMOJI["medium_high"]
            color = MOOD_COLORS["medium_high"]
        else:
            emoji = MOOD_EMOJI["high"]
            color = MOOD_COLORS["high"]
        
        # Parse emotions
        try:
            emotions = json.loads(entry.emotions_json)
        except Exception:
            emotions = {}
        
        # Parse tags
        tags = entry.tags.split(",") if entry.tags else []
        
        # Display entry card
        with st.expander(f"{emoji} {date} - Mood: {mood_score}/100"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Text:**\n{entry.text}")
                if entry.summary:
                    st.markdown(f"**Summary:**\n{entry.summary}")
            
            with col2:
                st.metric("Sentiment", f"{entry.sentiment:.2f}")
                st.metric("Mood Score", f"{mood_score}/100")
                
                if tags:
                    st.markdown("**Tags:**")
                    tag_str = " ".join([f"`{tag.strip()}`" for tag in tags])
                    st.markdown(tag_str)
                
                if emotions:
                    st.markdown("**Emotions:**")
                    for emotion, value in emotions.items():
                        st.progress(value, text=f"{emotion}: {value:.1%}")
            
            # Display suggestions if available
            if hasattr(entry, 'suggestions') and entry.suggestions:
                st.markdown("**Suggestions:**")
                for suggestion in entry.suggestions:
                    st.write(f"💡 {suggestion}")
else:
    st.info("No entries found. Try adjusting your filters or check in to create your first entry! 🌊")

