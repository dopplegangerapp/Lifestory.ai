import streamlit as st
import os
from ui_components.styles import add_custom_styles
from ui_components.timeline import create_timeline_ui
from ui_components.interview import render as create_interview_ui
import requests
import json
from datetime import datetime
import uuid

# Set environment variable to skip email prompt
os.environ['STREAMLIT_SERVER_EMAIL'] = ''

# Configure Streamlit page
st.set_page_config(
    page_title="Lifestory.ai",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme
st.markdown("""
    <style>
    .main {
        background-color: #000000;
        color: #ffffff;
    }
    .stApp {
        background-color: #000000;
    }
    /* Make all text white */
    .stMarkdown, .stText, .stTextInput, .stTextArea, .stButton, .stProgress {
        color: #ffffff !important;
    }
    /* Make headers and labels more visible */
    h1, h2, h3, h4, h5, h6, label {
        color: #ffffff !important;
    }
    /* Make expander headers visible */
    .streamlit-expanderHeader {
        color: #ffffff !important;
    }
    .stButton>button {
        background-color: #1a1a1a;
        color: #00a8ff;
        border: 2px solid #00a8ff;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-size: 1.1em;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00a8ff;
        color: #000000;
    }
    .stTextArea>div>div>textarea {
        background-color: #1a1a1a;
        color: #ffffff;
        border: 2px solid #00a8ff;
        border-radius: 5px;
    }
    .droe-orb {
        width: 200px;
        height: 200px;
        background: radial-gradient(circle at center, #00a8ff 0%, #000000 70%);
        border-radius: 50%;
        margin: 2rem auto;
        box-shadow: 0 0 30px #00a8ff;
        animation: pulse 2s infinite;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
    }
    .droe-orb::before {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle at center, rgba(0, 168, 255, 0.5) 0%, transparent 70%);
        border-radius: 50%;
        animation: glow 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 30px #00a8ff; }
        50% { transform: scale(1.05); box-shadow: 0 0 50px #00a8ff; }
        100% { transform: scale(1); box-shadow: 0 0 30px #00a8ff; }
    }
    @keyframes glow {
        0% { opacity: 0.5; }
        50% { opacity: 0.8; }
        100% { opacity: 0.5; }
    }
    .question-box {
        background-color: #1a1a1a;
        border: 2px solid #00a8ff;
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem 0;
        color: #ffffff;
    }
    .progress-box {
        background-color: #1a1a1a;
        border: 2px solid #00a8ff;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #ffffff;
    }
    .timeline-event {
        background-color: #1a1a1a;
        border: 2px solid #00a8ff;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #ffffff;
    }
    /* Make success and warning messages more visible */
    .stAlert {
        background-color: #1a1a1a !important;
        border: 2px solid #00a8ff !important;
        color: #ffffff !important;
    }
    .stSuccess {
        background-color: #1a1a1a !important;
        border: 2px solid #00ff00 !important;
        color: #ffffff !important;
    }
    .stWarning {
        background-color: #1a1a1a !important;
        border: 2px solid #ffff00 !important;
        color: #ffffff !important;
    }
    .stError {
        background-color: #1a1a1a !important;
        border: 2px solid #ff0000 !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'interview_data' not in st.session_state:
    st.session_state.interview_data = None

# API configuration
API_BASE_URL = "http://localhost:5001"

def get_interview():
    """Get the current interview state."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/interview",
            cookies={'session_id': st.session_state.session_id}
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error getting interview: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None

def submit_answer(answer):
    """Submit an answer to the current interview question."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/interview",
            json={'answer': answer},
            cookies={'session_id': st.session_state.session_id}
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error submitting answer: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None

def main():
    # Create layout
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #00a8ff;">Lifestory.ai</h1>
        </div>
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
        st.header("Interview")
        
        # Get current interview state
        interview_data = get_interview()
        if interview_data:
            st.session_state.interview_data = interview_data
            
            # DROE Orb
            st.markdown('<div class="droe-orb"></div>', unsafe_allow_html=True)
            
            # Display current question
            st.markdown('<div class="question-box">', unsafe_allow_html=True)
            st.write(f"**Question:** {interview_data['question']}")
            if interview_data.get('context'):
                st.write(f"*{interview_data['context']}*")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display progress
            st.markdown('<div class="progress-box">', unsafe_allow_html=True)
            st.progress(interview_data['progress'] / 100)
            st.write(f"Progress: {interview_data['progress']:.1f}%")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Answer input
            answer = st.text_area("Your answer:", key="answer_input")
            if st.button("Submit Answer"):
                if answer.strip():
                    result = submit_answer(answer)
                    if result:
                        st.success("Answer submitted successfully!")
                        st.rerun()
                else:
                    st.warning("Please enter an answer before submitting.")
            
            # Back button
            if st.button("Back to Home"):
                st.session_state.page = "home"
                st.rerun()
    elif st.session_state.page == "timeline":
        st.header("Timeline")
        
        # Get timeline data
        try:
            response = requests.get(
                f"{API_BASE_URL}/timeline",
                cookies={'session_id': st.session_state.session_id}
            )
            if response.status_code == 200:
                timeline_data = response.json()
                
                # Display timeline
                for event in timeline_data.get('timeline', []):
                    with st.expander(f"{event['title']} - {event['date']}"):
                        st.write(event['description'])
            else:
                st.error(f"Error getting timeline: {response.text}")
        except Exception as e:
            st.error(f"Error connecting to API: {str(e)}")
        
        # Back button
        if st.button("Back to Home"):
            st.session_state.page = "home"
            st.rerun()
    elif st.session_state.page == "cards":
        st.write("Cards view coming soon...")
    else:
        st.write("Welcome to Lifestory.ai! Click a button above to get started.")

if __name__ == "__main__":
    main() 