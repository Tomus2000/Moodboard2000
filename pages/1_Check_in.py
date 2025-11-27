"""Check-in page for mood entry."""
import streamlit as st
from datetime import datetime
from core.db import init_db, get_or_create_user, add_entry, get_streak, get_entries
from core.ai import analyze_text
from core.config import MOOD_EMOJI, MOOD_COLORS
from core.auth import check_auth
from core.nlp_utils import scrub_pii
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
st.title("🌊 How's the tide today?")
st.markdown("Share your thoughts and feelings. We'll help you understand your mood.")

# Check for PII scrubbing setting
scrub_pii_enabled = st.session_state.get("scrub_pii", False)

# Streak banner
streak = get_streak(user.id)
if streak > 0:
    shells = "🐚" * min(streak, 10)
    st.success(f"**You've checked in {streak} day{'s' if streak != 1 else ''} in a row!** {shells}")

# Text input
st.subheader("What's on your mind?")
text = st.text_area(
    "Share your thoughts",
    height=150,
    placeholder="Today's class stressed me out, but I'm looking forward to the weekend...",
    help="Write about your day, how you're feeling, or what's on your mind.",
    key="checkin_text",
)

# Character counter
char_count = len(text)
st.caption(f"{char_count} characters")

# Tags input
st.subheader("Tags (optional)")
tags_input = st.text_input(
    "Add tags (comma-separated)",
    placeholder="exams, stress, friends, classes",
    help="Add tags to categorize your entry (e.g., exams, stress, friends).",
)

# Parse tags
tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()] if tags_input else []

# Analyze button
if st.button("🌊 Check in", type="primary", use_container_width=True):
    if not text.strip():
        st.warning("Please enter some text before checking in.")
    else:
        with st.spinner("Analyzing your mood..."):
            # Scrub PII if enabled
            text_to_analyze = scrub_pii(text) if scrub_pii_enabled else text
            
            # Analyze text
            result = analyze_text(text_to_analyze, tags)
            
            # Save entry
            entry = add_entry(
                user_id=user.id,
                text=text_to_analyze,
                summary=result["summary"],
                sentiment=result["sentiment"],
                mood_score=result["mood_score"],
                emotions=result["emotions"],
                tags=",".join(tags) if tags else "",
                source="manual",
                model_used=result["model_used"],
                tokens=result["tokens"],
            )
            
            # Show success message
            st.success("Saved 🌊")
            st.balloons()
            
            # Display results
            st.divider()
            st.subheader("Your Mood Analysis")
            
            # Mood score badge
            mood_score = result["mood_score"]
            if mood_score < 40:
                mood_emoji = MOOD_EMOJI["low"]
                mood_color = MOOD_COLORS["low"]
                mood_label = "Low"
            elif mood_score < 60:
                mood_emoji = MOOD_EMOJI["medium_low"]
                mood_color = MOOD_COLORS["medium_low"]
                mood_label = "Medium-Low"
            elif mood_score < 80:
                mood_emoji = MOOD_EMOJI["medium_high"]
                mood_color = MOOD_COLORS["medium_high"]
                mood_label = "Medium-High"
            else:
                mood_emoji = MOOD_EMOJI["high"]
                mood_color = MOOD_COLORS["high"]
                mood_label = "High"
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Mood Score", f"{mood_score}/100", delta=f"{mood_emoji} {mood_label}")
            with col2:
                st.metric("Sentiment", f"{result['sentiment']:.2f}", delta="(-1 to +1)")
            with col3:
                st.metric("Model", result["model_used"], delta=f"{result['tokens']} tokens")
            
            # Summary
            st.markdown("### Summary")
            st.info(result["summary"])
            
            # Emotions
            st.markdown("### Emotions")
            emotions = result["emotions"]
            emotion_cols = st.columns(4)
            for i, (emotion, value) in enumerate(emotions.items()):
                with emotion_cols[i % 4]:
                    st.progress(value, text=f"{emotion}: {value:.1%}")
            
            # Suggestions
            st.markdown("### Gentle Suggestions")
            suggestions = result["suggestions"]
            for i, suggestion in enumerate(suggestions, 1):
                st.checkbox(f"💡 {suggestion}", key=f"suggestion_{i}")
            
            # Use form to clear text after submission - don't modify session state directly
            # The text will persist until next interaction which is fine for UX

# Display recent entries
st.divider()
st.subheader("Recent Entries")
recent_entries = get_entries(user_id=user.id, limit=5)

if recent_entries:
    for entry in recent_entries[:3]:
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
        
        with st.container():
            st.markdown(
                f"""
                <div style="background: rgba(255,255,255,0.72); border-radius: 12px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid {color};">
                    <strong>{emoji} {date}</strong><br>
                    <small>Mood: {mood_score}/100 | Sentiment: {entry.sentiment:.2f}</small><br>
                    <p style="margin-top: 0.5rem;">{entry.text[:100]}{"..." if len(entry.text) > 100 else ""}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
else:
    st.info("No entries yet. Check in to get started! 🌊")

