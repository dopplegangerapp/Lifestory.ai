import streamlit as st

def create_knowledge_sidebar():
    st.markdown("""
        <style>
            .knowledge-section {
                background: rgba(20, 20, 40, 0.8);
                border-radius: 12px;
                padding: 1rem;
                margin: 1rem 0;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            
            .knowledge-section h3 {
                color: var(--primary-glow);
                margin-top: 0;
            }
            
            .assistant-message {
                background: rgba(74, 144, 226, 0.1);
                border-radius: 8px;
                padding: 0.8rem;
                margin: 0.5rem 0;
                border-left: 3px solid var(--primary-glow);
            }
            
            .assistant-message p {
                margin: 0;
                font-size: 0.9rem;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Onboarding section
    with st.expander("📚 Getting Started", expanded=True):
        st.markdown("""
            <div class="knowledge-section">
                <h3>Welcome to Lifestory.ai</h3>
                <p>Here's how to get started:</p>
                <ol>
                    <li>Begin with the Interview to share your memories</li>
                    <li>View your timeline to see your life events</li>
                    <li>Explore your memory cards</li>
                </ol>
            </div>
        """, unsafe_allow_html=True)
    
    # DROE Assistant section
    with st.expander("🧠 DROE Assistant", expanded=True):
        st.markdown("""
            <div class="knowledge-section">
                <h3>Memory Assistant</h3>
                <div class="assistant-message">
                    <p>I'm here to help you organize and explore your memories. Ask me anything!</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Simulated DROE responses
        if st.button("Ask DROE a question"):
            st.markdown("""
                <div class="assistant-message">
                    <p class="typing-text">I'm analyzing your memories to provide personalized insights...</p>
                </div>
            """, unsafe_allow_html=True)
    
    # Tips section
    with st.expander("💡 Tips & Tricks", expanded=True):
        st.markdown("""
            <div class="knowledge-section">
                <h3>Pro Tips</h3>
                <ul>
                    <li>Use specific dates for better timeline organization</li>
                    <li>Add emotions to your memories for richer context</li>
                    <li>Tag people and places to create connections</li>
                </ul>
            </div>
        """, unsafe_allow_html=True) 