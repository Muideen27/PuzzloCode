from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(100))
    question_text = db.Column(db.Text, nullable=False)

    def __init__(self, title, difficulty, topic, question_text):
        self.title = title
        self.difficulty = difficulty
        self.topic = topic
        self.question_text = question_text