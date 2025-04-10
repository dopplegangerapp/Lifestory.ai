// Shared JavaScript functionality for DROE Core App

// Handle navigation active state
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// Handle search functionality
function setupSearch(inputId, containerId) {
    const searchInput = document.getElementById(inputId);
    const container = document.getElementById(containerId);
    
    if (searchInput && container) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const items = container.querySelectorAll('.card');
            
            items.forEach(item => {
                const text = item.textContent.toLowerCase();
                item.style.display = text.includes(searchTerm) ? 'block' : 'none';
            });
        });
    }
}

// Handle card expansion
function setupCardExpansion() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        card.addEventListener('click', function() {
            this.classList.toggle('expanded');
        });
    });
}

// Initialize shared functionality
document.addEventListener('DOMContentLoaded', function() {
    setupCardExpansion();
}); 