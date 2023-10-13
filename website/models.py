from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class BaseCodingQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    option_A = db.Column(db.String(250), nullable=True)
    option_B = db.Column(db.String(250), nullable=True)
    option_C = db.Column(db.String(250), nullable=True)
    option_D = db.Column(db.String(250), nullable=True)
    correct_answer = db.Column(db.String(1), nullable=False)

    __abstract__ = True

    def to_dict(self):
        return {
            'id': self.id,
            'question_text': self.question_text,
            'difficulty': self.difficulty,
            'topic': self.topic,
            'option_A': self.option_A,
            'option_B': self.option_B,
            'option_C': self.option_C,
            'option_D': self.option_D,
            'correct_answer': self.correct_answer
    }

class OnlineAssessment(BaseCodingQuestion):
    __tablename__ = 'online_assessment'

class HTMLAssessment(BaseCodingQuestion):
    __tablename__ = 'html_assessment'

class CSSAssessment(BaseCodingQuestion):
    __tablename__ = 'css_assessment'

class JsAssessment(BaseCodingQuestion):
    __tablename__ = 'js_assessment'

class VCSAssessment(BaseCodingQuestion):
    __tablename__ = 'vcs_assessment'

class FrameworkAssessment(BaseCodingQuestion):
    __tablename__ = 'fw_assessment'