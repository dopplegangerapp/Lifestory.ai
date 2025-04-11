from openai import OpenAI
import os
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class ImageGenerator:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the image generator with OpenAI API key."""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = None
        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.error(f"Error initializing OpenAI client: {e}")
    
    def generate_image(self, prompt: str, size: str = "1024x1024") -> str:
        """
        Generate an image using DALL-E.
        
        Args:
            prompt: The text description of the image to generate
            size: The size of the image (1024x1024, 512x512, or 256x256)
            
        Returns:
            The URL of the generated image or a default image URL
        """
        if not self.client:
            logger.warning("OpenAI client not initialized, using default image")
            return "/static/images/default_card.png"
            
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality="standard",
                n=1
            )
            return response.data[0].url
        except Exception as e:
            logger.error(f"Error generating image: {e}")
            return "/static/images/default_card.png"
    
    def save_image(self, image_url: str, save_path: str) -> bool:
        """
        Save an image from a URL to a local file.
        
        Args:
            image_url: The URL of the image to save
            save_path: The path where to save the image
            
        Returns:
            True if the image was saved successfully, False otherwise
        """
        try:
            import requests
            from PIL import Image
            from io import BytesIO
            
            response = requests.get(image_url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                img.save(save_path)
                return True
            return False
        except Exception as e:
            logger.error(f"Error saving image: {e}")
            return False 