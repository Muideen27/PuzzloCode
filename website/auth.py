from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, SignupForm, ResetPasswordRequestForm, ResetPasswordForm
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .email import send_password_reset_email

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash('Logged in successfully!', category='success')
            return redirect(url_for('views.home'))
        flash('Incorrect email or password. Please try again.', category='error')
    return render_template("login.html", user=current_user, form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignupForm()

    if form.validate_on_submit():
        email = form.email.data
        first_name = form.first_name.data
        password = form.password1.data

        if User.query.filter_by(email=email).first():
            flash('Email already exists.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created! Proceed to login.', category='success')
            return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user, form=form)

@auth.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()

    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()

        if user:
            reset_password_token = user.get_reset_password_token(user.id)
            db.session.commit()

            send_password_reset_email(user)
            flash('An email with instructions to reset your password has been sent to your email.', category='info')
            return redirect(url_for('auth.login'))
        else:
            flash('Email not found. Please check the email address and try again.', category='error')

    return render_template('reset_password_request.html', user=current_user, form=form)

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    form = ResetPasswordForm()

    if form.validate_on_submit():
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

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
                return redirect(url_for('auth.login'))  # Return a valid response here

            flash('Invalid or expired token. Please request a new password reset.', category='error')

    return render_template('reset_password.html', token=token, user=current_user, form=form)