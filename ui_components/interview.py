
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
    st.markdown("""
        <style>
        .stApp {
            background-color: black;
            height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        
        .title {
            color: #0096FF;
            font-size: 32px;
            text-align: center;
            margin: 10px 0;
            font-family: 'Arial Black', sans-serif;
        }
        
        .orb {
            width: 150px;
            height: 150px;
            margin: 10px auto;
            background: radial-gradient(circle at 30% 30%, #00ffdd, #006666);
            border-radius: 50%;
            box-shadow: 0 0 30px #00ffdd55;
            animation: pulse 4s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(1); opacity: 0.8; }
        }
        
        .copyright {
            position: fixed;
            bottom: 10px;
            width: 100%;
            text-align: center;
            color: white;
            left: 0;
            font-size: 12px;
        }
        
        .stTextInput > div > div {
            background-color: rgba(255, 255, 255, 0.1);
            border-color: #0096FF;
            border-radius: 5px;
            color: white;
        }
        
        .stButton > button {
            background-color: transparent;
            color: #0096FF;
            border: 2px solid #0096FF;
            border-radius: 5px;
            padding: 8px 24px;
            font-size: 16px;
            transition: all 0.3s;
            width: 160px;
            margin: 10px auto;
            display: block;
        }
        
        .stButton > button:hover {
            background-color: #0096FF;
            color: black;
        }
        
        div[data-testid="stVerticalBlock"] {
            gap: 0em;
        }

        .question-text {
            text-align: center;
            color: white;
            margin: 10px 0;
            font-size: 20px;
        }

        .stProgress {
            margin: 5px 0;
        }

        div[data-testid="stForm"] {
            background-color: transparent;
            border: none;
            padding: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="orb"></div>', unsafe_allow_html=True)

    if "started" not in st.session_state:
        reset_session()

    try:
        if not st.session_state.started:
            st.markdown('<h2 class="question-text">I\'m DROE, Let\'s talk about your life.<br>What\'s your name?</h2>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                name = st.text_input("", key="name_input", label_visibility="collapsed")
                if st.button("CONTINUE"):
                    try:
                        response = requests.get("http://0.0.0.0:5000/interview", timeout=5)
                        data = response.json()
                        if response.status_code == 200 and data and "question" in data:
                            st.session_state.started = True
                            st.session_state.current_question = data["question"]
                            st.session_state.stage = data.get("current_stage", "welcome")
                            st.session_state.name = name
                            st.rerun()
                        else:
                            st.error(f"Server response error: {response.status_code}")
                    except requests.exceptions.ConnectionError:
                        st.error("Failed to connect to server. Please try again.")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
        else:
            if st.session_state.progress > 0:
                st.progress(st.session_state.progress / 100)

            st.markdown(f'<h2 class="question-text">{st.session_state.current_question}</h2>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                answer = st.text_input("", key="answer_input", label_visibility="collapsed")
                if st.button("CONTINUE"):
                    if answer.strip():
                        try:
                            response = requests.post(
                                "http://0.0.0.0:5000/interview",
                                json={"answer": answer.strip()},
                                timeout=5
                            )
                            if response.status_code == 200:
                                data = response.json()
                                if data.get("completed", False):
                                    st.session_state.started = False
                                    st.rerun()
                                else:
                                    st.session_state.current_question = data.get("next_question")
                                    st.session_state.stage = data.get("current_stage")
                                    st.session_state.progress = float(data.get("progress", 0))
                                    st.rerun()
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")

        st.markdown('<div class="copyright">COPYRIGHT 2025 REAL KEED</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        if st.button("Reset Interview"):
            reset_session()
            st.rerun()
