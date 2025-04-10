from flask import Blueprint, render_template, request, jsonify, session
from datetime import datetime
from typing import Dict, List, Optional, Any
from ai.prompt_engine import PromptEngine
from ai.image_generator import ImageGenerator
from utils.db_utils import get_db
from ai.assistant import Assistant
from dataclasses import dataclass, field, asdict
import json
import random

interview_bp = Blueprint('interview', __name__)

class InterviewStage:
    def __init__(self):
        self.current_stage = "welcome"
        self.current_question_index = 0
        self.answers = []
        self.completed = False
        self.created_at = datetime.now()
        self.context = {}  # Store context for personalized follow-up questions
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "current_stage": self.current_stage,
            "current_question_index": self.current_question_index,
            "answers": self.answers,
            "completed": self.completed,
            "created_at": self.created_at.isoformat(),
            "context": self.context
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'InterviewStage':
        stage = cls()
        stage.current_stage = data.get("current_stage", "welcome")
        stage.current_question_index = data.get("current_question_index", 0)
        stage.answers = data.get("answers", [])
        stage.completed = data.get("completed", False)
        stage.created_at = datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
        stage.context = data.get("context", {})
        return stage

# Interview questions by stage with context-aware follow-ups
INTERVIEW_QUESTIONS = {
    "welcome": [
        {
            "question": "Welcome to your life story interview! I'm DROE, your AI assistant. What would you like me to call you?",
            "context_key": "name",
            "follow_up": "It's nice to meet you, {name}! Let's begin documenting your life story."
        }
    ],
    "foundations": [
        {
            "question": "When and where were you born?",
            "context_key": "birth",
            "follow_up": "Thank you for sharing that. Let's explore your early years in {birth_place}."
        },
        {
            "question": "What are your parents' names and what were they like?",
            "context_key": "parents",
            "follow_up": "Your parents sound like {parent_quality}. How did they influence your upbringing?"
        },
        {
            "question": "Do you have any siblings? If so, what are their names and what was your relationship like growing up?",
            "context_key": "siblings",
            "follow_up": "It sounds like you had a {sibling_relationship} relationship with your siblings. How did this shape your childhood?"
        }
    ],
    "childhood": [
        {
            "question": "What are your earliest childhood memories?",
            "context_key": "early_memories",
            "follow_up": "Those sound like {memory_quality} memories. What made them so special to you?"
        },
        {
            "question": "What was your childhood home like? Describe the place where you grew up.",
            "context_key": "childhood_home",
            "follow_up": "Your childhood home sounds {home_quality}. How did this environment influence you?"
        },
        {
            "question": "What were your favorite activities or hobbies as a child?",
            "context_key": "childhood_hobbies",
            "follow_up": "It's interesting that you enjoyed {hobby}. How did this interest develop over time?"
        }
    ],
    "education": [
        {
            "question": "What schools did you attend growing up? Which one left the biggest impression on you?",
            "context_key": "schools",
            "follow_up": "Your experience at {school_name} sounds {school_quality}. How did this shape your educational journey?"
        },
        {
            "question": "Who were some of your favorite teachers and why?",
            "context_key": "teachers",
            "follow_up": "It seems {teacher_name} had a significant impact on you. How did they influence your life?"
        },
        {
            "question": "What were your dreams and aspirations as a child?",
            "context_key": "childhood_dreams",
            "follow_up": "Your dream of {dream} is fascinating. How has this evolved over time?"
        }
    ],
    "life_moments": [
        {
            "question": "What are some of the most significant moments or turning points in your life?",
            "context_key": "turning_points",
            "follow_up": "That moment when {turning_point} must have been {emotion_quality}. How did it change you?"
        },
        {
            "question": "What challenges have you faced, and how did you overcome them?",
            "context_key": "challenges",
            "follow_up": "Facing {challenge} must have been difficult. What strengths did you discover in yourself?"
        },
        {
            "question": "What achievements are you most proud of?",
            "context_key": "achievements",
            "follow_up": "Your achievement of {achievement} is impressive. What did you learn from this experience?"
        }
    ],
    "relationships": [
        {
            "question": "Who are the most important people in your life?",
            "context_key": "important_people",
            "follow_up": "{person_name} sounds like a {relationship_quality} presence in your life. How did you meet?"
        },
        {
            "question": "What qualities do you value most in your relationships?",
            "context_key": "relationship_values",
            "follow_up": "Your emphasis on {value} in relationships is meaningful. How has this value guided your life?"
        },
        {
            "question": "What lessons have you learned about love and friendship?",
            "context_key": "relationship_lessons",
            "follow_up": "The lesson about {lesson} is profound. How has this wisdom served you?"
        }
    ],
    "reflection": [
        {
            "question": "What are the most important lessons life has taught you?",
            "context_key": "life_lessons",
            "follow_up": "The lesson about {lesson} is powerful. How has it influenced your decisions?"
        },
        {
            "question": "How have you grown as a person over the years?",
            "context_key": "personal_growth",
            "follow_up": "Your growth in {area} is remarkable. What helped you develop this aspect of yourself?"
        },
        {
            "question": "What legacy do you hope to leave behind?",
            "context_key": "legacy",
            "follow_up": "Your vision of {legacy_goal} is inspiring. What steps are you taking to achieve this?"
        }
    ]
}

def get_or_create_stage() -> InterviewStage:
    if 'interview_stage' not in session:
        stage = InterviewStage()
        session['interview_stage'] = stage.to_dict()
    else:
        stage = InterviewStage.from_dict(session['interview_stage'])
    return stage

def generate_follow_up_question(stage: InterviewStage, answer: str) -> str:
    """Generate a personalized follow-up question based on the answer and context."""
    current_question = INTERVIEW_QUESTIONS[stage.current_stage][stage.current_question_index]
    context_key = current_question.get('context_key')
    
    if context_key:
        # Simple context extraction (in a real app, this would use NLP)
        stage.context[context_key] = answer
        follow_up = current_question.get('follow_up', '')
        
        # Replace placeholders with context
        for key, value in stage.context.items():
            follow_up = follow_up.replace(f"{{{key}}}", str(value))
        
        return follow_up
    return ""

@interview_bp.route('/', strict_slashes=False, methods=['GET'])
def get_question():
    stage = get_or_create_stage()
    
    if stage.completed:
        return jsonify({
            "question": "Thank you for sharing your story! Your life journey has been documented.",
            "completed": True
        })
    
    current_stage_questions = INTERVIEW_QUESTIONS.get(stage.current_stage, [])
    if not current_stage_questions or stage.current_question_index >= len(current_stage_questions):
        # Move to next stage
        stages = list(INTERVIEW_QUESTIONS.keys())
        current_stage_index = stages.index(stage.current_stage)
        if current_stage_index < len(stages) - 1:
            stage.current_stage = stages[current_stage_index + 1]
            stage.current_question_index = 0
            session['interview_stage'] = stage.to_dict()
            return get_question()
        else:
            stage.completed = True
            session['interview_stage'] = stage.to_dict()
            return jsonify({
                "question": "Thank you for sharing your story! Your life journey has been documented.",
                "completed": True
            })
    
    question_data = current_stage_questions[stage.current_question_index]
    return jsonify({
        "question": question_data["question"],
        "current_stage": stage.current_stage,
        "progress": (stage.current_question_index / len(current_stage_questions)) * 100
    })

@interview_bp.route('/', strict_slashes=False, methods=['POST'])
def submit_answer():
    stage = get_or_create_stage()
    data = request.get_json()
    answer = data.get('answer', '').strip()
    
    if not answer:
        return jsonify({"error": "Answer cannot be empty"}), 400
    
    current_stage_questions = INTERVIEW_QUESTIONS.get(stage.current_stage, [])
    if stage.current_question_index < len(current_stage_questions):
        question_data = current_stage_questions[stage.current_question_index]
        follow_up = generate_follow_up_question(stage, answer)
        
        stage.answers.append({
            "question": question_data["question"],
            "answer": answer,
            "follow_up": follow_up,
            "stage": stage.current_stage,
            "timestamp": datetime.now().isoformat()
        })
        
        # Move to next question
        stage.current_question_index += 1
        
        # Check if we need to move to next stage
        if stage.current_question_index >= len(current_stage_questions):
            stages = list(INTERVIEW_QUESTIONS.keys())
            current_stage_index = stages.index(stage.current_stage)
            if current_stage_index < len(stages) - 1:
                stage.current_stage = stages[current_stage_index + 1]
                stage.current_question_index = 0
            else:
                stage.completed = True
        
        session['interview_stage'] = stage.to_dict()
        
        # Get the next question
        next_question_data = None
        if not stage.completed:
            next_stage_questions = INTERVIEW_QUESTIONS.get(stage.current_stage, [])
            if stage.current_question_index < len(next_stage_questions):
                next_question_data = next_stage_questions[stage.current_question_index]
        
        return jsonify({
            "success": True,
            "follow_up": follow_up,
            "next_question": next_question_data["question"] if next_question_data else None,
            "current_stage": stage.current_stage,
            "progress": (stage.current_question_index / len(INTERVIEW_QUESTIONS.get(stage.current_stage, []))) * 100,
            "completed": stage.completed
        })
    
    return jsonify({"error": "Invalid question index"}), 400

@interview_bp.route('/progress', methods=['GET'], strict_slashes=False)
def get_interview_progress():
    """Get the current interview progress."""
    stage = get_or_create_stage()
    return jsonify({
        'current_stage': stage.current_stage,
        'stage_name': stage.current_stage,
        'progress': (stage.current_question_index / len(INTERVIEW_QUESTIONS.get(stage.current_stage, []))) * 100,
        'is_complete': stage.completed
    })
