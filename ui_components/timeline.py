import streamlit as st
import requests
from datetime import datetime
import json

def create_timeline_ui():
    """Create the timeline UI component."""
    st.title("Your Life Timeline")
    
    # Initialize session state for timeline
    if 'timeline_events' not in st.session_state:
        st.session_state.timeline_events = []
    
    # Check if backend URL is initialized
    if 'backend_url' not in st.session_state:
        st.error("Backend server not initialized. Please restart the application.")
        return

    try:
        # Fetch events from backend
        response = requests.get(f"{st.session_state['backend_url']}/timeline")
        if response.status_code == 200:
            events = response.json().get('events', [])
            
            # Display timeline
            for event in events:
                date = datetime.fromisoformat(event['date']).strftime('%B %d, %Y')
                st.markdown(f"""
                    <div style='background-color: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 4px solid #4a90e2;'>
                        <h3 style='color: #4a90e2; margin-top: 0;'>{event['title']}</h3>
                        <p style='color: #666;'>{date}</p>
                        <p>{event['description']}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        else:
            st.error("Failed to load timeline events. Please try again later.")
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the server: {str(e)}")
    
    # Add new event button
    if st.button("Add New Event", key="add_event"):
        st.session_state.show_event_form = True
    
    # Event form
    if st.session_state.get('show_event_form', False):
        with st.form("event_form"):
            title = st.text_input("Event Title")
            date = st.date_input("Date")
            description = st.text_area("Description")
            
            if st.form_submit_button("Save Event"):
                try:
                    # Submit event to backend
                    response = requests.post(
                        f"{st.session_state['backend_url']}/timeline",
                        json={
                            "title": title,
                            "date": date.isoformat(),
                            "description": description
                        }
                    )
                    
                    if response.status_code == 200:
                        st.success("Event added successfully!")
                        st.session_state.show_event_form = False
                        st.experimental_rerun()
                    else:
                        st.error("Failed to add event. Please try again.")
                
                except requests.exceptions.RequestException as e:
                    st.error(f"Error connecting to the server: {str(e)}")

    st.markdown("""
        <style>
            .timeline-container {
                position: relative;
                padding: 2rem;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .timeline-nav {
                position: sticky;
                top: 0;
                background: rgba(20, 20, 40, 0.95);
                padding: 1rem;
                z-index: 100;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
            }
            
            .timeline-filters {
                display: flex;
                gap: 1rem;
                margin-bottom: 1rem;
            }
            
            .timeline-filters button {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 20px;
                color: var(--text-primary);
                cursor: pointer;
                transition: all 0.3s ease;
            }
            
            .timeline-filters button:hover {
                background: var(--primary-glow);
                transform: translateY(-2px);
            }
            
            .timeline-filters button.active {
                background: var(--primary-glow);
            }
            
            .timeline-years {
                display: flex;
                gap: 1rem;
                overflow-x: auto;
                padding: 1rem 0;
                scrollbar-width: none;
            }
            
            .timeline-years::-webkit-scrollbar {
                display: none;
            }
            
            .year-pill {
                background: rgba(255, 255, 255, 0.1);
                padding: 0.5rem 1rem;
                border-radius: 20px;
                cursor: pointer;
                transition: all 0.3s ease;
                white-space: nowrap;
            }
            
            .year-pill:hover {
                background: var(--primary-glow);
                transform: translateY(-2px);
            }
            
            .year-pill.active {
                background: var(--primary-glow);
            }
            
            .timeline-content {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 2rem;
                padding: 2rem 0;
            }
            
            .life-period {
                background: rgba(20, 20, 40, 0.8);
                border-radius: 12px;
                padding: 1.5rem;
                border: 1px solid rgba(255, 255, 255, 0.1);
                transition: all 0.3s ease;
            }
            
            .life-period:hover {
                transform: translateY(-5px);
                box-shadow: 0 8px 30px rgba(74, 144, 226, 0.3);
            }
            
            .period-header {
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 1rem;
            }
            
            .period-icon {
                width: 40px;
                height: 40px;
                background: var(--primary-glow);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.2rem;
            }
            
            .period-title {
                font-size: 1.2rem;
                font-weight: 600;
                margin: 0;
            }
            
            .period-dates {
                color: var(--text-secondary);
                font-size: 0.9rem;
            }
            
            .period-events {
                display: flex;
                flex-direction: column;
                gap: 1rem;
            }
            
            .event-card {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                padding: 1rem;
                border-left: 3px solid var(--primary-glow);
                transition: all 0.3s ease;
            }
            
            .event-card:hover {
                transform: translateX(5px);
                background: rgba(255, 255, 255, 0.1);
            }
            
            .event-date {
                color: var(--primary-glow);
                font-size: 0.8rem;
                margin-bottom: 0.5rem;
            }
            
            .event-title {
                font-size: 1rem;
                margin-bottom: 0.5rem;
            }
            
            .event-description {
                color: var(--text-secondary);
                font-size: 0.9rem;
            }
            
            .event-tags {
                display: flex;
                gap: 0.5rem;
                margin-top: 0.5rem;
                flex-wrap: wrap;
            }
            
            .event-tag {
                background: rgba(74, 144, 226, 0.2);
                padding: 0.2rem 0.5rem;
                border-radius: 12px;
                font-size: 0.8rem;
                color: var(--primary-glow);
            }
            
            .timeline-search {
                margin-bottom: 1rem;
            }
            
            .timeline-search input {
                width: 100%;
                padding: 0.8rem;
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: var(--text-primary);
            }
            
            .timeline-search input:focus {
                outline: none;
                border-color: var(--primary-glow);
                box-shadow: 0 0 10px rgba(74, 144, 226, 0.3);
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Timeline Navigation
    st.markdown("""
        <div class="timeline-nav">
            <div class="timeline-filters">
                <button class="active">All</button>
                <button>Events</button>
                <button>Memories</button>
                <button>People</button>
                <button>Places</button>
            </div>
            <div class="timeline-search">
                <input type="text" placeholder="Search your life story...">
            </div>
            <div class="timeline-years">
                <div class="year-pill">2020</div>
                <div class="year-pill">2021</div>
                <div class="year-pill active">2022</div>
                <div class="year-pill">2023</div>
                <div class="year-pill">2024</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Timeline Content
    st.markdown("""
        <div class="timeline-content">
            <!-- Childhood Period -->
            <div class="life-period">
                <div class="period-header">
                    <div class="period-icon">👶</div>
                    <div>
                        <h3 class="period-title">Childhood</h3>
                        <div class="period-dates">1990 - 2000</div>
                    </div>
                </div>
                <div class="period-events">
                    <div class="event-card">
                        <div class="event-date">1995</div>
                        <div class="event-title">First Day of School</div>
                        <div class="event-description">Started kindergarten at Sunshine Elementary</div>
                        <div class="event-tags">
                            <span class="event-tag">Education</span>
                            <span class="event-tag">Family</span>
                        </div>
                    </div>
                    <div class="event-card">
                        <div class="event-date">1998</div>
                        <div class="event-title">Family Vacation</div>
                        <div class="event-description">Trip to Disney World with parents and siblings</div>
                        <div class="event-tags">
                            <span class="event-tag">Travel</span>
                            <span class="event-tag">Family</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Teenage Years -->
            <div class="life-period">
                <div class="period-header">
                    <div class="period-icon">🎓</div>
                    <div>
                        <h3 class="period-title">Teenage Years</h3>
                        <div class="period-dates">2001 - 2010</div>
                    </div>
                </div>
                <div class="period-events">
                    <div class="event-card">
                        <div class="event-date">2005</div>
                        <div class="event-title">High School Graduation</div>
                        <div class="event-description">Graduated with honors from Central High School</div>
                        <div class="event-tags">
                            <span class="event-tag">Education</span>
                            <span class="event-tag">Achievement</span>
                        </div>
                    </div>
                    <div class="event-card">
                        <div class="event-date">2006</div>
                        <div class="event-title">First Job</div>
                        <div class="event-description">Started working at the local library</div>
                        <div class="event-tags">
                            <span class="event-tag">Work</span>
                            <span class="event-tag">Growth</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Adulthood -->
            <div class="life-period">
                <div class="period-header">
                    <div class="period-icon">💼</div>
                    <div>
                        <h3 class="period-title">Adulthood</h3>
                        <div class="period-dates">2011 - Present</div>
                    </div>
                </div>
                <div class="period-events">
                    <div class="event-card">
                        <div class="event-date">2015</div>
                        <div class="event-title">College Graduation</div>
                        <div class="event-description">Earned Bachelor's degree in Computer Science</div>
                        <div class="event-tags">
                            <span class="event-tag">Education</span>
                            <span class="event-tag">Career</span>
                        </div>
                    </div>
                    <div class="event-card">
                        <div class="event-date">2018</div>
                        <div class="event-title">First Home</div>
                        <div class="event-description">Purchased first apartment in the city</div>
                        <div class="event-tags">
                            <span class="event-tag">Home</span>
                            <span class="event-tag">Milestone</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Add JavaScript for interactivity
    st.markdown("""
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                // Year navigation
                const yearPills = document.querySelectorAll('.year-pill');
                yearPills.forEach(pill => {
                    pill.addEventListener('click', () => {
                        yearPills.forEach(p => p.classList.remove('active'));
                        pill.classList.add('active');
                    });
                });
                
                // Filter buttons
                const filterButtons = document.querySelectorAll('.timeline-filters button');
                filterButtons.forEach(button => {
                    button.addEventListener('click', () => {
                        filterButtons.forEach(b => b.classList.remove('active'));
                        button.classList.add('active');
                    });
                });
                
                // Search functionality
                const searchInput = document.querySelector('.timeline-search input');
                searchInput.addEventListener('input', (e) => {
                    const searchTerm = e.target.value.toLowerCase();
                    const events = document.querySelectorAll('.event-card');
                    
                    events.forEach(event => {
                        const text = event.textContent.toLowerCase();
                        if (text.includes(searchTerm)) {
                            event.style.display = 'block';
                        } else {
                            event.style.display = 'none';
                        }
                    });
                });
            });
        </script>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="timeline-container">
            <div class="year-orb" style="background: radial-gradient(circle at 30% 30%, #6c5ce7, rgba(108, 92, 231, 0.6));">
                1984
            </div>
            <div class="timeline-line"></div>
            <div class="year-orb" style="background: radial-gradient(circle at 30% 30%, #4aedc4, rgba(74, 237, 196, 0.6));">
                1985
            </div>
            <div class="timeline-line"></div>
            <div class="year-orb" style="background: radial-gradient(circle at 30% 30%, #6c5ce7, rgba(108, 92, 231, 0.6));">
                1986
            </div>
            <div class="timeline-line"></div>
            <div class="year-orb" style="background: radial-gradient(circle at 30% 30%, #4a90e2, rgba(74, 144, 226, 0.6));">
                1987
            </div>
            <div class="timeline-line"></div>
            <div class="year-orb" style="background: radial-gradient(circle at 30% 30%, #4aedc4, rgba(74, 237, 196, 0.6));">
                1988
            </div>
        </div>

        <div class="year-detail">
            <div class="section-title">EVENTS</div>
            <div class="button-grid">
                <button class="detail-button">BIRTH</button>
                <button class="detail-button">FIRST STEP</button>
            </div>

            <div class="section-title">MEMORIES</div>
            <div class="button-grid">
                <button class="detail-button">IN THE CRIB</button>
                <button class="detail-button">PICK ME UP</button>
                <button class="detail-button">FIGHTING</button>
            </div>

            <div class="section-title">PLACES</div>
            <div class="button-grid">
                <button class="detail-button">OHSU</button>
                <button class="detail-button">HOME</button>
            </div>

            <div class="section-title">PEOPLE</div>
            <div class="people-section">
                <div class="person-avatar"></div>
                <div class="person-avatar"></div>
                <div class="person-avatar"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Add click handlers for the year orbs
    if 'selected_year' not in st.session_state:
        st.session_state.selected_year = 1984

    # Handle year selection
    selected_year = st.session_state.selected_year 