import streamlit as st
import requests

def create_interview_ui():
    """Create an engaging and supportive interview UI."""
    st.title("Your Life Story Interview")

    # Initialize session state for interview if not exists
    if 'backend_url' not in st.session_state:
        st.session_state.backend_url = "http://localhost:5000"
    if 'current_question' not in st.session_state:
        st.session_state.current_question = "Ready to begin your life story interview?"
    if 'stage' not in st.session_state:
        st.session_state.stage = "welcome"
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    if 'started' not in st.session_state:
        st.session_state.started = False

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
            .interview-container {
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }

            .stButton {
                margin: 10px 0;
            }

            .stTextInput, .stTextArea {
                margin: 15px 0;
            }

            .stMarkdown {
                margin: 20px 0;
            }

            .element-container {
                margin: 10px 0;
            }

            .stSelectbox {
                margin: 15px 0;
            }

            /* Fix overlapping issues */
            div[data-testid="stVerticalBlock"] > div {
                margin-bottom: 15px;
            }

            /* Ensure proper spacing between elements */
            .row-widget {
                margin: 10px 0;
            }
        </style>
    """, unsafe_allow_html=True)

    # Display progress
    st.progress(st.session_state.progress)

    # Display current question
    st.header(st.session_state.current_question)

    # Start button for initial question
    if not st.session_state.started:
        if st.button("Start Interview"):
            st.session_state.started = True
            try:
                response = requests.get(f"{st.session_state.backend_url}/interview")
                data = response.json()
                st.session_state.current_question = data.get("question", "What's your name?")
                st.session_state.stage = data.get("current_stage", "welcome")
                st.rerun()
            except Exception as e:
                st.error(f"Error starting interview: {str(e)}")
    else:
        # Answer input for ongoing interview
        answer = st.text_area("Your answer:", height=150)

        if st.button("Continue"):
            if answer:
                try:
                    response = requests.post(
                        f"{st.session_state.backend_url}/interview",
                        json={"answer": answer}
                    )
                    data = response.json()

                    # Update session state with new data
                    st.session_state.current_question = data.get("next_question", "Thank you for sharing!")
                    st.session_state.stage = data.get("current_stage", "complete")
                    st.session_state.progress = data.get("progress", 100)

                    if data.get("completed", False):
                        st.success("Interview completed! Thank you for sharing your story.")
                        st.session_state.started = False

                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")