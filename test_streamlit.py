"""Test script to verify Streamlit works."""
import streamlit as st

st.set_page_config(
    page_title="Test",
    page_icon="🌊",
    layout="wide",
)

st.title("Test Page")
st.write("If you see this, Streamlit is working!")
st.write("Now try running: py -m streamlit run app.py")


