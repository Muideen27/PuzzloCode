from . import db
from flask_login import UserMixin
import secrets
import datetime
from itsdangerous import URLSafeTimedSerializer

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    #reset password logic
    reset_password_token = db.Column(db.String(100), unique=True, nullable=True)

    def get_reset_password_token(self, expires_sec=600):
        from website import app
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id, 'reset_password': True}, salt='reset-salt')
    
    @staticmethod
    def verify_reset_password_token(token):
        from website import app
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token, salt='reset-salt', max_age=600)  # Token expires in 1800 seconds (30 minutes)
            if data.get('reset_password'):
                return User.query.get(data['user_id'])
        except Exception as e:
            return None

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