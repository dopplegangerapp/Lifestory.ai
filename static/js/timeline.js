// Timeline functionality
document.addEventListener('DOMContentLoaded', function() {
    const timelineContainer = document.getElementById('timeline-container');
    const zoomInBtn = document.getElementById('zoom-in');
    const zoomOutBtn = document.getElementById('zoom-out');
    const filterSelect = document.getElementById('filter-select');
    const eventDetails = document.getElementById('event-details');
    
    let currentZoom = 1;
    let events = [];
    
    // Fetch events from the API
    async function fetchEvents() {
        try {
            const response = await fetch('/api/timeline/events');
            events = await response.json();
            renderTimeline();
        } catch (error) {
            console.error('Error fetching events:', error);
        }
    }
    
    // Render timeline markers
    function renderTimeline() {
        timelineContainer.innerHTML = '';
        const filteredEvents = filterEvents();
        
        filteredEvents.forEach(event => {
            const marker = document.createElement('div');
            marker.className = 'timeline-marker';
            marker.style.left = `${calculatePosition(event.date)}%`;
            marker.dataset.id = event.id;
            marker.dataset.type = event.type;
            
            marker.addEventListener('click', () => showEventDetails(event));
            timelineContainer.appendChild(marker);
        });
    }
    
    // Calculate position based on date
    function calculatePosition(date) {
        const eventDate = new Date(date);
        const minDate = new Date('1900-01-01');
        const maxDate = new Date('2100-12-31');
        const totalDays = (maxDate - minDate) / (1000 * 60 * 60 * 24);
        const eventDays = (eventDate - minDate) / (1000 * 60 * 60 * 24);
        return (eventDays / totalDays) * 100;
    }
    
    // Filter events based on selected type
    function filterEvents() {
        const selectedType = filterSelect.value;
        return selectedType === 'all' 
            ? events 
            : events.filter(event => event.type === selectedType);
    }
    
    // Show event details
    async function showEventDetails(event) {
        try {
            const response = await fetch(`/api/timeline/${event.type}/${event.id}`);
            const details = await response.json();
            
            eventDetails.innerHTML = `
                <h3>${details.title}</h3>
                <p>${details.description}</p>
                <p>Date: ${new Date(details.date).toLocaleDateString()}</p>
                ${details.media ? `<img src="${details.media}" alt="${details.title}">` : ''}
            `;
            eventDetails.style.display = 'block';
        } catch (error) {
            console.error('Error fetching event details:', error);
        }
    }
    
    // Handle zoom
    function handleZoom(delta) {
        currentZoom = Math.max(0.5, Math.min(2, currentZoom + delta));
        timelineContainer.style.transform = `scale(${currentZoom})`;
    }
    
    // Event listeners
    zoomInBtn.addEventListener('click', () => handleZoom(0.1));
    zoomOutBtn.addEventListener('click', () => handleZoom(-0.1));
    filterSelect.addEventListener('change', renderTimeline);
    
    // Initial load
    fetchEvents();
}); 