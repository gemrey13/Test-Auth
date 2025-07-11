from datetime import datetime, timedelta
from flask import jsonify
from models import User
from extensions import db, mail
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from utils import generate_verification_code


def register_user(data):
    email = data["email"]
    password = generate_password_hash(data["password"])

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 400

    code = generate_verification_code()
    user = User(
        email=email,
        password=password,
        verification_code=code,
        code_sent_at=datetime.now(),
    )
    db.session.add(user)
    db.session.commit()

    msg = Message("Your Verification Code", recipients=[email])
    msg.body = f"Your verification code is: {code}"
    mail.send(msg)

    return jsonify({"message": "Verification code sent to email"}), 201


def verify_user_code(data):
    email = data["email"]
    code = data["code"]

    user = User.query.filter_by(email=email).first()

    if not user or user.verification_code != code:
        return jsonify({"message": "Invalid code"}), 400

    if datetime.now() - user.code_sent_at > timedelta(minutes=10):
        return jsonify({"message": "Code expired"}), 400

    user.is_verified = True
    user.verification_code = None
    user.code_sent_at = None
    db.session.commit()

    msg = Message(subject="Welcome to Our App!", recipients=[email])
    msg.body = (
        f"Hi there,\n\n"
        f"Thank you for verifying your email. We're excited to have you on board!\n\n"
        f"Enjoy your experience with us.\n\n"
        f"Best,\n"
        f"The Team"
    )
    mail.send(msg)

    return jsonify({"message": "Email verified successfully and welcome message sent!"})


def login_user(data):
    user = User.query.filter_by(email=data["email"]).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401
    if not user.is_verified:
        return jsonify({"message": "Email not verified"}), 403

    access_token = create_access_token(identity={"id": user.id, "email": user.email, "is_verified": user.is_verified})
    refresh_token = create_refresh_token(identity={"id": user.id, "email": user.email, "is_verified": user.is_verified})

    return jsonify({"access_token": access_token, "refresh_token": refresh_token})


def refresh_access_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    return jsonify({"access_token": new_access_token})
