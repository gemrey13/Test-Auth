from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from controllers.auth_controller import (
    register_user,
    verify_user_code,
    login_user,
    refresh_access_token
)

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():
    return register_user(request.get_json())

@auth.route("/verify-code", methods=["POST"])
def verify_code():
    return verify_user_code(request.get_json())

@auth.route("/login", methods=["POST"])
def login():
    return login_user(request.get_json())

@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    return refresh_access_token()
