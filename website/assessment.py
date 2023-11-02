from flask import Blueprint, jsonify, request  # Import 'request'
from .models import HTMLAssessment, CSSAssessment
from sqlalchemy.sql.expression import func
from flask_login import login_required, current_user

assessment = Blueprint('assessment', __name__)

@assessment.route('/api/questions', methods=['GET'])
@login_required
def get_assessment_questions():
    if current_user.is_authenticated:
        question_count = int(request.args.get('count', 1))
        questions = HTMLAssessment.query.order_by(func.random()).limit(question_count).all()

        questions_json = [question.to_dict() for question in questions]
        return jsonify(questions_json)
    else:
        return jsonify(error="You must be logged in to access this page"), 403
