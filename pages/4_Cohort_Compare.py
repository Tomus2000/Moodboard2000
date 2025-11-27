"""Cohort comparison page for teacher mode."""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from core.db import init_db, get_or_create_user, get_cohort_entries, Cohort, CohortMember
from core.charts import mood_time_series, emotion_radar, tag_frequency
from core.config import MOOD_COLORS
from core.auth import check_auth
from core.styles import apply_beach_theme
from sqlmodel import Session, select, create_engine
from core.config import DB_URL
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

# Check if user is a teacher
if user.role != "teacher":
    st.warning("Cohort comparison is only available for teachers. Please contact an administrator to enable teacher mode.")
    st.stop()

# Title
st.title("👥 Cohort Comparison")
st.markdown("Compare anonymized mood data across class sections.")

# Privacy notice
st.info("⚠️ **Privacy Notice:** This view only shows aggregated data. No individual entries or raw text are displayed.")

# Get cohorts
engine = create_engine(DB_URL)
with Session(engine) as session:
    cohorts = session.exec(select(Cohort)).all()

if not cohorts:
    st.info("No cohorts available. Please create cohorts in Settings.")
    st.stop()

# Select cohorts to compare
st.subheader("Select Cohorts to Compare")
selected_cohorts = st.multiselect(
    "Cohorts",
    options=[c.name for c in cohorts],
    default=[c.name for c in cohorts[:2]] if len(cohorts) >= 2 else [c.name for c in cohorts],
    help="Select cohorts to compare",
)

if not selected_cohorts:
    st.info("Please select at least one cohort to compare.")
    st.stop()

# Date range
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input(
        "Start Date",
        value=datetime.now().date() - timedelta(days=30),
        help="Select start date for comparison",
    )
with col2:
    end_date = st.date_input(
        "End Date",
        value=datetime.now().date(),
        help="Select end date for comparison",
    )

# Get entries for each cohort
cohort_data = {}
with Session(engine) as session:
    for cohort_name in selected_cohorts:
        cohort = session.exec(select(Cohort).where(Cohort.name == cohort_name)).first()
        if cohort:
            entries = get_cohort_entries(cohort.id)
            # Filter by date range
            start_ts = int(datetime.combine(start_date, datetime.min.time()).timestamp())
            end_ts = int(datetime.combine(end_date, datetime.max.time()).timestamp())
            entries = [e for e in entries if start_ts <= e.created_at <= end_ts]
            cohort_data[cohort_name] = entries

# Summary metrics
st.divider()
st.subheader("Summary Metrics")

summary_data = []
for cohort_name, entries in cohort_data.items():
    if entries:
        avg_mood = sum(e.mood_score for e in entries) / len(entries)
        avg_sentiment = sum(e.sentiment for e in entries) / len(entries)
        total_entries = len(entries)
        unique_users = len(set(e.user_id for e in entries))
        
        summary_data.append({
            "Cohort": cohort_name,
            "Average Mood": f"{avg_mood:.1f}",
            "Average Sentiment": f"{avg_sentiment:.2f}",
            "Total Entries": total_entries,
            "Unique Users": unique_users,
        })

if summary_data:
    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary, use_container_width=True)

# Comparison charts
st.divider()
st.subheader("Mood Over Time Comparison")

for cohort_name, entries in cohort_data.items():
    if entries:
        st.markdown(f"### {cohort_name}")
        fig = mood_time_series(entries, days=30)
        st.plotly_chart(fig, use_container_width=True)

# Emotion comparison
st.divider()
st.subheader("Emotion Distribution Comparison")

for cohort_name, entries in cohort_data.items():
    if entries:
        st.markdown(f"### {cohort_name}")
        fig = emotion_radar(entries)
        st.plotly_chart(fig, use_container_width=True)

# Tag comparison
st.divider()
st.subheader("Tag Frequency Comparison")

for cohort_name, entries in cohort_data.items():
    if entries:
        st.markdown(f"### {cohort_name}")
        fig = tag_frequency(entries, top_n=10)
        st.plotly_chart(fig, use_container_width=True)

# Notes
st.divider()
st.info("**Note:** All data is anonymized. Individual entries and raw text are not displayed to protect student privacy.")

