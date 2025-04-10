from typing import Optional
import openai
import os

class WhisperTranscriber:
    """Handles audio transcription using OpenAI's Whisper model."""
    
    def __init__(self, api_key: str):
        """
        Initialize the transcriber.
        
        Args:
            api_key (str): OpenAI API key
        """
        self.api_key = api_key
        openai.api_key = api_key
    
    def transcribe_audio(self, 
                        audio_path: str,
                        language: Optional[str] = None) -> str:
        """
        Transcribe audio file to text using Whisper.
        
        Args:
            audio_path (str): Path to audio file
            language (str, optional): Language code (e.g., 'en', 'es')
            
        Returns:
            str: Transcribed text
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe(
                    "whisper-1",
                    audio_file,
                    language=language
                )
            return transcript.text
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
    
    def transcribe_audio_chunk(self,
                             audio_chunk: bytes,
                             language: Optional[str] = None) -> str:
        """
        Transcribe an audio chunk to text using Whisper.
        
        Args:
            audio_chunk (bytes): Audio data in bytes
            language (str, optional): Language code
            
        Returns:
            str: Transcribed text
        """
        try:
            transcript = openai.Audio.transcribe(
                "whisper-1",
                audio_chunk,
                language=language
            )
            return transcript.text
        except Exception as e:
            raise Exception(f"Transcription failed: {str(e)}")
