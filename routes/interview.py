from flask import Blueprint, jsonify, request, session
from datetime import datetime
from typing import Dict, List, Optional

interview_bp = Blueprint('interview', __name__)

INTERVIEW_QUESTIONS = {
    "welcome": [
        {"question": "Are you ready to begin your life story interview?"}
    ],
    "foundations": [
        {"question": "What is your full name and when were you born?"},
        {"question": "Where were you born and where did you grow up?"},
        {"question": "Tell me about your parents and siblings."},
        {"question": "What are your earliest memories?"}
    ],
    "childhood": [
        {"question": "What was your childhood home like?"},
        {"question": "What were your favorite activities as a child?"},
        {"question": "Who were your closest friends growing up?"}
    ]
}

class InterviewStage:
    def __init__(self):
        self.current_stage = "welcome"
        self.current_question_index = 0
        self.answers = []
        self.completed = False
        self.created_at = datetime.now()

    def to_dict(self) -> Dict:
        return {
            "current_stage": self.current_stage,
            "current_question_index": self.current_question_index,
            "answers": self.answers,
            "completed": self.completed,
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'InterviewStage':
        if not isinstance(data, dict):
            raise ValueError("Invalid data format for InterviewStage")

        instance = cls()
        instance.current_stage = data.get("current_stage", "welcome")
        instance.current_question_index = data.get("current_question_index", 0)
        instance.answers = data.get("answers", [])
        instance.completed = data.get("completed", False)
        instance.created_at = datetime.fromisoformat(data.get("created_at", datetime.now().isoformat()))
        return instance

    def advance(self) -> bool:
        """Advance to next question or stage, returns True if interview is complete"""
        if self.completed:
            return True

        current_stage_questions = INTERVIEW_QUESTIONS.get(self.current_stage, [])

        if self.current_question_index < len(current_stage_questions) - 1:
            self.current_question_index += 1
            return False

        stages = list(INTERVIEW_QUESTIONS.keys())
        try:
            current_stage_index = stages.index(self.current_stage)
        except ValueError:
            self.completed = True
            return True

        if current_stage_index < len(stages) - 1:
            self.current_stage = stages[current_stage_index + 1]
            self.current_question_index = 0
            return False

        self.completed = True
        return True

    def get_current_question(self) -> Optional[Dict]:
        if self.completed:
            return None

        current_stage_questions = INTERVIEW_QUESTIONS.get(self.current_stage, [])
        if self.current_question_index < len(current_stage_questions):
            return current_stage_questions[self.current_question_index]
        return None

    def get_progress(self) -> float:
        if self.completed:
            return 100.0

        total_questions = sum(len(questions) for questions in INTERVIEW_QUESTIONS.values())
        if total_questions == 0:
            return 0.0

        completed_questions = 0
        stages = list(INTERVIEW_QUESTIONS.keys())

        try:
            current_stage_index = stages.index(self.current_stage)
        except ValueError:
            return 0.0

        # Add completed stages
        for stage in stages[:current_stage_index]:
            completed_questions += len(INTERVIEW_QUESTIONS[stage])

        # Add current stage progress
        completed_questions += self.current_question_index

        return (completed_questions / total_questions) * 100

@interview_bp.route('/', methods=['GET'])
def get_question():
    print("Debug - Received GET request for initial question")
    try:
        if 'interview_stage' not in session:
            session['interview_stage'] = InterviewStage().to_dict()

        stage = InterviewStage.from_dict(session['interview_stage'])

        if stage.completed:
            response = {
                "question": "Thank you for sharing your story!",
                "completed": True,
                "current_stage": stage.current_stage,
                "progress": 100
            }
            print(f"Debug - Sending response: {response}")
            return jsonify(response)

        question_data = stage.get_current_question()
        if not question_data:
            return jsonify({"error": "No question available"}), 400

        session['interview_stage'] = stage.to_dict()
        response = {
            "question": question_data["question"],
            "current_stage": stage.current_stage,
            "progress": stage.get_progress()
        }
        print(f"Debug - Sending response: {response}")
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@interview_bp.route('/', methods=['POST'])
def submit_answer():
    try:
        if 'interview_stage' not in session:
            return jsonify({"error": "Interview not started"}), 400

        stage = InterviewStage.from_dict(session['interview_stage'])
        data = request.get_json()

        if not data or 'answer' not in data:
            return jsonify({"error": "No answer provided"}), 400

        answer = data['answer'].strip()
        if not answer:
            return jsonify({"error": "Answer cannot be empty"}), 400

        current_question = stage.get_current_question()
        if not current_question:
            return jsonify({"error": "No current question"}), 400

        stage.answers.append({
            "question": current_question["question"],
            "answer": answer,
            "stage": stage.current_stage,
            "timestamp": datetime.now().isoformat()
        })

        is_complete = stage.advance()
        session['interview_stage'] = stage.to_dict()

        if is_complete:
            return jsonify({
                "completed": True,
                "success": True
            })

        next_question = stage.get_current_question()
        if not next_question:
            return jsonify({"error": "Failed to get next question"}), 500

        return jsonify({
            "success": True,
            "next_question": next_question["question"],
            "current_stage": stage.current_stage,
            "progress": stage.get_progress(),
            "completed": False
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500