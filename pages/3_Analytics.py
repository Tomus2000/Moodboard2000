"""Analytics page with comprehensive mood insights."""
import streamlit as st
from datetime import datetime, timedelta
from core.db import init_db, get_or_create_user, get_entries, get_all_tags
from core.charts import (
    mood_time_series,
    emotion_radar,
    tag_frequency,
    hour_of_day_heatmap,
    calendar_heatmap,
    sentiment_distribution,
)
from core.nlp_utils import get_top_ngrams, get_wordcloud, get_positive_negative_words
from core.config import MOOD_EMOJI, MOOD_COLORS
from core.auth import check_auth
from core.styles import apply_beach_theme
import pandas as pd
import json
from PIL import Image
import io

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
st.title("📊 Analytics Dashboard")
st.markdown("Explore your mood patterns and insights.")

# Date range selector
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input(
        "Start Date",
        value=datetime.now().date() - timedelta(days=30),
        help="Select start date for analytics",
    )
with col2:
    end_date = st.date_input(
        "End Date",
        value=datetime.now().date(),
        help="Select end date for analytics",
    )

# Get entries
entries = get_entries(
    user_id=user.id,
    start_date=datetime.combine(start_date, datetime.min.time()),
    end_date=datetime.combine(end_date, datetime.max.time()),
)

if not entries:
    st.info("No entries found for this date range. Check in to create your first entry! 🌊")
    st.stop()

# Summary metrics
st.divider()
st.subheader("Summary Metrics")

col1, col2, col3, col4 = st.columns(4)

avg_mood = sum(e.mood_score for e in entries) / len(entries)
avg_sentiment = sum(e.sentiment for e in entries) / len(entries)
total_entries = len(entries)
days_with_entries = len(set(datetime.fromtimestamp(e.created_at).date() for e in entries))

with col1:
    st.metric("Average Mood", f"{avg_mood:.1f}/100")
with col2:
    st.metric("Average Sentiment", f"{avg_sentiment:.2f}")
with col3:
    st.metric("Total Entries", total_entries)
with col4:
    st.metric("Days with Entries", days_with_entries)

# Insights
st.divider()
st.subheader("Insights")

insights_col1, insights_col2 = st.columns(2)

with insights_col1:
    # Most positive day
    mood_by_date = {}
    for entry in entries:
        date = datetime.fromtimestamp(entry.created_at).date()
        if date not in mood_by_date:
            mood_by_date[date] = []
        mood_by_date[date].append(entry.mood_score)
    
    avg_mood_by_date = {date: sum(scores) / len(scores) for date, scores in mood_by_date.items()}
    if avg_mood_by_date:
        best_date = max(avg_mood_by_date.items(), key=lambda x: x[1])
        worst_date = min(avg_mood_by_date.items(), key=lambda x: x[1])
        
        st.info(f"**Most Positive Day:** {best_date[0]} (Mood: {best_date[1]:.1f}/100)")
        st.warning(f"**Least Positive Day:** {worst_date[0]} (Mood: {worst_date[1]:.1f}/100)")

with insights_col2:
    # Top tags
    all_tags = get_all_tags(user.id)
    if all_tags:
        tag_counts = {}
        for entry in entries:
            if entry.tags:
                for tag in entry.tags.split(","):
                    tag = tag.strip()
                    if tag:
                        tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        if tag_counts:
            top_tag = max(tag_counts.items(), key=lambda x: x[1])
            st.info(f"**Top Tag:** {top_tag[0]} ({top_tag[1]} entries)")

# Time series chart
st.divider()
st.subheader("Mood Over Time")
fig_time = mood_time_series(entries, days=30)
st.plotly_chart(fig_time, use_container_width=True)

# Emotion radar
st.divider()
st.subheader("Emotion Distribution")
col1, col2 = st.columns([2, 1])

with col1:
    fig_radar = emotion_radar(entries)
    st.plotly_chart(fig_radar, use_container_width=True)

with col2:
    # Average emotions
    emotion_sums = {}
    for entry in entries:
        try:
            emotions = json.loads(entry.emotions_json)
            for emotion, value in emotions.items():
                emotion_sums[emotion] = emotion_sums.get(emotion, 0.0) + value
        except Exception:
            continue
    
    if emotion_sums:
        count = len(entries)
        avg_emotions = {emotion: emotion_sums.get(emotion, 0.0) / count for emotion in emotion_sums.keys()}
        sorted_emotions = sorted(avg_emotions.items(), key=lambda x: x[1], reverse=True)
        
        st.markdown("**Top Emotions:**")
        for emotion, value in sorted_emotions[:5]:
            st.progress(value, text=f"{emotion}: {value:.1%}")

# Tag frequency
st.divider()
st.subheader("Tag Frequency")
fig_tags = tag_frequency(entries, top_n=10)
st.plotly_chart(fig_tags, use_container_width=True)

# Hour of day heatmap
st.divider()
st.subheader("Mood by Hour and Day")
fig_heatmap = hour_of_day_heatmap(entries)
st.plotly_chart(fig_heatmap, use_container_width=True)

# Calendar heatmap
st.divider()
st.subheader("Calendar Heatmap")
year = st.selectbox("Select Year", options=[datetime.now().year, datetime.now().year - 1])
fig_calendar = calendar_heatmap(entries, year=year)
st.plotly_chart(fig_calendar, use_container_width=True)

# Sentiment distribution
st.divider()
st.subheader("Sentiment Distribution")
fig_sentiment = sentiment_distribution(entries)
st.plotly_chart(fig_sentiment, use_container_width=True)

# Word cloud
st.divider()
st.subheader("Word Cloud")
all_text = " ".join([e.text for e in entries])
if all_text:
    try:
        wordcloud_img = get_wordcloud(all_text, width=800, height=400)
        if wordcloud_img:
            img = Image.open(wordcloud_img)
            st.image(img, use_container_width=True)
        else:
            st.info("Word cloud generation unavailable.")
    except Exception as e:
        st.info(f"Word cloud generation unavailable: {str(e)}")

# Triggers (n-grams)
st.divider()
st.subheader("Common Phrases")
if all_text:
    try:
        bigrams = get_top_ngrams([e.text for e in entries], n=2, top_k=10)
        trigrams = get_top_ngrams([e.text for e in entries], n=3, top_k=10)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Top Bigrams:**")
            for phrase, count in bigrams:
                st.write(f"- {phrase} ({count})")
        
        with col2:
            st.markdown("**Top Trigrams:**")
            for phrase, count in trigrams:
                st.write(f"- {phrase} ({count})")
    except Exception:
        st.info("Phrase analysis unavailable.")

# Positive/negative words
st.divider()
st.subheader("Positive and Negative Words")
if all_text:
    try:
        positive, negative = get_positive_negative_words([e.text for e in entries], top_k=10)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Positive Words:**")
            for word in positive:
                st.write(f"- {word}")
        
        with col2:
            st.markdown("**Negative Words:**")
            for word in negative:
                st.write(f"- {word}")
    except Exception:
        st.info("Word analysis unavailable.")

