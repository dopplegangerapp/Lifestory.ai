import streamlit as st

def create_droe_orb():
    """Create DROE's animated orb representation."""
    st.markdown("""
        <style>
        @keyframes orb-pulse {
            0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(74, 144, 226, 0.7); }
            50% { transform: scale(1.1); box-shadow: 0 0 30px 15px rgba(74, 144, 226, 0.4); }
            100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(74, 144, 226, 0.7); }
        }
        
        @keyframes orb-float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
        
        .droe-orb {
            width: 100px;
            height: 100px;
            background: radial-gradient(circle at 30% 30%, #4a90e2, #357abd);
            border-radius: 50%;
            position: relative;
            animation: orb-pulse 2s infinite, orb-float 3s ease-in-out infinite;
            box-shadow: 0 0 20px rgba(74, 144, 226, 0.5);
            margin: 20px auto;
        }
        
        .droe-orb::before {
            content: '';
            position: absolute;
            width: 30%;
            height: 30%;
            background: rgba(255, 255, 255, 0.8);
            border-radius: 50%;
            top: 20%;
            left: 20%;
            filter: blur(2px);
        }
        
        .droe-orb::after {
            content: 'DROE';
            position: absolute;
            bottom: -30px;
            left: 50%;
            transform: translateX(-50%);
            color: #4a90e2;
            font-weight: bold;
            font-size: 1.2em;
            text-shadow: 0 0 10px rgba(74, 144, 226, 0.5);
        }
        
        .droe-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        </style>
        
        <div class="droe-container">
            <div class="droe-orb"></div>
        </div>
    """, unsafe_allow_html=True) 