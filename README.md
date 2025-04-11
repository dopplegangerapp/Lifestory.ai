
# Lifestory.ai - Digital Record of Existence (DROE)

A modern web application for capturing, organizing, and exploring your life's memories through AI-assisted interviews, timelines, and memory cards.

## Current Tech Stack

### Backend
- Python 3.12
- Flask (Web framework)
- SQLAlchemy (ORM)
- SQLite (Database)

### Frontend
- Streamlit (UI Framework)
- Custom CSS/JavaScript
- Plotly (Data visualization)

### AI/ML Integration
- Whisper (Audio transcription) - In Progress
- Custom Prompt Engine
- Image Generation Capabilities

## Projected Tech Stack (After Completion)

### Additional Features
- OpenAI GPT Integration
- Advanced Image Recognition
- Natural Language Processing
- Real-time Audio Processing
- Advanced Timeline Visualization
- Memory Graph Database

## Current Phase: Alpha Development

### Completed Features
- Basic UI Framework
- Interview Component
- Timeline View
- Card System Architecture
- Basic Testing Framework
- Media Upload Functionality

### In Progress
- Frontend Interview Testing
- AI Integration
- Advanced Timeline Features
- Media Processing Pipeline

## Current Issues

1. Frontend Testing
   - Interview component tests failing
   - Session state management needs improvement
   - Mock integration required for AI components

2. Backend Integration
   - API endpoint stabilization needed
   - Database optimization required
   - Error handling improvements needed

3. UI/UX
   - Mobile responsiveness improvements needed
   - Timeline performance optimization
   - Card view refinements

## Roadmap

### Phase 1 (Current)
- [x] Basic Framework Setup
- [x] Core UI Components
- [ ] Complete Test Coverage
- [ ] Basic AI Integration

### Phase 2
- [ ] Advanced AI Features
- [ ] Enhanced Timeline
- [ ] Memory Graph
- [ ] Mobile App Development

### Phase 3
- [ ] Social Features
- [ ] Advanced Analytics
- [ ] API Platform
- [ ] Enterprise Features

## Development Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the application:
```bash
python main.py
```

## Testing

Run tests using:
```bash
python -m pytest
```

## Project Structure

```
├── ai/                 # AI/ML components
├── cards/             # Card system modules
├── db/                # Database models and utilities
├── routes/            # API routes and handlers
├── ui_components/     # Streamlit UI components
├── utils/             # Helper utilities
└── tests/             # Test suites
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - See LICENSE file for details

## Authors

ReaL KeeD - Project Lead
