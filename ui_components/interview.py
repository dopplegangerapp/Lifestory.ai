
import streamlit as st
import requests
from typing import Dict, Any

def handle_error(error: str) -> None:
    """Display error message and reset interview if needed"""
    st.error(error)
    if "Connection refused" in error:
        st.warning("Please ensure the API server is running")
        if st.button("Reset Interview"):
            st.session_state.clear()
            st.rerun()

def render():
    st.title("Life Story Interview")
    
    # Initialize session state
    if "started" not in st.session_state:
        st.session_state.started = False
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "current_question" not in st.session_state:
        st.session_state.current_question = None
    if "stage" not in st.session_state:
        st.session_state.stage = None
    if "progress" not in st.session_state:
        st.session_state.progress = 0

    try:
        if not st.session_state.started:
            if st.button("Start Interview", use_container_width=True):
                response = requests.get("http://0.0.0.0:5000/interview")
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.started = True
                    st.session_state.current_question = data.get("question")
                    st.session_state.stage = data.get("current_stage")
                    st.session_state.progress = float(data.get("progress", 0))
                    st.rerun()
                else:
                    handle_error(f"Failed to start interview: {response.status_code}")
        else:
            # Show progress
            progress_val = st.session_state.progress / 100
            st.progress(progress_val)
            
            # Show current stage
            if st.session_state.stage:
                st.subheader(f"Stage: {st.session_state.stage.title()}")
            
            # Show question and get answer
            st.write(st.session_state.current_question)
            answer = st.text_area("Your answer:", key="answer_input")
            
            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("Reset"):
                    st.session_state.clear()
                    st.rerun()
                    
            with col2:
                if st.button("Continue", use_container_width=True, disabled=not answer):
                    response = requests.post(
                        "http://0.0.0.0:5000/interview",
                        json={"answer": answer.strip()}
                    )

                    if response.status_code == 200:
                        data = response.json()
                        
                        # Store answer
                        st.session_state.answers.append({
                            "question": st.session_state.current_question,
                            "answer": answer,
                            "stage": st.session_state.stage
                        })

                        if data.get("completed"):
                            st.success("Interview completed!")
                            st.session_state.started = False
                            st.session_state.current_question = None
                            st.balloons()
                            st.rerun()
                        else:
                            st.session_state.current_question = data.get("next_question")
                            st.session_state.stage = data.get("current_stage")
                            st.session_state.progress = float(data.get("progress", 0))
                            st.rerun()
                    else:
                        handle_error(f"Failed to submit answer: {response.status_code}")

    except requests.exceptions.ConnectionError:
        handle_error("Could not connect to server. Please ensure the API is running.")
    except Exception as e:
        handle_error(f"An error occurred: {str(e)}")

    # Show debug info in development
    if st.session_state.get("debug", False):
        st.write("Debug Info:")
        st.write(st.session_state)
