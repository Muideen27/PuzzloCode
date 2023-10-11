from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class CodingQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(100), nullable=False)

    # Fields for multiple-choice options
    option_A = db.Column(db.String(250), nullable=True)
    option_B = db.Column(db.String(250), nullable=True)
    option_C = db.Column(db.String(250), nullable=True)
    option_D = db.Column(db.String(250), nullable=True)

    # Correct answer (e.g., 'A', 'B', 'C', or 'D')
    correct_answer = db.Column(db.String(1), nullable=False)

    # Additional fields you might consider:
    # - Explanation for the correct answer
    # - Tags or categories for better organization
    # - Creation date or timestamp
    # - Author or source of the question

    def __repr__(self):
        return f'<CodingQuestion: {self.id}>'