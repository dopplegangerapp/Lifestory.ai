import streamlit as st
import requests

def create_interview_ui():
    """Create an engaging and supportive interview UI."""

    # Initialize session state for interview if not exists
    if 'backend_url' not in st.session_state:
        st.session_state.backend_url = "http://0.0.0.0:5000"
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
        st.session_state.started = False
        st.session_state.current_stage = "foundations"
        st.session_state.progress = 0

    # Create a clean, minimal container
    with st.container():
        st.markdown("<h2 style='text-align: center; margin-bottom: 1rem;'>Your Life Story</h2>", unsafe_allow_html=True)

        # Progress bar
        st.progress(st.session_state.progress)

        # Current question display
        st.markdown(f"<h3 style='text-align: center; margin: 1rem 0;'>{st.session_state.current_question}</h3>", unsafe_allow_html=True)

        # Input section
        if not st.session_state.started:
            if st.button("Start Interview", use_container_width=True):
                st.session_state.started = True
                st.rerun()
        else:
            answer = st.text_area("Your answer:", key="answer_input", height=150)
            if st.button("Continue", use_container_width=True) and answer:
                # Process answer and update progress
                st.session_state.answers.append(answer)
                st.session_state.progress += 0.2
                if st.session_state.progress >= 1.0:
                    st.session_state.progress = 1.0
                st.rerun()

    # This section is removed as the logic is handled within the container above.
    #The following code is removed because the functionality is integrated into the main container above.
    # Display progress
    #st.progress(st.session_state.progress)

    # Display current question in the center column
    #with col2:
    #    st.markdown(f"<h3 style='text-align: center; margin: 1rem 0;'>{st.session_state.current_question}</h3>", unsafe_allow_html=True)

        # Start button for initial question
        #if not st.session_state.started:
        #    if st.button("Start Interview", use_container_width=True):
        #        st.session_state.started = True
        #        try:
        #            response = requests.get(f"{st.session_state.backend_url}/interview")
        #            data = response.json()
        #            st.session_state.current_question = data.get("question", "What's your name?")
        #            st.session_state.stage = data.get("current_stage", "welcome")
        #            st.rerun()
        #        except Exception as e:
        #            st.error(f"Error starting interview: {str(e)}")
        #else:
            # Answer input for ongoing interview
            #answer = st.text_area("Your answer:", height=150, key="answer_input")

            #if st.button("Continue", use_container_width=True):
            #    if answer:
            #        try:
            #            response = requests.post(
            #            f"{st.session_state.backend_url}/interview",
            #            json={"answer": answer}
            #        )
            #        data = response.json()

                    # Update session state with new data
            #        st.session_state.current_question = data.get("next_question", "Thank you for sharing!")
            #        st.session_state.stage = data.get("current_stage", "complete")
            #        st.session_state.progress = data.get("progress", 100)

                    #if data.get("completed", False):
            #        st.success("Interview completed! Thank you for sharing your story.")
            #        st.session_state.started = False

            #        st.rerun()
            #    except Exception as e:
            #        st.error(f"Error: {str(e)}")