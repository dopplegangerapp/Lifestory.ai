
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
    if 'error_count' not in st.session_state:
        st.session_state.error_count = 0

    # Create a clean, minimal container
    with st.container():
        # Progress bar
        st.progress(st.session_state.progress)

        # Current question display
        st.markdown(f"### {st.session_state.current_question}")

        # Input section
        if not st.session_state.started:
            if st.button("Start Interview", use_container_width=True):
                st.session_state.started = True
                try:
                    response = requests.get("http://0.0.0.0:5000/interview", timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.current_question = data.get("question", "What's your name?")
                        st.session_state.stage = data.get("current_stage", "welcome")
                        st.session_state.progress = float(data.get("progress", 0)) / 100
                        st.experimental_rerun()
                except Exception as e:
                    st.error(f"Failed to start interview: {str(e)}")
                    st.session_state.started = False
        else:
            # Text input for answer
            answer = st.text_input("Your answer:", key="answer_input")
            
            # Continue button
            if answer and st.button("Continue", use_container_width=True):
                try:
                    response = requests.post(
                        "http://0.0.0.0:5000/interview",
                        json={"answer": answer, "stage": st.session_state.stage},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.error_count = 0
                        
                        # Update progress
                        if "progress" in data:
                            st.session_state.progress = float(data.get("progress", 0)) / 100
                        
                        # Store answer
                        st.session_state.answers.append({
                            "answer": answer,
                            "stage": st.session_state.stage
                        })
                        
                        # Handle next question or completion
                        next_question = data.get("next_question")
                        if next_question:
                            st.session_state.current_question = next_question
                            if "current_stage" in data:
                                st.session_state.stage = data["current_stage"]
                            st.session_state.answer_input = ""
                            st.experimental_rerun()
                        elif data.get("completed", False):
                            st.success("Interview completed!")
                            st.session_state.current_question = "Thank you for sharing your story!"
                            st.session_state.started = False
                            st.experimental_rerun()
                    else:
                        st.error(f"Server error: {response.status_code}")
                        st.session_state.error_count += 1
                        if st.session_state.error_count > 3:
                            st.session_state.started = False
                            st.error("Too many errors occurred. Please try again.")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
                    st.session_state.error_count += 1
                    if st.session_state.error_count > 3:
                        st.session_state.started = False
                        st.error("Too many errors occurred. Please try again.")
