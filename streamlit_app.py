import streamlit as st
import subprocess
import time

# Start Flask server
subprocess.Popen(["python", "app.py"])

# Wait for Flask to start
time.sleep(5)

st.set_page_config(
    page_title="Smart Home Dashboard",
    layout="wide"
)

st.markdown(
    """
    <style>
    .block-container{
        padding-top:0rem;
        padding-bottom:0rem;
        padding-left:0rem;
        padding-right:0rem;
    }
    iframe{
        border:none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.components.v1.iframe(
    "http://localhost:5000",
    height=1000,
    scrolling=True
)
