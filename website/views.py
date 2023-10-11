from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

# Frontend Questions
@views.route('/frontend-questions')
@login_required
def frontend_questions():
    # Add your code to retrieve and display frontend questions here
    return render_template("frontend_questions.html", user=current_user)

# Backend Questions
@views.route('/backend-questions')
@login_required
def backend_questions():
    # Add your code to retrieve and display backend questions here
    return render_template("backend_questions.html")

# DevOps Questions
@views.route('/devops-questions')
@login_required
def devops_questions():
    # Add your code to retrieve and display devops questions here
    return render_template("devops_questions.html")

# Online Assessment
@views.route('/start_mock_assessment')
@login_required
def start_mock_assessment():
    return render_template("start_mock_assessment")

# HTML Questions
@views.route('/html-questions')
@login_required
def html_questions():
    return render_template("html_questions.html")