
import streamlit as st
import requests

def create_interview_ui():
    """Create an engaging and supportive interview UI."""
    st.title("Your Life Story Interview")
    
    # Initialize session state for interview
    if 'current_question' not in st.session_state:
        st.session_state.current_question = "Ready to begin your life story interview?"
    if 'stage' not in st.session_state:
        st.session_state.stage = "foundations"
    if 'progress' not in st.session_state:
        st.session_state.progress = 0

    # Create the orb animation
    st.markdown("""
        <div style="text-align: center; margin: 2rem;">
            <div style="width: 100px; height: 100px; margin: 0 auto; border-radius: 50%; 
                 background: radial-gradient(circle, #448aff, #1a237e);
                 animation: pulse 2s infinite;">
            </div>
        </div>
        <style>
            @keyframes pulse {
                0% { transform: scale(1); opacity: 0.7; }
                50% { transform: scale(1.1); opacity: 1; }
                100% { transform: scale(1); opacity: 0.7; }
            }
        </style>
    """, unsafe_allow_html=True)

    # Display progress
    st.progress(st.session_state.progress)
    
    # Display current question
    st.header(st.session_state.current_question)
    
    # Answer input
    answer = st.text_area("Your answer:", height=150)
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("Submit"):
            if answer:
                try:
                    response = requests.post(f"{st.session_state.backend_url}/interview",
                                          json={"answer": answer})
                    data = response.json()
                    st.session_state.current_question = data.get("question", "Thank you for sharing!")
                    st.session_state.stage = data.get("current_stage", "complete")
                    st.session_state.progress = data.get("progress", 100)
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
