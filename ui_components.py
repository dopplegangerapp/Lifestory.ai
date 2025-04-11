import streamlit as st
import numpy as np
from typing import Optional, List, Dict, Any
import json
from datetime import datetime
import random
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import pandas as pd

# Custom CSS for animations and effects
st.markdown("""
<style>
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(255, 255, 255, 0.5); }
        50% { box-shadow: 0 0 20px rgba(255, 255, 255, 0.8); }
        100% { box-shadow: 0 0 5px rgba(255, 255, 255, 0.5); }
    }
    
    @keyframes vibrate {
        0% { transform: translate(0); }
        20% { transform: translate(-2px, 2px); }
        40% { transform: translate(-2px, -2px); }
        60% { transform: translate(2px, 2px); }
        80% { transform: translate(2px, -2px); }
        100% { transform: translate(0); }
    }
    
    .glowing-card {
        animation: glow 2s infinite;
        transition: all 0.3s ease;
    }
    
    .glowing-card:hover {
        transform: scale(1.02);
        animation: glow 1s infinite;
    }
    
    .vibrating-button {
        transition: all 0.3s ease;
    }
    
    .vibrating-button:active {
        animation: vibrate 0.3s linear;
    }
    
    .smooth-transition {
        transition: all 0.5s ease;
    }
    
    .card-container {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
        padding: 20px;
    }
    
    .card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        width: 300px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .card-title {
        font-size: 1.5em;
        margin-bottom: 10px;
        color: #fff;
    }
    
    .card-content {
        color: rgba(255, 255, 255, 0.8);
    }
    
    .floating {
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
        100% { transform: translateY(0px); }
    }
</style>
""", unsafe_allow_html=True)

class AnimatedCard:
    def __init__(self, title: str, content: str, animation_type: str = "glow"):
        self.title = title
        self.content = content
        self.animation_type = animation_type
        
    def render(self):
        st.markdown(f"""
        <div class="card {self.animation_type}-card floating">
            <div class="card-title">{self.title}</div>
            <div class="card-content">{self.content}</div>
        </div>
        """, unsafe_allow_html=True)

class AnimatedButton:
    def __init__(self, text: str, callback: callable, color: str = "#4CAF50"):
        self.text = text
        self.callback = callback
        self.color = color
        
    def render(self):
        if st.button(self.text, key=f"btn_{random.randint(0, 1000)}"):
            self.callback()
            st.markdown(f"""
            <style>
                .stButton > button {{
                    background-color: {self.color};
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }}
                .stButton > button:hover {{
                    transform: scale(1.05);
                    box-shadow: 0 0 15px {self.color};
                }}
            </style>
            """, unsafe_allow_html=True)

class CardGrid:
    def __init__(self, cards: List[AnimatedCard]):
        self.cards = cards
        
    def render(self):
        st.markdown('<div class="card-container">', unsafe_allow_html=True)
        for card in self.cards:
            card.render()
        st.markdown('</div>', unsafe_allow_html=True)

def create_animated_ui():
    # Create a sidebar for navigation
    st.sidebar.title("DROE Core App")
    page = st.sidebar.radio(
        "Navigation",
        ["Dashboard", "Cards", "Timeline", "Analytics"]
    )
    
    # Main content area
    st.title("DROE Core Dashboard")
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Cards":
        show_cards()
    elif page == "Timeline":
        show_timeline()
    elif page == "Analytics":
        show_analytics()

def show_dashboard():
    # Create animated metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Cards", "0", "0%")
    with col2:
        st.metric("Active Memories", "0", "0%")
    with col3:
        st.metric("Events Today", "0", "0%")
    
    # Create animated chart
    st.subheader("Recent Activity")
    chart_data = np.random.randn(20, 3)
    chart = st.line_chart(chart_data)
    
    # Add some placeholder content
    st.info("Welcome to DROE Core! Start by creating your first card.")

def show_cards():
    # Card creation form
    with st.expander("Create New Card", expanded=True):
        card_type = st.selectbox(
            "Select Card Type",
            ["Event", "Memory", "Person", "Place", "Time Period"]
        )
        
        if card_type:
            title = st.text_input("Enter Card Title")
            description = st.text_area("Enter Card Description")
            
            if st.button("Create Card"):
                st.success(f"Created {card_type} card: {title}")
    
    # Card grid view
    st.subheader("Your Cards")
    cols = st.columns(3)
    for i in range(3):
        with cols[i]:
            st.info("Sample Card")
            st.write("This is a sample card description.")

def show_timeline():
    # Create an animated timeline
    st.subheader("Life Timeline")
    
    # Create sample timeline data
    timeline_data = [
        {"date": "2024-01-01", "event": "New Year", "type": "event"},
        {"date": "2024-02-14", "event": "Valentine's Day", "type": "memory"},
        {"date": "2024-03-21", "event": "Spring Equinox", "type": "event"}
    ]
    
    # Create timeline visualization
    fig = go.Figure()
    
    for i, item in enumerate(timeline_data):
        fig.add_trace(go.Scatter(
            x=[item["date"]],
            y=[i],
            mode="markers+text",
            marker=dict(size=20),
            text=item["event"],
            textposition="top center"
        ))
    
    fig.update_layout(
        showlegend=False,
        height=400,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_analytics():
    # Create animated analytics dashboard
    st.subheader("Life Analytics")
    
    # Create sample data
    dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")
    values = np.random.randn(len(dates))
    
    # Create animated line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode="lines",
        name="Activity"
    ))
    
    fig.update_layout(
        title="Yearly Activity",
        xaxis_title="Date",
        yaxis_title="Activity Level",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add some statistics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Average Activity", "0.5", "0.1")
    with col2:
        st.metric("Peak Activity", "1.2", "0.3")

if __name__ == "__main__":
    create_animated_ui() 