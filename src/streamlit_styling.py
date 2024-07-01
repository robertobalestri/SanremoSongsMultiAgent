#streamòit_styling.py
import streamlit as st

def initialize_styling():
    # Set page configuration for wide layout
    st.set_page_config(layout="wide")

    # CSS for custom styling
    st.markdown("""
        <style>
            .lyrics-container {
                font-family: 'Courier New', Courier, monospace;
                white-space: pre-wrap; /* Preserve whitespace */
                background: #f4f4f4; /* Light grey background */
                padding: 20px; /* Some padding for better readability */
                border-radius: 10px; /* Rounded corners */
                border: 1px solid #ddd; /* Light border */
                overflow-y: auto; /* Enable vertical scrolling if needed */
                height: 100%;
                color: #333; /* Dark text color */
            }
            .lyrics-container p {
                margin: 0; /* Remove default paragraph margin */
                line-height: 1.5; /* Improve line spacing */
            }
            .user-message {
                background-color: #D6EAF8;
                color: black;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            .assistant-message {
                background-color: #FADBD8;
                color: black;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 10px;
            }
            .markdown h1, .markdown h2, .markdown h3, .markdown h4, .markdown h5, .markdown h6 {
                color: black !important;
            }
            
            
        </style>
    """, unsafe_allow_html=True)