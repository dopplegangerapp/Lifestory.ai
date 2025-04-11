import streamlit as st
import requests
from time import sleep

def reset_session():
    st.session_state.started = False
    st.session_state.answers = []
    st.session_state.current_question = None
    st.session_state.stage = None
    st.session_state.progress = 0
    st.session_state.error = None

def render():
    st.title("Life Story Interview")

    # Initialize session state
    if "started" not in st.session_state:
        reset_session()

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
            # Show progress
            st.progress(st.session_state.progress / 100)

            # Show current stage if available
            if st.session_state.stage:
                st.write(f"Stage: {st.session_state.stage.title()}")

            # Show question and get answer
            st.write(st.session_state.current_question)

            col1, col2 = st.columns([4,1])

            with col1:
                answer = st.text_area("Your answer:", key="answer_input", height=100)

            with col2:
                if st.button("Continue", use_container_width=True, disabled=not answer):
                    try:
                        response = requests.post(
                            "http://0.0.0.0:5000/interview",
                            json={"answer": answer.strip()},
                            timeout=5
                        )

                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.current_question = data.get("question")
                            st.session_state.stage = data.get("current_stage")
                            st.session_state.progress = float(data.get("progress", 0))
                            if data.get("completed", False):
                                st.session_state.started = False
                            st.rerun()
                        else:
                            st.error("Failed to submit answer. Please try again.")
                            sleep(2)
                            st.rerun()
                    except requests.exceptions.RequestException as e:
                        st.error(f"Connection error: {str(e)}")
                        sleep(2)
                        st.rerun()

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        if st.button("Reset Interview"):
            reset_session()
            st.rerun()