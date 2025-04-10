// Card viewer functionality
document.addEventListener('DOMContentLoaded', function() {
    const cardGrid = document.getElementById('card-grid');
    const searchInput = document.getElementById('search-input');
    const filterSelect = document.getElementById('filter-select');
    
    let cards = [];
    
    // Fetch cards from the API
    async function fetchCards() {
        try {
            const response = await fetch('/api/cards');
            cards = await response.json();
            renderCards();
        } catch (error) {
            console.error('Error fetching cards:', error);
        }
    }
    
    // Render cards in the grid
    function renderCards() {
        cardGrid.innerHTML = '';
        const filteredCards = filterCards();
        
        filteredCards.forEach(card => {
            const cardElement = document.createElement('div');
            cardElement.className = 'card';
            cardElement.innerHTML = `
                <h3>${card.title}</h3>
                <p>${card.description}</p>
                ${card.media ? `<img src="${card.media}" alt="${card.title}">` : ''}
                <div class="card-footer">
                    <span class="card-type">${card.type}</span>
                    <span class="card-date">${new Date(card.date).toLocaleDateString()}</span>
                </div>
            `;
            
            cardElement.addEventListener('click', () => {
                window.location.href = `/cards/${card.type}/${card.id}`;
            });
            
            cardGrid.appendChild(cardElement);
        });
    }
    
    // Filter cards based on search and type
    function filterCards() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedType = filterSelect.value;
        
        return cards.filter(card => {
            const matchesSearch = card.title.toLowerCase().includes(searchTerm) ||
                                card.description.toLowerCase().includes(searchTerm);
            const matchesType = selectedType === 'all' || card.type === selectedType;
            return matchesSearch && matchesType;
        });
    }
    
    // Event listeners
    searchInput.addEventListener('input', renderCards);
    filterSelect.addEventListener('change', renderCards);
    
    // Initial load
    fetchCards();
}); 