import streamlit as st
import requests
from time import sleep

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
        st.markdown(f"### {st.session_state.current_question}")

        # Input section
        if not st.session_state.started:
            if st.button("Start Interview", use_container_width=True):
                try:
                    response = requests.get("http://0.0.0.0:5000/interview")
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.started = True
                        st.session_state.current_question = data.get("question", "What's your name?")
                        st.session_state.stage = data.get("current_stage", "welcome")
                        st.session_state.progress = float(data.get("progress", 0)) / 100
                        st.rerun()
                except Exception as e:
                    st.error(f"Unable to connect to server. Please ensure the API is running.")
                    st.session_state.started = False
        else:
            answer = st.text_input("Your answer:", key="answer_input")

            if answer and st.button("Continue", use_container_width=True):
                try:
                    response = requests.post(
                        "http://0.0.0.0:5000/interview",
                        json={"answer": answer},
                        timeout=5
                    )

                    if response.status_code == 200:
                        data = response.json()

                        # Store answer
                        st.session_state.answers.append({
                            "question": st.session_state.current_question,
                            "answer": answer,
                            "stage": st.session_state.stage
                        })

                        # Update progress
                        if "progress" in data:
                            st.session_state.progress = float(data.get("progress", 0)) / 100

                        # Handle next question or completion
                        next_question = data.get("next_question")
                        if next_question:
                            st.session_state.current_question = next_question
                            if "current_stage" in data:
                                st.session_state.stage = data["current_stage"]
                            st.session_state.answer_input = ""
                            st.rerun()
                        elif data.get("completed", False):
                            st.success("Interview completed!")
                            st.session_state.current_question = "Thank you for sharing your story!"
                            st.session_state.started = False
                            st.rerun()
                    else:
                        st.error("Server error. Please try again.")
                except requests.exceptions.RequestException as e:
                    st.error("Unable to connect to server. Please ensure the API is running.")
                    st.session_state.started = False