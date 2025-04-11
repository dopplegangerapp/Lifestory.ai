import streamlit as st
import os
from ui_components.styles import add_custom_styles
from ui_components.timeline import create_timeline_ui
from ui_components.interview import render as create_interview_ui

# Set environment variable to skip email prompt
os.environ['STREAMLIT_SERVER_EMAIL'] = ''

# Configure Streamlit page
st.set_page_config(
    page_title="Lifestory.ai",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'backend_url' not in st.session_state:
    st.session_state.backend_url = "http://localhost:5001"  # Updated to match API server port

def main():
    # Add custom styles
    add_custom_styles()

    # Create layout
    st.markdown("""
        <div class="header">Lifestory.ai</div>
    """, unsafe_allow_html=True)

    # Show buttons only when not in interview mode
    if st.session_state.page != "interview":
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Start Interview", key="interview_btn"):
                st.session_state.page = "interview"
                st.rerun()
        with col2:
            if st.button("View Timeline", key="timeline_btn"):
                st.session_state.page = "timeline"
                st.rerun()
        with col3:
            if st.button("Browse Cards", key="cards_btn"):
                st.session_state.page = "cards"
                st.rerun()

    # Render the appropriate page
    if st.session_state.page == "interview":
        create_interview_ui()
    elif st.session_state.page == "timeline":
        create_timeline_ui()
    elif st.session_state.page == "cards":
        st.write("Cards view coming soon...")
    else:
        st.write("Welcome to Lifestory.ai! Click a button above to get started.")

if __name__ == "__main__":
    main() 