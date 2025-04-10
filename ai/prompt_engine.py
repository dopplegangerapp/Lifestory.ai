from typing import Dict, List, Any
import openai
from .assistant import Assistant
from .image_generator import ImageGenerator

class PromptEngine:
    """Engine for generating and managing AI prompts for the DROE Core system."""
    
    def __init__(self):
        """Initialize the prompt engine with assistant and image generator."""
        self.assistant = Assistant()
        self.image_generator = ImageGenerator()

    def generate_interview_question(self, context: Dict[str, Any]) -> str:
        """
        Generate the next interview question based on context.
        
        Args:
            context (dict): Current interview context including previous answers
            
        Returns:
            str: Generated question
        """
        return self.assistant.generate_follow_up(context)
    
    def analyze_response(self, response: str) -> Dict[str, Any]:
        """
        Analyze a user's response to extract key information.
        
        Args:
            response (str): User's response text
            
        Returns:
            dict: Extracted information and analysis
        """
        analysis = self.assistant.analyze_text(response)
        return {
            'key_points': analysis['key_points'],
            'emotions': analysis['emotions'],
            'suggested_follow_up': self.generate_follow_up_question(response, '')
        }
    
    def generate_card_content(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate structured content for a card based on raw data.
        
        Args:
            data (dict): Raw data to process
            
        Returns:
            dict: Structured card content
        """
        analysis = self.assistant.analyze_text(data.get('description', ''))
        image_url = None
        if data.get('type') == 'memory':
            image_url = self.image_generator.generate_memory_image(data['description'])
        elif data.get('type') == 'emotion':
            image_url = self.image_generator.generate_emotion_image(
                data.get('emotion', ''),
                data.get('intensity', 'medium')
            )
        
        return {
            'title': data.get('title', ''),
            'description': data.get('description', ''),
            'metadata': {
                'emotions': analysis['emotions'],
                'key_points': analysis['key_points'],
                'image_url': image_url
            }
        }

    def analyze_story_arcs(self, text: str) -> list[str]:
        """
        Analyze text for story arcs using the assistant.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            list[str]: Detected story arcs
        """
        analysis = self.assistant.analyze_text(text)
        return analysis['story_arcs']

    def generate_follow_up_question(self, answer: str, current_stage: str) -> str:
        """
        Generate a follow-up question based on the answer and current stage.
        
        Args:
            answer (str): User's answer
            current_stage (str): Current interview stage
            
        Returns:
            str: Generated follow-up question
        """
        context = {
            'answer': answer,
            'stage': current_stage
        }
        return self.assistant.generate_follow_up(context)
