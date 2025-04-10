import streamlit as st
import requests
from datetime import datetime
import time

def create_interview_ui():
    """Create an engaging and supportive interview UI with DROE's presence."""
    
    # Initialize session state for interview
    if 'interview_stage' not in st.session_state:
        st.session_state.interview_stage = 0
    if 'interview_answers' not in st.session_state:
        st.session_state.interview_answers = {}
    
    # Check if backend URL is initialized
    if 'backend_url' not in st.session_state:
        st.error("Backend server not initialized. Please restart the application.")
        return

    st.markdown("""
        <div class="droe-orb-container">
            <div class="droe-orb"></div>
        </div>

        <div class="chat-container">
            <div class="message droe-message">
                WELCOME TO LIFESTORY.AI
                I AM DROE
            </div>
        </div>

        <style>
        .chat-container {
            max-width: 800px;
            margin: 2rem auto;
            padding: 1rem;
        }

        .message {
            margin: 1rem 0;
            padding: 1.5rem;
            border-radius: 8px;
            font-family: 'Arial', sans-serif;
            font-weight: bold;
            letter-spacing: 1px;
            text-transform: uppercase;
            border: 1px solid var(--glow-teal);
            background: rgba(255, 255, 255, 0.05);
            box-shadow: 0 0 20px rgba(74, 237, 196, 0.2);
        }

        .droe-message {
            margin-right: 20%;
            color: var(--glow-teal);
        }

        .user-message {
            margin-left: 20%;
            text-align: right;
            color: white;
        }

        .chat-input {
            margin-top: 2rem;
            width: 100%;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--glow-teal);
            color: white;
            padding: 1rem;
            font-family: 'Arial', sans-serif;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        </style>
    """, unsafe_allow_html=True)

    # Add the chat input
    user_input = st.text_input("Type your message", key="chat_input", placeholder="TYPE YOUR MESSAGE...", label_visibility="collapsed")
    if st.button("SEND", key="send_button"):
        if user_input:
            # Add the user's message to the chat
            st.session_state.messages = st.session_state.get('messages', []) + [
                {'role': 'user', 'content': user_input.upper()}
            ]

    st.title("Life Story Interview with DROE")
    
    # Initialize session state for interview
    if 'interview_stage' not in st.session_state:
        st.session_state.interview_stage = 0
    if 'interview_answers' not in st.session_state:
        st.session_state.interview_answers = {}
    if 'show_follow_up' not in st.session_state:
        st.session_state.show_follow_up = False
    
    try:
        # Fetch current question from backend
        response = requests.get(f"{st.session_state['backend_url']}/interview")
        if response.status_code == 200:
            data = response.json()
            
            if data.get('completed', False):
                st.markdown("""
                    <div class="card" style="text-align: center; padding: 3rem;">
                        <h2 style="color: #4a90e2;">🎉 Your Life Story is Complete!</h2>
                        <p style="font-size: 1.2rem;">Thank you for sharing your journey with DROE.</p>
                    </div>
                """, unsafe_allow_html=True)
                return
            
            question = data.get('question', '')
            current_stage = data.get('current_stage', '')
            progress = data.get('progress', 0)
            
            # Display DROE's orb and current stage
            st.markdown(f"""
                <div style="display: flex; align-items: center; margin-bottom: 2rem;">
                    <div class="droe-orb"></div>
                    <div style="margin-left: 1rem;">
                        <span style="color: #4a90e2; font-weight: 600; text-transform: capitalize;">{current_stage.replace('_', ' ')}</span>
                        <div style="color: #666;">{int(progress)}% Complete</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Display question in a styled card with typing animation
            st.markdown(f"""
                <div class="card" style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);">
                    <div class="typing-text">
                        <h3 style="color: #4a90e2; margin-top: 0;">{question}</h3>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Answer input with enhanced styling and character count
            answer = st.text_area(
                "Your answer",
                height=150,
                placeholder="Share your thoughts here...",
                key="answer_input"
            )
            
            # Character count and encouragement
            if answer:
                char_count = len(answer)
                st.markdown(f"""
                    <div style="text-align: right; color: #666; font-size: 0.9rem;">
                        {char_count} characters • Keep going!
                    </div>
                """, unsafe_allow_html=True)
            
            # Navigation buttons with enhanced styling
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Previous", key="prev_btn"):
                    st.session_state.interview_stage = max(0, st.session_state.interview_stage - 1)
                    st.rerun()
            
            with col2:
                if st.button("Next →", key="next_btn"):
                    if answer:
                        # Submit answer to backend
                        submit_response = requests.post(
                            f"{st.session_state['backend_url']}/interview",
                            json={"answer": answer}
                        )
                        
                        if submit_response.status_code == 200:
                            response_data = submit_response.json()
                            follow_up = response_data.get('follow_up', '')
                            
                            # Save answer locally
                            st.session_state.interview_answers[question] = {
                                "answer": answer,
                                "follow_up": follow_up,
                                "timestamp": datetime.now().isoformat()
                            }
                            
                            # Show success message with animation
                            st.success("✓ Answer saved!")
                            time.sleep(0.5)  # Brief pause for animation
                            
                            # Show follow-up if available
                            if follow_up:
                                st.session_state.show_follow_up = True
                                st.markdown(f"""
                                    <div class="card" style="background: linear-gradient(135deg, #f0f7ff 0%, #e6f2ff 100%);">
                                        <p style="color: #4a90e2; font-style: italic;">{follow_up}</p>
                                    </div>
                                """, unsafe_allow_html=True)
                            
                            # Clear the answer input
                            st.session_state.answer_input = ""
                            
                            # Force a rerun to get the next question
                            st.rerun()
                        else:
                            st.error("Failed to save answer. Please try again.")
                    else:
                        st.warning("Please share your thoughts before proceeding.")
            
            # Progress bar with enhanced styling
            st.markdown(f"""
                <div style="margin-top: 2rem;">
                    <div style="background: #f0f0f0; height: 8px; border-radius: 4px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #4a90e2 0%, #357abd 100%); width: {progress}%; height: 100%; transition: width 0.3s ease;"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        else:
            st.error("Failed to load interview question. Please try again later.")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the server: {str(e)}")
    
    # Display previous answers in a collapsible section
    if st.session_state.interview_answers:
        with st.expander("View Your Story So Far", expanded=False):
            for q, data in st.session_state.interview_answers.items():
                st.markdown(f"""
                    <div class="card" style="margin-bottom: 1rem;">
                        <h4 style="color: #4a90e2; margin-top: 0;">{q}</h4>
                        <p>{data['answer']}</p>
                        {f'<p style="color: #666; font-style: italic;">{data["follow_up"]}</p>' if data.get('follow_up') else ''}
                    </div>
                """, unsafe_allow_html=True)

    # Interview UI without instruction boxes
    st.markdown("""
        <div class="interview-container">
            <div class="interview-form">
                <form id="interviewForm">
                    <div class="form-group">
                        <input type="text" id="question" name="question" placeholder="Ask a question..." required>
                    </div>
                    <button type="submit" class="submit-button">Submit</button>
                </form>
            </div>
            <div class="interview-responses">
                <div id="responses"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Add JavaScript for form submission
    st.markdown("""
        <script>
        document.getElementById('interviewForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const question = document.getElementById('question').value;
            if (question.trim()) {
                // Add question to responses
                const responsesDiv = document.getElementById('responses');
                const questionElement = document.createElement('div');
                questionElement.className = 'response question';
                questionElement.textContent = question;
                responsesDiv.appendChild(questionElement);
                
                // Clear input
                document.getElementById('question').value = '';
                
                // Scroll to bottom
                responsesDiv.scrollTop = responsesDiv.scrollHeight;
            }
        });
        </script>
    """, unsafe_allow_html=True) 