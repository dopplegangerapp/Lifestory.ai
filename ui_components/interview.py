
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
    # Custom CSS for the new design
    st.markdown("""
        <style>
        .stApp {
            background-color: black;
        }
        
        .title {
            color: #0096FF;
            font-size: 48px;
            text-align: center;
            margin-bottom: 20px;
            font-family: 'Arial Black', sans-serif;
        }
        
        .orb {
            width: 200px;
            height: 200px;
            margin: 20px auto;
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
            bottom: 20px;
            width: 100%;
            text-align: center;
            color: white;
            left: 0;
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
            padding: 10px 30px;
            font-size: 18px;
            transition: all 0.3s;
            width: 200px;
            margin: 0 auto;
            display: block;
        }
        
        .stButton > button:hover {
            background-color: #0096FF;
            color: black;
        }
        
        div[data-testid="stVerticalBlock"] {
            gap: 0em;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown('<h1 class="title">LIFESTORY.AI</h1>', unsafe_allow_html=True)
    
    # Animated orb
    st.markdown('<div class="orb"></div>', unsafe_allow_html=True)

    # Initialize session state
    if "started" not in st.session_state:
        reset_session()

    try:
        if not st.session_state.started:
            # Center align text
            st.markdown('<h2 style="text-align: center; color: white; margin: 20px 0;">I\'m DROE, Let\'s talk about your life.<br>What\'s your name?</h2>', unsafe_allow_html=True)
            
            # Create columns for centering
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                name = st.text_input("", key="name_input", label_visibility="collapsed")
                if st.button("CONTINUE"):
                    try:
                        response = requests.get("http://0.0.0.0:5000/interview", timeout=5)
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.started = True
                            st.session_state.current_question = data.get("question")
                            st.session_state.stage = data.get("current_stage")
                            st.session_state.name = name
                            st.rerun()
                    except requests.exceptions.ConnectionError:
                        st.error("Failed to connect to server. Please try again.")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")
        else:
            # Show progress
            if st.session_state.progress > 0:
                st.progress(st.session_state.progress / 100)

            # Show current question
            st.markdown(f'<h2 style="text-align: center; color: white; margin: 20px 0;">{st.session_state.current_question}</h2>', unsafe_allow_html=True)
            
            # Create columns for centering
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

        # Copyright notice
        st.markdown('<div class="copyright">COPYRIGHT 2025 REAL KEED</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        if st.button("Reset Interview"):
            reset_session()
            st.rerun()
