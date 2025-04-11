
import streamlit as st
import requests

def render():
    st.title("Life Story Interview")

    # Initialize session state
    if "started" not in st.session_state:
        st.session_state.started = False
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'stage' not in st.session_state:
        st.session_state.stage = None
    if 'progress' not in st.session_state:
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
                    st.error(f"Server error: {response.status_code}")
        else:
            st.progress(st.session_state.progress)
            st.write(st.session_state.current_question)
            answer = st.text_area("Your answer:")

            if st.button("Continue", use_container_width=True) and answer:
                response = requests.post(
                    "http://0.0.0.0:5000/interview",
                    json={"answer": answer.strip()}
                )

                if response.status_code == 200:
                    data = response.json()
                    
                    st.session_state.answers.append({
                        "question": st.session_state.current_question,
                        "answer": answer,
                        "stage": st.session_state.stage
                    })

                    if data.get("completed"):
                        st.success("Interview completed!")
                        st.session_state.started = False
                        st.session_state.current_question = None
                        st.rerun()
                    else:
                        st.session_state.current_question = data.get("next_question")
                        st.session_state.stage = data.get("current_stage")
                        st.session_state.progress = float(data.get("progress", 0))
                        st.rerun()
                else:
                    st.error(f"Failed to submit answer. Status code: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to server. Please ensure the API is running.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
