# DROE Core App

A Digital Record of Existence (DROE) application for tracking people, places, events, and emotions in your life.

## Features

- **People Management**: Track information about people in your life, including relationships and descriptions.
- **Place Tracking**: Record and manage locations that are significant to you.
- **Event Logging**: Document events with details about who was involved and where they occurred.
- **Emotion Recording**: Track emotions associated with your memories and experiences.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/droe-core.git
   cd droe-core
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```
   python init_db.py
   ```

5. Run the application:
   ```
   python app.py
   ```

6. Open your browser and navigate to `http://127.0.0.1:5000/`

## Project Structure

- `app.py`: Main Flask application file
- `routes/`: Contains route handlers for different parts of the application
- `db/`: Database models and connection handling
- `templates/`: HTML templates for the application
- `static/`: Static files (CSS, JavaScript, images)

## Technologies Used

- Flask: Web framework
- SQLAlchemy: Database ORM
- Jinja2: Template engine
- HTML/CSS/JavaScript: Frontend technologies

## License

This project is licensed under the MIT License - see the LICENSE file for details. 