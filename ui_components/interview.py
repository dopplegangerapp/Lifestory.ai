import streamlit as st
import requests

def render():
    st.title("Life Story Interview")

    if "started" not in st.session_state:
        st.session_state.started = False
    if 'answers' not in st.session_state:
        st.session_state.answers = []

    if not st.session_state.started:
        if st.button("Start Interview", use_container_width=True):
            try:
                response = requests.get("http://0.0.0.0:5000/interview")
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.started = True
                    st.session_state.current_question = data.get("question")
                    st.session_state.stage = data.get("current_stage")
                    st.session_state.progress = float(data.get("progress", 0))
                    st.rerun()
            except Exception as e:
                st.error("Connection error. Please try again.")
    else:
        st.progress(st.session_state.get("progress", 0))
        st.write(st.session_state.get("current_question"))
        answer = st.text_area("Your answer:")

        if st.button("Continue", use_container_width=True) and answer:
            try:
                response = requests.post(
                    "http://0.0.0.0:5000/interview",
                    json={"answer": answer}
                )

                if response.status_code == 200:
                    data = response.json()
                    
                    # Store answer (from original code)
                    st.session_state.answers.append({
                        "question": st.session_state.current_question,
                        "answer": answer,
                        "stage": st.session_state.stage
                    })

                    if data.get("completed"):
                        st.success("Interview completed!")
                        st.session_state.started = False
                    else:
                        st.session_state.current_question = data.get("next_question")
                        st.session_state.stage = data.get("current_stage")
                        st.session_state.progress = float(data.get("progress", 0))
                        st.rerun()
            except Exception as e:
                st.error("Error submitting answer. Please try again.")