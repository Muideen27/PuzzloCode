from flask import url_for
from flask_mail import Message
from . import mail
from . import db

def send_password_reset_email(user):
    token = user.get_reset_password_token(user.id)  # Pass the user_id
    msg = Message('Password Reset Request', sender='noreplymycolorfullife27@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_password', token=token, _external=True)}

If you did not make this request, please ignore this email.
'''
    mail.send(msg)
