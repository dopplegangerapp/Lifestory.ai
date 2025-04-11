import openai
import os
from typing import Dict, Optional, List
import logging
import json

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        openai.api_key = self.api_key
        
        # Create or retrieve the interview assistant
        self.assistant_id = self._get_or_create_assistant()
        logger.info(f"Using assistant ID: {self.assistant_id}")

    def _get_or_create_assistant(self) -> str:
        """Get or create the interview assistant"""
        try:
            # List existing assistants
            assistants = openai.beta.assistants.list()
            
            # Look for our interview assistant
            for assistant in assistants.data:
                if assistant.name == "Life Story Interviewer":
                    return assistant.id
            
            # If not found, create a new one
            assistant = openai.beta.assistants.create(
                name="Life Story Interviewer",
                instructions="""You are an expert interviewer conducting a life story interview.
                Your role is to:
                1. Generate relevant, open-ended questions that encourage detailed responses
                2. Consider the interview context and previous answers
                3. Progress naturally through different life stages
                4. Be empathetic and understanding, especially with sensitive topics
                5. Validate answers and suggest follow-up questions when needed
                
                IMPORTANT: You must format your responses as JSON objects with specific fields:
                
                For get_next_question requests:
                {
                    "question": "The actual question to ask",
                    "stage": "The current interview stage (foundations, childhood, etc.)",
                    "context": "Brief explanation of why this question is relevant"
                }
                
                For process_answer requests:
                {
                    "is_relevant": true/false,
                    "key_information": "Extracted key information from the answer",
                    "needs_follow_up": true/false,
                    "suggested_follow_up": "Follow-up question if needed",
                    "analysis": "Your analysis of the answer"
                }
                
                Always return valid JSON with all required fields.""",
                model="gpt-4-turbo-preview",
                tools=[{"type": "code_interpreter"}]
            )
            return assistant.id
            
        except Exception as e:
            logger.error(f"Error creating assistant: {str(e)}")
            raise

    def _create_thread(self) -> str:
        """Create a new conversation thread"""
        try:
            thread = openai.beta.threads.create()
            return thread.id
        except Exception as e:
            logger.error(f"Error creating thread: {str(e)}")
            raise

    def _add_message(self, thread_id: str, content: str) -> None:
        """Add a message to the thread"""
        try:
            openai.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=content
            )
        except Exception as e:
            logger.error(f"Error adding message: {str(e)}")
            raise

    def _run_assistant(self, thread_id: str) -> str:
        """Run the assistant on the thread and get the response"""
        try:
            run = openai.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=self.assistant_id
            )
            
            # Wait for the run to complete
            while True:
                run_status = openai.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
                if run_status.status == 'completed':
                    break
                elif run_status.status in ['failed', 'cancelled', 'expired']:
                    raise Exception(f"Run failed with status: {run_status.status}")
            
            # Get the messages
            messages = openai.beta.threads.messages.list(thread_id=thread_id)
            return messages.data[0].content[0].text.value
            
        except Exception as e:
            logger.error(f"Error running assistant: {str(e)}")
            raise

    def get_next_question(self, context: Dict) -> Dict:
        """
        Generate the next interview question based on the context.
        """
        try:
            # Create a new thread
            thread_id = self._create_thread()
            
            # Add system message to enforce format
            self._add_message(thread_id, """SYSTEM: You must respond with a JSON object in this exact format:
            {
                "question": "The actual question to ask",
                "stage": "The current interview stage (foundations, childhood, etc.)",
                "context": "Brief explanation of why this question is relevant"
            }""")
            
            # Add the context as a message
            self._add_message(thread_id, json.dumps({
                "type": "get_next_question",
                "context": context
            }))
            
            # Run the assistant and get the response
            response = self._run_assistant(thread_id)
            result = json.loads(response)
            logger.info(f"Generated next question: {result}")
            return result

        except Exception as e:
            logger.error(f"Error generating next question: {str(e)}")
            return {
                "question": "Can you tell me more about your early life?",
                "stage": "foundations",
                "context": "Starting the interview"
            }

    def process_interview_answer(self, current_question: str, answer: str, context: Dict) -> Dict:
        """
        Process an interview answer using OpenAI to:
        1. Validate the answer's relevance
        2. Extract key information
        3. Determine appropriate follow-up
        """
        try:
            # Create a new thread
            thread_id = self._create_thread()
            
            # Add system message to enforce format
            self._add_message(thread_id, """SYSTEM: You must respond with a JSON object in this exact format:
            {
                "is_relevant": true/false,
                "key_information": "Extracted key information from the answer",
                "needs_follow_up": true/false,
                "suggested_follow_up": "Follow-up question if needed",
                "analysis": "Your analysis of the answer"
            }""")
            
            # Add the context as a message
            self._add_message(thread_id, json.dumps({
                "type": "process_answer",
                "current_question": current_question,
                "answer": answer,
                "context": context
            }))
            
            # Run the assistant and get the response
            response = self._run_assistant(thread_id)
            result = json.loads(response)
            logger.info(f"Processed answer: {result}")
            return result

        except Exception as e:
            logger.error(f"Error processing answer with OpenAI: {str(e)}")
            return {
                "is_relevant": True,
                "key_information": answer,
                "needs_follow_up": False,
                "suggested_follow_up": None,
                "analysis": "Error processing answer"
            }

    def generate_follow_up_question(self, context: Dict) -> Optional[str]:
        """
        Generate a follow-up question based on the interview context
        """
        try:
            conversation = [
                {"role": "system", "content": """You are an expert interviewer. Generate a relevant follow-up question
                based on the interview context. The question should be open-ended and encourage detailed responses."""},
                {"role": "user", "content": f"Interview context: {context}"}
            ]

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=conversation,
                temperature=0.7,
                max_tokens=100
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Error generating follow-up question: {str(e)}")
            return None

# Create a global instance
openai_service = OpenAIService() 