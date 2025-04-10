import streamlit as st

def add_custom_styles():
    st.markdown("""
        <style>
            /* Reset and Base Styles */
            body {
                margin: 0;
                padding: 0;
                background: #000;
                color: #fff;
                font-family: Arial, sans-serif;
                height: 100vh;
                overflow: hidden;
            }
            
            /* Main Container */
            .stApp {
                background: #000;
                min-height: 100vh;
                position: relative;
                padding: 0.5rem;
                margin: 0;
                display: flex;
                flex-direction: column;
                justify-content: flex-start;
                overflow-y: auto;
            }

            /* Adjust content for interview mode */
            [data-testid="stVerticalBlock"] {
                gap: 0.5rem !important;
            }

            [data-testid="stForm"] {
                padding: 0.5rem !important;
            }
            
            /* Header */
            .header {
                text-align: center;
                color: #007bff;
                font-size: 2rem;
                font-weight: bold;
                letter-spacing: 4px;
                text-transform: uppercase;
                margin: 1rem 0;
                padding: 0;
            }

            /* Content Containers */
            .stButton {
                margin: 0.5rem 0;
            }

            .element-container {
                margin: 0.5rem 0;
            }

            /* Ensure content fits screen */
            .main .block-container {
                padding: 1rem;
                max-width: 100%;
                width: 100%;
            }

            /* Interview specific styles */
            .stTextArea {
                min-height: 100px;
                margin: 1rem 0;
            }

            .stProgress {
                margin: 1rem 0;
            }

            /* Container adjustments */
            [data-testid="stVerticalBlock"] {
                gap: 0.5rem;
                padding: 0;
            }
            
            .block-container {
                padding: 0 !important;
            }

            /* Header adjustments */
            h1, h2, h3 {
                margin: 0.5rem 0;
            }

            /* Responsive text */
            @media (max-width: 768px) {
                .header {
                    font-size: 1.5rem;
                    letter-spacing: 2px;
                }
            }
            
            /* Orb */
            .droe-orb {
                width: 350px;
                height: 350px;
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: radial-gradient(circle at 30% 30%, 
                    rgba(0, 123, 255, 1),
                    rgba(0, 40, 255, 0.95));
                border-radius: 50%;
                box-shadow: 
                    0 0 100px rgba(0, 123, 255, 0.8),
                    0 0 200px rgba(0, 123, 255, 0.6),
                    0 0 300px rgba(0, 123, 255, 0.4);
                z-index: 0;
            }

            /* Button Container */
            .button-container {
                position: fixed;
                bottom: 30%;
                left: 50%;
                transform: translateX(-50%);
                width: 100%;
                max-width: 1200px;
                display: flex;
                flex-direction: column;
                gap: 20px;
                z-index: 1;
                padding: 0 20px;
            }

            /* Buttons */
            .stButton > button {
                width: 100%;
                background: rgba(0, 0, 0, 0.3);
                border: 2px solid #007bff;
                color: #fff;
                padding: 1.5rem;
                font-size: 1.5rem;
                font-weight: bold;
                letter-spacing: 4px;
                text-transform: uppercase;
                transition: all 0.3s ease;
            }
            
            .stButton > button:hover {
                background: #007bff;
                color: #000;
                transform: translateY(-4px);
            }
            
            /* Footer */
            .footer {
                position: fixed;
                bottom: 20px;
                left: 0;
                right: 0;
                text-align: center;
                padding: 10px;
                color: #fff;
                font-size: 0.8rem;
                letter-spacing: 1px;
                text-transform: uppercase;
                z-index: 2;
            }
        </style>
    """, unsafe_allow_html=True)

def add_global_styles():
    st.markdown("""
        <style>
            /* Global theme variables */
            :root {
                --primary-glow: #4a90e2;
                --secondary-glow: #2c3e50;
                --background-dark: #0a0a0a;
                --text-light: #ffffff;
                --card-bg: rgba(20, 20, 20, 0.8);
                --hover-glow: rgba(74, 144, 226, 0.3);
                --button-primary: #4a90e2;
                --button-hover: #357abd;
                --button-text: #ffffff;
                --button-shadow: rgba(74, 144, 226, 0.3);
            }
            
            /* Base styles - Mobile First */
            .stApp {
                background: var(--background-dark);
                color: var(--text-light);
                padding: 1rem;
            }
            
            /* Mobile Navigation */
            .nav-button {
                display: block;
                padding: 1rem;
                color: var(--button-text);
                text-decoration: none;
                border-radius: 8px;
                transition: all 0.3s ease;
                background: var(--button-primary);
                border: none;
                text-align: center;
                font-weight: 600;
                margin-bottom: 0.5rem;
                width: 100%;
                box-shadow: 0 4px 6px var(--button-shadow);
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .nav-button:hover {
                background: var(--button-hover);
                transform: translateX(5px);
                box-shadow: 0 6px 12px var(--button-shadow);
            }
            
            /* Mobile Cards */
            .card {
                background: var(--card-bg);
                border-radius: 12px;
                padding: 1.5rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
                margin-bottom: 1rem;
                width: 100%;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            
            .card:hover {
                transform: translateY(-5px);
                border-color: var(--primary-glow);
                box-shadow: 0 8px 15px var(--button-shadow);
            }
            
            .card-button {
                display: block;
                padding: 1rem;
                background: var(--button-primary);
                color: var(--button-text);
                text-decoration: none;
                border-radius: 8px;
                margin-top: 1rem;
                transition: all 0.3s ease;
                text-align: center;
                width: 100%;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 1px;
                box-shadow: 0 4px 6px var(--button-shadow);
            }
            
            .card-button:hover {
                background: var(--button-hover);
                transform: scale(1.02);
                box-shadow: 0 6px 12px var(--button-shadow);
            }
            
            /* Mobile Welcome Page */
            .welcome-container {
                width: 100%;
                padding: 1rem;
            }
            
            .welcome-title {
                text-align: center;
                margin-bottom: 2rem;
                color: var(--text-light);
                font-size: 2rem;
            }
            
            .feature-cards {
                display: flex;
                flex-direction: column;
                gap: 1rem;
                margin-top: 1rem;
            }
            
            /* Mobile Cards Page */
            .cards-container {
                width: 100%;
                padding: 1rem;
            }
            
            .cards-grid {
                display: grid;
                grid-template-columns: 1fr;
                gap: 1rem;
                margin-top: 1rem;
            }
            
            /* Mobile Sidebar */
            .stSidebar {
                width: 100%;
                padding: 1rem;
                background: var(--background-dark);
            }
            
            .droe-orb-container {
                display: flex;
                justify-content: center;
                margin-bottom: 1rem;
            }
            
            /* Responsive Design - Tablet */
            @media (min-width: 768px) {
                .stApp {
                    padding: 2rem;
                }
                
                .feature-cards {
                    grid-template-columns: repeat(2, 1fr);
                }
                
                .cards-grid {
                    grid-template-columns: repeat(2, 1fr);
                }
                
                .stSidebar {
                    width: 300px;
                }
            }
            
            /* Responsive Design - Desktop */
            @media (min-width: 1024px) {
                .feature-cards {
                    grid-template-columns: repeat(3, 1fr);
                }
                
                .cards-grid {
                    grid-template-columns: repeat(3, 1fr);
                }
                
                .welcome-container,
                .cards-container {
                    max-width: 1200px;
                    margin: 0 auto;
                }
            }
            
            /* Mobile Scrollbar */
            ::-webkit-scrollbar {
                width: 6px;
            }
            
            ::-webkit-scrollbar-track {
                background: var(--background-dark);
            }
            
            ::-webkit-scrollbar-thumb {
                background: var(--primary-glow);
                border-radius: 3px;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: var(--secondary-glow);
            }
            
            /* Mobile Touch Targets */
            button, a, input, textarea {
                min-height: 44px;
                min-width: 44px;
            }
            
            /* Mobile Typography */
            h1 { font-size: 2rem; }
            h2 { font-size: 1.75rem; }
            h3 { font-size: 1.5rem; }
            p { font-size: 1rem; }
            
            /* Mobile Spacing */
            .spacing-sm { margin: 0.5rem 0; }
            .spacing-md { margin: 1rem 0; }
            .spacing-lg { margin: 2rem 0; }
        </style>
    """, unsafe_allow_html=True)

def add_droe_orb_styles():
    st.markdown("""
        <style>
        /* Main Container */
        .main-container {
            position: relative;
            width: 100%;
            height: 100vh;
            background: #000;
            overflow: hidden;
        }

        /* Header */
        .header {
            position: fixed;
            top: 2rem;
            left: 0;
            right: 0;
            text-align: center;
            color: var(--glow-blue);
            font-size: 3rem;
            font-weight: bold;
            letter-spacing: 6px;
            text-transform: uppercase;
            text-shadow: 0 0 30px var(--button-glow);
            z-index: 2;
        }

        /* DROE Orb */
        .droe-orb {
            width: 600px;
            height: 600px;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: radial-gradient(circle at 30% 30%, 
                rgba(0, 123, 255, 1),
                rgba(0, 40, 255, 0.95));
            border-radius: 50%;
            animation: pulse 3s infinite ease-in-out;
            box-shadow: 
                0 0 200px rgba(0, 123, 255, 0.8),
                0 0 400px rgba(0, 123, 255, 0.6),
                0 0 600px rgba(0, 123, 255, 0.4),
                inset 0 0 200px rgba(255, 255, 255, 0.3);
            z-index: 0;
            pointer-events: none;
        }

        /* Button Container */
        .button-container {
            position: fixed;
            bottom: 5vh;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 600px;
            display: flex;
            flex-direction: column;
            gap: 2rem;
            z-index: 1;
            padding: 2rem;
        }

        /* Button Styles */
        .stButton > button {
            width: 100%;
            background: rgba(0, 0, 0, 0.3);
            border: 2px solid var(--glow-blue);
            color: var(--text-color);
            padding: 1.5rem;
            font-size: 1.5rem;
            font-weight: bold;
            letter-spacing: 4px;
            text-transform: uppercase;
            transition: all 0.3s ease;
            margin: 0;
            box-shadow: 0 0 40px var(--button-glow);
            backdrop-filter: blur(5px);
        }

        .stButton > button:hover {
            background: var(--glow-blue);
            color: black;
            transform: translateY(-4px);
            box-shadow: 0 0 60px var(--button-glow);
        }

        /* Footer */
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            text-align: center;
            padding: 1rem;
            color: var(--text-color);
            font-size: 0.9rem;
            letter-spacing: 2px;
            text-transform: uppercase;
            background: rgba(0, 0, 0, 0.8);
            border-top: 1px solid var(--glow-blue);
            box-shadow: 0 0 20px var(--button-glow);
            z-index: 2;
        }
        </style>
    """, unsafe_allow_html=True)

def create_droe_orb():
    st.markdown("""
        <div class="droe-orb-container">
            <div class="droe-orb-glow"></div>
            <div class="droe-orb"></div>
            <div class="droe-orb-label">DROE</div>
        </div>
    """, unsafe_allow_html=True)

def add_typing_animation():
    st.markdown("""
        <style>
            .typing-text {
                display: inline-block;
                overflow: hidden;
                border-right: 2px solid var(--primary-glow);
                white-space: nowrap;
                animation: typing 3.5s steps(40, end),
                           blink-caret 0.75s step-end infinite;
            }

            @keyframes typing {
                from { width: 0 }
                to { width: 100% }
            }

            @keyframes blink-caret {
                from, to { border-color: transparent }
                50% { border-color: var(--primary-glow) }
            }
        </style>
    """, unsafe_allow_html=True) 