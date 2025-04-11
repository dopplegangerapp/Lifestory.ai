
import streamlit as st
import requests

def create_interview_ui():
    """Create an engaging and supportive interview UI."""
    
    # Initialize session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = "Ready to begin your life story interview?"
    if 'stage' not in st.session_state:
        st.session_state.stage = "welcome"
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    if 'started' not in st.session_state:
        st.session_state.started = False
    if 'answers' not in st.session_state:
        st.session_state.answers = []

    # Create a clean, minimal container
    with st.container():
        # Progress bar
        st.progress(st.session_state.progress)

        # Current question display
        st.markdown(f"<div style='text-align: center; margin: 0.5rem 0;'>{st.session_state.current_question}</div>", unsafe_allow_html=True)

        # Input section
        if not st.session_state.started:
            if st.button("Start Interview", use_container_width=True):
                st.session_state.started = True
                try:
                    response = requests.get("http://0.0.0.0:5000/interview")
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.current_question = data.get("question", "What's your name?")
                        st.session_state.stage = data.get("current_stage", "welcome")
                        st.session_state.progress = float(data.get("progress", 0)) / 100
                        st.rerun()
                    else:
                        st.error(f"Server error: {response.status_code}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
        else:
            answer = st.text_area("Your answer:", key="answer_input", height=100, max_chars=1000)
            
            # Only show the continue button if there's an answer
            if answer and st.button("Continue", use_container_width=True):
                try:
                    response = requests.post(
                        "http://0.0.0.0:5000/interview",
                        json={"answer": answer}
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        
                        # Store the answer and clear input
                        st.session_state.answers.append(answer)
                        st.session_state.answer_input = ""
                        
                        # Update progress
                        if "progress" in data:
                            st.session_state.progress = float(data.get("progress", 0)) / 100
                        
                        # Handle next question or completion
                        next_question = data.get("next_question")
                        if next_question:
                            st.session_state.current_question = next_question
                            if "current_stage" in data:
                                st.session_state.stage = data["current_stage"]
                            st.experimental_rerun()
                        elif data.get("completed", False):
                            st.success("Interview completed!")
                            st.session_state.current_question = "Thank you for sharing your story!"
                        else:
                            st.error("No next question received from server")
                            st.session_state.current_question = "Thank you for sharing your story!"
                        else:
                            st.error("No next question received")
                    else:
                        st.error(f"Failed to submit answer: {response.status_code}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
