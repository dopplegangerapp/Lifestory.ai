import streamlit as st

def create_animated_ui():
    """Create the main animated UI for the home page."""
    st.title("Welcome to Lifestory.ai")
    
    # Hero section
    st.markdown("""
        <div style='text-align: center; margin: 2rem 0;'>
            <h2 style='color: #4a90e2;'>Your Personal Life Story Assistant</h2>
            <p style='font-size: 1.2rem;'>Capture, organize, and cherish your life's moments with DROE</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Features grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style='text-align: center; padding: 1rem;'>
                <h3>📝 Interviews</h3>
                <p>Guided conversations to capture your stories</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 1rem;'>
                <h3>📅 Timeline</h3>
                <p>Visualize your life's journey</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style='text-align: center; padding: 1rem;'>
                <h3>🎴 Cards</h3>
                <p>Organize your memories and events</p>
            </div>
        """, unsafe_allow_html=True)
    
    # Call to action
    st.markdown("""
        <div style='text-align: center; margin: 2rem 0;'>
            <h3>Ready to start your journey?</h3>
            <p>Select an option from the sidebar to begin</p>
        </div>
    """, unsafe_allow_html=True) 