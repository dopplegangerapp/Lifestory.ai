from typing import Dict, List, Optional
from datetime import datetime

class InterviewStage:
    def __init__(self):
        self.current_stage = "foundations"
        self.current_question = None
        self.answers = []
        self.completed = False
        self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        """Convert the stage to a dictionary for storage"""
        return {
            "current_stage": self.current_stage,
            "current_question": self.current_question,
            "answers": self.answers,
            "completed": self.completed,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'InterviewStage':
        """Create a stage from a dictionary"""
        stage = cls()
        stage.current_stage = data.get("current_stage", "foundations")
        stage.current_question = data.get("current_question")
        stage.answers = data.get("answers", [])
        stage.completed = data.get("completed", False)
        stage.created_at = data.get("created_at", datetime.now().isoformat())
        return stage

    def add_answer(self, answer: str) -> None:
        """Add an answer to the stage"""
        if self.current_question:
            self.answers.append({
                "question": self.current_question,
                "answer": answer,
                "stage": self.current_stage,
                "timestamp": datetime.now().isoformat()
            })

    def get_progress(self) -> float:
        """Calculate interview progress as a percentage"""
        # This is a simplified progress calculation
        # You might want to adjust this based on your needs
        if self.completed:
            return 100.0
        
        # Base progress on number of answers
        base_progress = min(len(self.answers) * 10, 90)  # Cap at 90% until completed
        return float(base_progress) 