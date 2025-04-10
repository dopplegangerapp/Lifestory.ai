import os
from openai import OpenAI
from typing import Optional, Dict, Any
import time

class Assistant:
    """Handles conversation and analysis using OpenAI's Assistant API."""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.assistant = self._get_or_create_assistant()
        self.thread = self.client.beta.threads.create()

    def _get_or_create_assistant(self):
        """Get existing assistant or create a new one."""
        # List existing assistants
        assistants = self.client.beta.assistants.list()
        
        # Look for our assistant
        for assistant in assistants.data:
            if assistant.name == "DROE Life Story Assistant":
                return assistant
        
        # Create new assistant if not found
        return self.client.beta.assistants.create(
            name="DROE Life Story Assistant",
            instructions="You are a helpful assistant designed to help people document their life stories.",
            model="gpt-4-turbo-preview"
        )
    
    def create_message(self, content: str) -> Dict[str, Any]:
        """Create a new message in the thread."""
        message = self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=content
        )
        return {'id': message.id}
    
    def create_run(self) -> Dict[str, Any]:
        """Create a new run for the current thread."""
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id
        )
        return {'id': run.id}
    
    def get_response(self, timeout: int = 30) -> str:
        """Get the assistant's response."""
        # Wait for the run to complete
        start_time = time.time()
        while time.time() - start_time < timeout:
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            
            # Get the most recent assistant message
            for message in messages.data:
                if message.role == "assistant":
                    return message.content[0].text.value
            
            time.sleep(1)
        
        raise TimeoutError("Assistant did not respond in time")

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for emotions, key points, and story arcs.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Analysis results including emotions, key points, and story arcs
        """
        try:
            # Add the user's message to the thread
            message = self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=f"Analyze this text: {text}"
            )
            
            # Create a run with the assistant
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id
            )
            
            # Wait for the run to complete
            while True:
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=run.id
                )
                if run_status.status == 'completed':
                    break
                elif run_status.status == 'failed':
                    raise Exception("Run failed")
            
            # Get the assistant's response
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            
            analysis = messages.data[0].content[0].text.value
            return self._parse_analysis(analysis)
        except Exception as e:
            print(f"Error analyzing text: {e}")
            return {
                'emotions': [],
                'key_points': [],
                'story_arcs': []
            }

    def generate_follow_up(self, context: Dict[str, Any]) -> str:
        """
        Generate a follow-up question based on conversation context.
        
        Args:
            context (dict): Current conversation context
            
        Returns:
            str: Generated follow-up question
        """
        try:
            # Add the user's message to the thread
            message = self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=f"Generate a follow-up question based on this context: {context}"
            )
            
            # Create a run with the assistant
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id
            )
            
            # Wait for the run to complete
            while True:
                run_status = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=run.id
                )
                if run_status.status == 'completed':
                    break
                elif run_status.status == 'failed':
                    raise Exception("Run failed")
            
            # Get the assistant's response
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            
            return messages.data[0].content[0].text.value
        except Exception as e:
            print(f"Error generating follow-up: {e}")
            return "Can you tell me more about that?"

    def _parse_analysis(self, analysis: str) -> Dict[str, Any]:
        """
        Parse the raw analysis text into structured data.
        
        Args:
            analysis (str): Raw analysis text from GPT
            
        Returns:
            dict: Structured analysis data
        """
        # This is a simplified parser - in production, you'd want more robust parsing
        emotions = []
        key_points = []
        story_arcs = []
        
        lines = analysis.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip().lower()
            if 'emotions:' in line:
                current_section = 'emotions'
            elif 'key points:' in line:
                current_section = 'key_points'
            elif 'story arcs:' in line:
                current_section = 'story_arcs'
            elif line and current_section:
                if current_section == 'emotions':
                    emotions.append(line)
                elif current_section == 'key_points':
                    key_points.append(line)
                elif current_section == 'story_arcs':
                    story_arcs.append(line)
        
        return {
            'emotions': emotions,
            'key_points': key_points,
            'story_arcs': story_arcs
        } 