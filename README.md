# Lifestory.AI

A digital platform for preserving and sharing life stories through AI-powered interviews and interactive storytelling.

## Current Status

### Phase 1: Core Infrastructure (In Progress)
- ✅ Basic card system implementation
- ✅ Storage manager implementation
- ✅ API endpoints setup
- ✅ Basic web interface
- 🔄 Testing and bug fixes

### Known Issues
1. PersonCard name attribute initialization
2. EventCard emotions attribute handling
3. Card type registration for PlaceCard and MemoryCard
4. Image generation API billing limit reached

### Test Status

#### Integration Tests (`test_integration.py`)
- ✅ Person card creation and storage
- ✅ Event card creation and storage
- ✅ Place card creation and storage
- ✅ Memory card creation and storage
- ✅ Time period card creation and storage
- ✅ Card deletion
- ✅ Card listing
- ✅ Card type registration

#### API Tests (`test_api.py`)
- ✅ Person creation endpoint
- ✅ Event creation endpoint
- ✅ Person retrieval endpoint
- ✅ Event retrieval endpoint
- ✅ Person update endpoint
- ✅ Person deletion endpoint
- ✅ Person listing endpoint

### Remaining Phases

#### Phase 2: Interview System
- [ ] Interview question generation
- [ ] Interview session management
- [ ] Response processing
- [ ] Card generation from responses

#### Phase 3: Media Integration
- [ ] Image generation integration
- [ ] Audio recording support
- [ ] Video recording support
- [ ] Media storage and retrieval

#### Phase 4: Story Generation
- [ ] Narrative generation from cards
- [ ] Timeline visualization
- [ ] Story export options
- [ ] Interactive story exploration

#### Phase 5: User Experience
- [ ] User authentication
- [ ] Profile management
- [ ] Sharing and collaboration
- [ ] Mobile responsiveness

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Lifestory.AI.git
cd Lifestory.AI
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
# Run the API server
python api.py

# Run the web interface
streamlit run app.py
```

## Development

### Running Tests
```bash
python run_tests.py
```

### Project Structure
```
Lifestoryai/
├── api.py              # API server
├── app.py              # Streamlit web interface
├── cards/              # Card system implementation
├── storage/            # Storage manager
├── tests/              # Test suite
├── utils/              # Utility functions
└── requirements.txt    # Project dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.