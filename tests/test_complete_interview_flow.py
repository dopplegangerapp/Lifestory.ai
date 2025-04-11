import pytest
import requests
import json
import time
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Constants
BASE_URL = "http://localhost:5001"
SESSION_ID = str(uuid.uuid4())

# Test answers designed to trigger different card types
TEST_ANSWERS = [
    # Place card - Birthplace
    {
        "answer": "I was born in Portland, Oregon. It's a beautiful city with lots of trees and bridges.",
        "expected_card_type": "place",
        "expected_location": "Portland, Oregon"
    },
    # Person card - Mother
    {
        "answer": "My mother was a teacher. She taught elementary school for 30 years and was very dedicated to her students.",
        "expected_card_type": "person",
        "expected_people": ["mother"]
    },
    # Event card - Graduation
    {
        "answer": "I graduated from high school in 2010. It was a big ceremony at the local stadium with all my friends and family.",
        "expected_card_type": "event",
        "expected_date": "2010"
    },
    # Memory card - Childhood memory
    {
        "answer": "One of my favorite childhood memories is when my family went camping in the mountains. We saw a bear and it was both scary and exciting.",
        "expected_card_type": "memory"
    }
]

def get_session_cookie():
    """Get the session cookie from the response."""
    try:
        response = requests.get(f"{BASE_URL}/interview", cookies={"session": SESSION_ID})
        response.raise_for_status()
        
        # Print response details for debugging
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response cookies: {response.cookies}")
        print(f"Response content: {response.text}")
        
        session_cookie = response.cookies.get("session")
        if session_cookie is None:
            print("Warning: No session cookie in response")
            # Try to get it from the response headers
            if 'Set-Cookie' in response.headers:
                print(f"Found Set-Cookie header: {response.headers['Set-Cookie']}")
                # Parse the Set-Cookie header manually if needed
        return session_cookie
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to get session cookie: {str(e)}")
        return None

def test_complete_interview_flow():
    """Test the complete interview flow including card creation and timeline."""
    # Start the interview
    session_cookie = get_session_cookie()
    assert session_cookie is not None, "Failed to get session cookie"
    
    # Track created cards
    created_cards = {
        "place": False,
        "person": False,
        "event": False,
        "memory": False
    }
    
    # Process each test answer
    for test_answer in TEST_ANSWERS:
        # Get current question
        response = requests.get(
            f"{BASE_URL}/interview",
            cookies={"session": session_cookie}
        )
        assert response.status_code == 200, "Failed to get current question"
        
        # Submit answer
        response = requests.post(
            f"{BASE_URL}/interview",
            json={"answer": test_answer["answer"]},
            cookies={"session": session_cookie}
        )
        assert response.status_code == 200, "Failed to submit answer"
        
        # Check if card was created
        response = requests.get(
            f"{BASE_URL}/cards",
            cookies={"session": session_cookie}
        )
        assert response.status_code == 200, "Failed to get cards"
        
        cards = response.json().get("cards", [])
        for card in cards:
            if card["type"] == test_answer["expected_card_type"]:
                created_cards[test_answer["expected_card_type"]] = True
                
                # Verify card specific attributes
                if test_answer["expected_card_type"] == "place":
                    assert card["location"] == test_answer["expected_location"], "Place card location mismatch"
                elif test_answer["expected_card_type"] == "person":
                    assert any(person in card["people"] for person in test_answer["expected_people"]), "Person card people mismatch"
                elif test_answer["expected_card_type"] == "event":
                    assert test_answer["expected_date"] in card["date"], "Event card date mismatch"
                
                # Verify DALL-E image was generated
                assert "image_url" in card, "Card missing image URL"
                assert card["image_url"].startswith("https://"), "Invalid image URL format"
    
    # Verify all card types were created
    for card_type, created in created_cards.items():
        assert created, f"Failed to create {card_type} card"
    
    # Verify timeline
    response = requests.get(
        f"{BASE_URL}/timeline",
        cookies={"session": session_cookie}
    )
    assert response.status_code == 200, "Failed to get timeline"
    
    timeline = response.json().get("timeline", [])
    assert len(timeline) > 0, "Timeline is empty"
    
    # Verify timeline contains both events and memories
    has_events = any(item["type"] == "event" for item in timeline)
    has_memories = any(item["type"] == "memory" for item in timeline)
    assert has_events, "Timeline missing events"
    assert has_memories, "Timeline missing memories"
    
    # Verify timeline items have required fields
    for item in timeline:
        assert "id" in item, "Timeline item missing ID"
        assert "title" in item, "Timeline item missing title"
        assert "description" in item, "Timeline item missing description"
        assert "date" in item, "Timeline item missing date"
        assert "type" in item, "Timeline item missing type"
        assert "image_url" in item, "Timeline item missing image URL"

def test_timeline_view():
    """Test that the timeline is properly viewable."""
    # Get session cookie
    session_cookie = get_session_cookie()
    assert session_cookie is not None, "Failed to get session cookie"
    
    # Get timeline
    response = requests.get(
        f"{BASE_URL}/timeline",
        cookies={"session": session_cookie}
    )
    assert response.status_code == 200, "Failed to get timeline"
    
    timeline = response.json().get("timeline", [])
    assert len(timeline) > 0, "Timeline is empty"
    
    # Verify timeline items are properly ordered by date
    dates = [datetime.fromisoformat(item["date"]) for item in timeline]
    assert dates == sorted(dates), "Timeline items are not properly ordered by date"
    
    # Verify timeline items have valid image URLs
    for item in timeline:
        image_response = requests.head(item["image_url"])
        assert image_response.status_code == 200, f"Invalid image URL: {item['image_url']}"

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 