import streamlit as st
import os
from ui_components.styles import add_custom_styles
from ui_components.timeline import create_timeline_ui
from ui_components.interview import create_interview_ui

# Set environment variable to skip email prompt
os.environ['STREAMLIT_SERVER_EMAIL'] = ''

# Configure Streamlit page
st.set_page_config(
    page_title="Lifestory.ai",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # Add custom styles
    add_custom_styles()

    # Initialize session state
    if 'page' not in st.session_state:
        st.session_state.page = "home"
    
    # Initialize backend URL
    if 'backend_url' not in st.session_state:
        st.session_state.backend_url = "http://localhost:5000"

    # Create layout
    st.markdown("""
        <div class="header">Lifestory.ai</div>
    """, unsafe_allow_html=True)

    # Show buttons only when not in interview mode
    if st.session_state.page != "interview":
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("INTERVIEW", key="interview_btn"):
                st.session_state.page = "interview"
                st.rerun()
        with col2:
            if st.button("TIMELINE", key="timeline_btn"):
                st.session_state.page = "timeline"
                st.rerun()
        with col3:
            if st.button("CARDS", key="cards_btn"):
                st.session_state.page = "cards"
                st.rerun()

    st.markdown("""<div class="footer">Copyright 2025 ReaL KeeD</div>""", unsafe_allow_html=True)

    # Display appropriate UI based on current page
    if st.session_state.page == "interview":
        create_interview_ui()
    elif st.session_state.page == "timeline":
        create_timeline_ui()
    elif st.session_state.page == "cards":
        st.markdown("""
            <div class="cards-container">
                <div class="card">
                    <div class="card-orb"></div>
                    <h3>EVENTS</h3>
                </div>
                
                <div class="card">
                    <div class="card-orb"></div>
                    <h3>MEMORIES</h3>
                </div>
                
                <div class="card">
                    <div class="card-orb"></div>
                    <h3>PLACES</h3>
                </div>
                
                <div class="card">
                    <div class="card-orb"></div>
                    <h3>PEOPLE</h3>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.session_state.page = "interview"  # Default to interview mode

if __name__ == "__main__":
    main() 