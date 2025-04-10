from openai import OpenAI
import os
from typing import Optional, Tuple
from datetime import datetime
import uuid

class ImageGenerationError(Exception):
    """Custom exception for image generation errors."""
    pass

class ImageGenerator:
    """Handles image generation using OpenAI's DALL-E."""
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)

    def generate_image(self, prompt: str) -> Tuple[str, Optional[str]]:
        """
        Generate an image based on the given prompt.
        
        Args:
            prompt (str): The prompt to generate an image from
            
        Returns:
            Tuple[str, Optional[str]]: A tuple containing the image URL and any error message
        """
        if not prompt:
            return "", "No prompt provided"
            
        try:
            # Modify prompt to ensure silhouette/clip art style
            style_prompt = f"Create a simple silhouette or clip art style image of {prompt}. Use only black and white colors, minimal details, and abstract shapes. No realistic features or details."
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=style_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            if not response.data:
                return "", "No image was generated"
                
            return response.data[0].url, None
            
        except Exception as e:
            error_msg = f"Error generating image: {str(e)}"
            print(error_msg)
            return "", error_msg

    def generate_memory_image(self, memory_text: str) -> Tuple[str, Optional[str]]:
        """
        Generate an image based on a memory description.
        
        Args:
            memory_text (str): Description of the memory
            
        Returns:
            Tuple[str, Optional[str]]: A tuple containing the image URL and any error message
        """
        if not memory_text:
            return "", "No memory text provided"
            
        # Modify prompt to ensure silhouette/clip art style for memories
        prompt = f"Create a simple silhouette or clip art style image representing this memory: {memory_text}. Use only black and white colors, minimal details, and abstract shapes. No realistic features or details."
        return self.generate_image(prompt)

    def generate_emotion_image(self, emotion: str, intensity: str = "medium") -> Tuple[str, Optional[str]]:
        """
        Generate an image representing an emotion.
        
        Args:
            emotion (str): The emotion to visualize
            intensity (str): The intensity of the emotion (low, medium, high)
            
        Returns:
            Tuple[str, Optional[str]]: A tuple containing the image URL and any error message
        """
        if not emotion:
            return "", "No emotion provided"
            
        # Modify prompt to ensure silhouette/clip art style for emotions
        prompt = f"Create a simple silhouette or clip art style image representing {intensity} intensity {emotion}. Use only black and white colors, minimal details, and abstract shapes. No realistic features or details."
        return self.generate_image(prompt) 