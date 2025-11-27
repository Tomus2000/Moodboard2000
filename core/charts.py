"""Chart utilities using Plotly and Altair."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json
from core.db import Entry
from core.config import MOOD_COLORS, EMOTIONS


def mood_time_series(entries: List[Entry], days: int = 30) -> go.Figure:
    """Create time series chart of mood scores."""
    if not entries:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
        )
        return fig
    
    df = pd.DataFrame([
        {
            "date": datetime.fromtimestamp(e.created_at).date(),
            "mood_score": e.mood_score,
            "sentiment": e.sentiment,
        }
        for e in entries
    ])
    
    # Group by date and calculate average
    df_grouped = df.groupby("date")["mood_score"].mean().reset_index()
    df_grouped["date"] = pd.to_datetime(df_grouped["date"])
    
    # Color based on mood score
    df_grouped["color"] = df_grouped["mood_score"].apply(
        lambda x: (
            MOOD_COLORS["low"] if x < 40
            else MOOD_COLORS["medium_low"] if x < 60
            else MOOD_COLORS["medium_high"] if x < 80
            else MOOD_COLORS["high"]
        )
    )
    
    fig = px.line(
        df_grouped,
        x="date",
        y="mood_score",
        title="Mood Score Over Time",
        labels={"mood_score": "Mood Score", "date": "Date"},
        color_discrete_sequence=[MOOD_COLORS["medium_high"]],
    )
    
    # Add scatter points with colors
    fig.add_trace(
        go.Scatter(
            x=df_grouped["date"],
            y=df_grouped["mood_score"],
            mode="markers",
            marker=dict(size=10, color=df_grouped["color"]),
            showlegend=False,
        )
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Mood Score (0-100)",
        yaxis_range=[0, 100],
        hovermode="x unified",
    )
    
    return fig


def emotion_radar(entries: List[Entry]) -> go.Figure:
    """Create radar chart of average emotions."""
    if not entries:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
        )
        return fig
    
    # Aggregate emotions
    emotion_sums = {emotion: 0.0 for emotion in EMOTIONS}
    count = 0
    
    for entry in entries:
        try:
            emotions = json.loads(entry.emotions_json)
            for emotion in EMOTIONS:
                emotion_sums[emotion] += emotions.get(emotion, 0.0)
            count += 1
        except Exception:
            continue
    
    if count == 0:
        emotion_avgs = {emotion: 0.0 for emotion in EMOTIONS}
    else:
        emotion_avgs = {emotion: emotion_sums[emotion] / count for emotion in EMOTIONS}
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatterpolar(
            r=[emotion_avgs[emotion] * 100 for emotion in EMOTIONS],
            theta=EMOTIONS,
            fill="toself",
            name="Average Emotions",
            line_color="rgb(20, 184, 166)",  # teal
        )
    )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
            ),
        ),
        showlegend=False,
        title="Emotion Distribution",
    )
    
    return fig


def tag_frequency(entries: List[Entry], top_n: int = 10) -> go.Figure:
    """Create bar chart of tag frequencies."""
    tag_counts = {}
    for entry in entries:
        if entry.tags:
            for tag in entry.tags.split(","):
                tag = tag.strip()
                if tag:
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    if not tag_counts:
        fig = go.Figure()
        fig.add_annotation(
            text="No tags available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
        )
        return fig
    
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:top_n]
    tags, counts = zip(*sorted_tags) if sorted_tags else ([], [])
    
    fig = px.bar(
        x=list(counts),
        y=list(tags),
        orientation="h",
        title="Tag Frequency",
        labels={"x": "Count", "y": "Tag"},
        color=list(counts),
        color_continuous_scale="Viridis",
    )
    
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        showlegend=False,
    )
    
    return fig


def hour_of_day_heatmap(entries: List[Entry]) -> go.Figure:
    """Create heatmap of mood by hour of day and day of week."""
    if not entries:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
        )
        return fig
    
    data = []
    for entry in entries:
        dt = datetime.fromtimestamp(entry.created_at)
        data.append({
            "hour": dt.hour,
            "day_of_week": dt.strftime("%A"),
            "mood_score": entry.mood_score,
        })
    
    df = pd.DataFrame(data)
    
    # Pivot table
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = df.pivot_table(
        values="mood_score",
        index="day_of_week",
        columns="hour",
        aggfunc="mean",
    )
    
    # Reorder rows
    pivot = pivot.reindex([d for d in days_order if d in pivot.index])
    
    fig = px.imshow(
        pivot,
        labels=dict(x="Hour of Day", y="Day of Week", color="Mood Score"),
        title="Mood by Hour and Day",
        color_continuous_scale="RdYlGn",
        aspect="auto",
    )
    
    fig.update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="Day of Week",
    )
    
    return fig


def calendar_heatmap(entries: List[Entry], year: Optional[int] = None) -> go.Figure:
    """Create calendar heatmap of mood scores."""
    if not entries:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
        )
        return fig
    
    if year is None:
        year = datetime.now().year
    
    # Create date range for the year
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    
    # Group entries by date
    mood_by_date = {}
    for entry in entries:
        date = datetime.fromtimestamp(entry.created_at).date()
        if start_date.date() <= date <= end_date.date():
            if date not in mood_by_date:
                mood_by_date[date] = []
            mood_by_date[date].append(entry.mood_score)
    
    # Calculate average mood per date
    avg_mood = {date: sum(scores) / len(scores) for date, scores in mood_by_date.items()}
    
    # Create data for heatmap
    dates = list(avg_mood.keys())
    moods = list(avg_mood.values())
    
    if not dates:
        fig = go.Figure()
        fig.add_annotation(
            text="No data for this year",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
        )
        return fig
    
    # Convert to strings for display
    date_strs = [d.strftime("%Y-%m-%d") for d in dates]
    
    fig = go.Figure(data=go.Scatter(
        x=date_strs,
        y=[1] * len(date_strs),
        mode="markers",
        marker=dict(
            size=20,
            color=moods,
            colorscale="RdYlGn",
            showscale=True,
            colorbar=dict(title="Mood Score"),
        ),
        text=[f"Date: {d}<br>Mood: {m:.1f}" for d, m in zip(date_strs, moods)],
        hovertemplate="%{text}<extra></extra>",
    ))
    
    fig.update_layout(
        title=f"Mood Calendar Heatmap ({year})",
        xaxis_title="Date",
        yaxis=dict(showticklabels=False, range=[0, 2]),
        height=200,
    )
    
    return fig


def sentiment_distribution(entries: List[Entry]) -> go.Figure:
    """Create histogram of sentiment distribution."""
    if not entries:
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
        )
        return fig
    
    sentiments = [e.sentiment for e in entries]
    
    fig = px.histogram(
        x=sentiments,
        nbins=20,
        title="Sentiment Distribution",
        labels={"x": "Sentiment (-1 to 1)", "y": "Frequency"},
        color_discrete_sequence=[MOOD_COLORS["medium_high"]],
    )
    
    fig.update_layout(
        xaxis_range=[-1, 1],
    )
    
    return fig


