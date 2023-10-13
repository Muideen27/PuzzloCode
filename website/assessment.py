from flask import Blueprint, jsonify
from .models import HTMLAssessment, CSSAssessment  # Import all relevant models
from sqlalchemy.sql.expression import func
from flask_login import login_required, current_user

assessment = Blueprint('assessment', __name__)

@assessment.route('/html-assessment-questions', methods=['GET'])
@login_required
def get_html_assessment_questions():
    # Check if the user is authenticated
    if current_user.is_authenticated:
        # Query the database for random HTML assessment questions
        questions = HTMLAssessment.query.order_by(func.random()).limit(1).all()

        # Convert the questions to a JSON format
        questions_json = [question.to_dict() for question in questions]
    
        # Return the questions as a JSON response
        return jsonify(questions_json)
    else:
        return "You must be logged in to access this page"
