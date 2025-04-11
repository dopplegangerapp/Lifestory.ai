import unittest
from services.openai_service import OpenAIService
import os

class TestOpenAIService(unittest.TestCase):
    def setUp(self):
        self.service = OpenAIService()

    def test_assistant_creation(self):
        """Test that the assistant is created and accessible"""
        self.assertIsNotNone(self.service.assistant_id)
        print(f"Assistant ID: {self.service.assistant_id}")

    def test_get_next_question(self):
        """Test question generation"""
        context = {
            "answers": [],
            "current_stage": "foundations"
        }
        result = self.service.get_next_question(context)
        print(f"Generated question: {result}")
        self.assertIsNotNone(result)
        self.assertIn("question", result)
        self.assertIn("stage", result)

    def test_process_answer(self):
        """Test answer processing"""
        result = self.service.process_interview_answer(
            "Where were you born and where did you grow up?",
            "I was born in Portland, Oregon and grew up in a small house near the river.",
            {"answers": []}
        )
        print(f"Processed answer: {result}")
        self.assertIsNotNone(result)
        self.assertIn("is_relevant", result)
        self.assertIn("key_information", result)

if __name__ == '__main__':
    unittest.main() 