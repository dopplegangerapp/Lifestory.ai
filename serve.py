from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Get cards data from API
    api_url = 'http://localhost:5000/api/events'
    try:
        response = requests.get(api_url)
        cards = response.json()
    except:
        cards = []
    return render_template('index.html', cards=cards)

if __name__ == '__main__':
    app.run(port=8000)  # Frontend runs on port 8000
