from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .email import send_password_reset_email

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                session['user_id'] = user.id # Storing data in the session
                flash('Logged in successfully!', category='success')
                login_user(user, remember=remember) # Passing the "remember" value to login_user
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            flash('Proceed to login.', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    # Route logic for reset password request
    user = None  # Initialize the user variable
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
    
    if user:
        # Generate a unique token for resetting the password
        user.reset_password_token = User.get_reset_password_token()
        db.session.commit()
        # Send an email with a link to reset the password
        send_password_reset_email(user)
        flash('An email with instructions to reset your password has been sent to your email.', category='info')
        return redirect(url_for('auth.login'))
    else:
        flash('Email not found. Please check the email address and try again.', category='error')

    return render_template('reset_password_request.html', user=current_user)

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Route logic for password reset
    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if new_password != confirm_password:
            flash('Passwords do not match. Please try again.', category='error')
        else:
            user = User.verify_reset_password_token(token)
            if user:
                hashed_password = generate_password_hash(new_password, method='sha256')
                user.password = hashed_password
                user.reset_password_token = None
                db.session.commit()
                flash('Your password has been reset successfully. You can now log in with your new password.', category='success')
                return redirect(url_for('auth.login'))
            else:
                flash('Invalid or expired token. Please request a new password reset.', category='error')

    return render_template('reset_password.html', token=token, user=current_user)