"""Settings page for configuration and export/import."""
import streamlit as st
from datetime import datetime
from core.db import init_db, get_or_create_user, get_entries
from core.export_import import export_to_csv, export_to_json, import_from_csv, import_from_json
from core.auth import check_auth, logout
from core.config import OPENAI_API_KEY, OPENAI_MODEL, APP_AUTH_PIN
from core.styles import apply_beach_theme
import os

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
st.title("⚙️ Settings")
st.markdown("Configure your app and manage your data.")

# Theme settings
st.divider()
st.subheader("Theme")
theme = st.selectbox(
    "Theme",
    options=["Light", "Dark", "Auto"],
    index=2,
    help="Select app theme",
)

# Privacy settings
st.divider()
st.subheader("Privacy")
scrub_pii = st.checkbox(
    "Scrub PII (Personally Identifiable Information)",
    value=st.session_state.get("scrub_pii", False),
    help="Remove emails, phone numbers, and other PII from entries before saving",
)

if scrub_pii:
    st.session_state.scrub_pii = True
else:
    st.session_state.scrub_pii = False

# Export data
st.divider()
st.subheader("Export Data")
st.markdown("Export your entries as CSV or JSON.")

col1, col2 = st.columns(2)

with col1:
    if st.button("Export as CSV", use_container_width=True):
        entries = get_entries(user_id=user.id)
        if entries:
            csv_data = export_to_csv(entries)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"moodmeter_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True,
            )
        else:
            st.info("No entries to export.")

with col2:
    if st.button("Export as JSON", use_container_width=True):
        entries = get_entries(user_id=user.id)
        if entries:
            json_data = export_to_json(entries)
            st.download_button(
                label="Download JSON",
                data=json_data,
                file_name=f"moodmeter_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
            )
        else:
            st.info("No entries to export.")

# Import data
st.divider()
st.subheader("Import Data")
st.markdown("Import entries from CSV or JSON files.")

uploaded_file = st.file_uploader(
    "Choose a file",
    type=["csv", "json"],
    help="Upload a CSV or JSON file to import entries",
)

if uploaded_file:
    file_ext = uploaded_file.name.split(".")[-1].lower()
    
    if st.button("Import", use_container_width=True):
        content = uploaded_file.read().decode("utf-8")
        
        if file_ext == "csv":
            result = import_from_csv(content, user.id)
        elif file_ext == "json":
            result = import_from_json(content, user.id)
        else:
            st.error("Unsupported file format. Please upload a CSV or JSON file.")
            result = None
        
        if result:
            if result["imported"] > 0:
                st.success(f"Successfully imported {result['imported']} entries.")
            if result["errors"] > 0:
                st.warning(f"Failed to import {result['errors']} entries.")
            st.rerun()

# API configuration
st.divider()
st.subheader("API Configuration")
st.markdown("Configure OpenAI API settings.")

col1, col2 = st.columns(2)

with col1:
    st.info(f"**Current Model:** {OPENAI_MODEL}")
    st.info(f"**API Key Set:** {'Yes' if OPENAI_API_KEY else 'No'}")

with col2:
    st.warning("⚠️ **Note:** API keys are configured via environment variables (.env file). Changes here require app restart.")

# Token Usage & Cost Tracking
st.divider()
st.subheader("📊 API Token Usage & Cost")
st.markdown("Track your OpenAI API usage and costs.")

# Load entries for token stats
entries_for_stats = get_entries(user_id=user.id)

if entries_for_stats:
    from core.token_usage import get_token_usage_stats
    
    stats = get_token_usage_stats(entries_for_stats)
    
    if stats["total_tokens"] > 0:
        # Main stats
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Tokens Used",
                f"{stats['total_tokens']:,}",
                help="Total number of API tokens consumed across all entries",
            )
        
        with col2:
            st.metric(
                "Total Cost (USD)",
                f"${stats['total_cost']:.4f}",
                help="Estimated total cost based on model pricing",
            )
        
        with col3:
            st.metric(
                "Avg Tokens/Entry",
                f"{stats['average_tokens_per_entry']:.0f}",
                help="Average number of tokens per entry",
            )
        
        # Detailed breakdown by model
        st.markdown("#### Breakdown by Model")
        
        if stats["model_usage"]:
            model_df_data = []
            for model, data in stats["model_usage"].items():
                model_df_data.append({
                    "Model": model,
                    "Tokens": f"{data['tokens']:,}",
                    "Entries": data["count"],
                    "Cost (USD)": f"${data['cost']:.4f}",
                })
            
            import pandas as pd
            model_df = pd.DataFrame(model_df_data)
            st.dataframe(model_df, use_container_width=True, hide_index=True)
        
        # Cost estimate info
        st.info(
            "💰 **Cost Calculation:** "
            "Costs are estimated based on OpenAI's pricing (as of 2024). "
            "Input tokens (~70%) and output tokens (~30%) are estimated from total tokens. "
            "Actual costs may vary. Prices shown are in USD."
        )
        
        # Fun stats
        st.markdown("#### Usage Statistics")
        col1, col2 = st.columns(2)
        
        with col1:
            entries_with_api = stats["entries_with_tokens"]
            total_entries = len(entries_for_stats)
            api_percentage = (entries_with_api / total_entries * 100) if total_entries > 0 else 0
            st.metric(
                "Entries with API Analysis",
                f"{entries_with_api} / {total_entries} ({api_percentage:.1f}%)",
            )
        
        with col2:
            if stats["total_tokens"] > 0:
                # Estimate how many more entries they can make with typical usage
                avg_tokens = stats["average_tokens_per_entry"]
                if avg_tokens > 0:
                    # Rough estimate: $10 budget = how many entries?
                    budget_10_usd = (10.0 / stats["total_cost"]) * entries_with_api if stats["total_cost"] > 0 else 0
                    st.metric(
                        "Estimated Entries per $10",
                        f"~{budget_10_usd:.0f}" if budget_10_usd > 0 else "N/A",
                    )
    else:
        st.info("📊 No API tokens used yet. Token usage will appear here after you check in with AI analysis enabled.")
else:
    st.info("📊 No entries yet. Token usage will appear here after you start checking in.")


# Authentication
st.divider()
st.subheader("Authentication")
st.markdown("Manage your authentication settings.")

col1, col2 = st.columns(2)

with col1:
    st.info(f"**Current PIN:** {APP_AUTH_PIN}")
    st.warning("⚠️ **Note:** PIN is configured via environment variables (.env file). Changes here require app restart.")

with col2:
    if st.button("Logout", use_container_width=True):
        logout()

# Database info
st.divider()
st.subheader("Database Information")
st.markdown("View database statistics.")

# Get entries for database stats
db_entries = get_entries(user_id=user.id)
if db_entries:
    st.info(f"**Total Entries:** {len(db_entries)}")
    st.info(f"**Database Location:** sqlite:///moodmeter.db")
else:
    st.info("No entries in database.")

# About
st.divider()
st.subheader("About")
st.markdown("""
**Student Moodmeter** 🌊

A calm, beach-themed web app where students check in their mood, journal briefly, and get AI sentiment + emotion analysis, trend insights, and gentle suggestions.

**Features:**
- Mood check-in with AI analysis
- Journal with search and filters
- Comprehensive analytics dashboard
- Export/import functionality
- Privacy-focused design

**Version:** 1.0.0
**Built with:** Streamlit, OpenAI, SQLite
""")

