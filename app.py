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
        st.header("Interview")
        
        # Get current interview state
        interview_data = get_interview()
        if interview_data:
            st.session_state.interview_data = interview_data
            
            # Display current question
            st.write(f"**Question:** {interview_data['question']}")
            if interview_data.get('context'):
                st.write(f"*{interview_data['context']}*")
            
            # Display progress
            st.progress(interview_data['progress'] / 100)
            st.write(f"Progress: {interview_data['progress']:.1f}%")
            
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