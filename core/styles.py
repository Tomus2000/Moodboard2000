"""Shared styles and CSS for the app."""
import streamlit as st
import base64
from pathlib import Path
from core.config import ASSETS_DIR


def apply_beach_theme():
    """Apply black theme CSS to the app."""
    # Always use black theme
    apply_gradient_theme()


def apply_gradient_theme():
    """Apply black theme CSS as fallback."""
    st.markdown(
        """
        <style>
        /* Main app background - pure black */
        .stApp {{
            background: #000000 !important;
            color: #e0e0e0;
        }}
        
        /* Main content area */
        .main {{
            background: #000000 !important;
        }}
        
        /* Block containers */
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            background: #1a1a1a !important;
            border-radius: 10px;
        }}
        
        /* All text elements */
        h1, h2, h3, h4, h5, h6, p, div, span, label {{
            color: #e0e0e0 !important;
        }}
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background: #1a1a1a !important;
        }}
        [data-testid="stSidebar"] * {{
            color: #e0e0e0 !important;
        }}
        
        /* Text inputs */
        .stTextInput > div > div > input {{
            background: #2a2a2a !important;
            color: #ffffff !important;
            border-color: #444444 !important;
        }}
        textarea {{
            background: #2a2a2a !important;
            color: #ffffff !important;
        }}
        
        /* Buttons */
        .stButton > button {{
            background: #14b8a6 !important;
            color: #ffffff !important;
            border: none;
        }}
        .stButton > button:hover {{
            background: #0fa896 !important;
        }}
        
        /* Metrics */
        [data-testid="stMetricValue"] {{
            color: #ffffff !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: #b0b0b0 !important;
        }}
        
        /* Info boxes */
        .stAlert {{
            background: #2a2a2a !important;
            border-color: #444444 !important;
        }}
        
        /* Select boxes */
        .stSelectbox > div > div {{
            background: #2a2a2a !important;
            color: #ffffff !important;
        }}
        
        /* Dataframes */
        .stDataFrame {{
            background: #1a1a1a !important;
        }}
        
        /* Remove any white backgrounds */
        section[data-testid="stSidebar"] {{
            background: #1a1a1a !important;
        }}
        
        /* Ensure body is black */
        body {{
            background: #000000 !important;
        }}
        
        /* Expanders - better contrast */
        .streamlit-expanderHeader {{
            background: #1a1a1a !important;
            color: #e0e0e0 !important;
            border: 1px solid #444444 !important;
        }}
        
        .streamlit-expanderHeader:hover {{
            background: #2a2a2a !important;
        }}
        
        .streamlit-expanderContent {{
            background: #1a1a1a !important;
            color: #e0e0e0 !important;
            border: 1px solid #444444 !important;
            border-top: none !important;
        }}
        
        [data-testid="stExpander"] {{
            background: #1a1a1a !important;
            border: 1px solid #444444 !important;
        }}
        
        [data-testid="stExpanderDetails"] {{
            background: #1a1a1a !important;
            color: #e0e0e0 !important;
        }}
        
        [data-testid="stExpanderToggleIcon"] {{
            color: #e0e0e0 !important;
        }}
        
        /* Containers */
        .stContainer {{
            background: transparent !important;
        }}
        
        /* Dividers */
        hr {{
            border-color: #444444 !important;
        }}
        
        /* Captions and small text */
        .stMarkdown small, small {{
            color: #b0b0b0 !important;
        }}
        
        /* Subheader text */
        h3 {{
            color: #ffffff !important;
        }}
        
        /* Info boxes - better contrast */
        .stInfo {{
            background: #1a3a3a !important;
            border-color: #14b8a6 !important;
            color: #e0e0e0 !important;
        }}
        
        /* Success boxes */
        .stSuccess {{
            background: #1a3a2a !important;
            border-color: #10b981 !important;
            color: #e0e0e0 !important;
        }}
        
        /* Warning boxes */
        .stWarning {{
            background: #3a2a1a !important;
            border-color: #f59e0b !important;
            color: #e0e0e0 !important;
        }}
        
        /* Error boxes */
        .stError {{
            background: #3a1a1a !important;
            border-color: #ef4444 !important;
            color: #e0e0e0 !important;
        }}
        
        /* Date input */
        .stDateInput > div > div > input {{
            background: #2a2a2a !important;
            color: #ffffff !important;
        }}
        
        /* Multiselect */
        .stMultiSelect > div > div {{
            background: #2a2a2a !important;
            color: #ffffff !important;
        }}
        
        /* Checkbox */
        .stCheckbox label {{
            color: #e0e0e0 !important;
        }}
        
        /* Markdown code blocks and inline code */
        code {{
            background: #2a2a2a !important;
            color: #14b8a6 !important;
            padding: 0.2em 0.4em !important;
            border-radius: 3px !important;
        }}
        
        pre {{
            background: #1a1a1a !important;
            color: #e0e0e0 !important;
            border: 1px solid #444444 !important;
        }}
        
        /* Progress bars - better visibility */
        .stProgress > div > div > div {{
            background-color: #14b8a6 !important;
        }}
        
        /* Strong/bold text */
        strong, b {{
            color: #ffffff !important;
        }}
        
        /* Links */
        a {{
            color: #14b8a6 !important;
        }}
        
        a:hover {{
            color: #0fa896 !important;
        }}
        
        /* Ensure all markdown text is visible */
        .stMarkdown {{
            color: #e0e0e0 !important;
        }}
        
        .stMarkdown p {{
            color: #e0e0e0 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


