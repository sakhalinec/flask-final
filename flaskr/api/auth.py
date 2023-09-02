from datetime import datetime, timedelta
from typing import Optional

import jwt
from flask import Blueprint, request, make_response, jsonify, current_app

from flaskr.validations import validate_auth_form
from flaskr.models import User, BlackJWToken

auth_blueprint = Blueprint("authAPI", __name__, url_prefix="/api/auth")


def _encode_auth_token(user_id: int) -> str:
    payload = {
        "exp": datetime.utcnow() + timedelta(days=0, seconds=50),
        "iat": datetime.utcnow(),
        "sub": user_id,
    }
    return jwt.encode(payload, current_app.config.get("SECRET_KEY"), algorithm="HS256")


def _decode_auth_token(auth_token: str) -> tuple[Optional[str], Optional[str]]:
    try:
        payload = jwt.decode(auth_token, current_app.config.get("SECRET_KEY"), algorithms=["HS256"])
        return payload["sub"], None
    except jwt.ExpiredSignatureError:
        return None, "Signature expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"


@auth_blueprint.route("/register", methods=["POST"])
def register():
    # get the post data
    post_data = request.get_json()

    if err := validate_auth_form(post_data):
        response = {"status": "fail", "message": err}
        return make_response(jsonify(response)), 400

    if err := User.from_post_data(post_data).commit():
        resp = {"status": "fail", "message": err}
        return make_response(jsonify(resp)), 418

    resp = {"status": "success", "message": "Successfully registered. Please Login"}

    return make_response(jsonify(resp)), 201


@auth_blueprint.route("/login", methods=["POST"])
def login():
    post_data = request.get_json()

    if err := validate_auth_form(post_data):
        response = {"status": "fail", "message": err}
        return make_response(jsonify(response)), 400

    if user := User.get_one(post_data):
        auth_token = _encode_auth_token(user.id)
        responseObject = {
            "status": "success",
            "message": "Successfully logged in.",
            "auth_token": auth_token,
        }
        return make_response(jsonify(responseObject)), 200
    else:
        responseObject = {"status": "fail", "message": "Try again"}
        return make_response(jsonify(responseObject)), 500


@auth_blueprint.route("/logout", methods=["POST"])
def logout():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        responseObject = {"status": "fail", "message": "Missing Authorization Header"}
        return make_response(jsonify(responseObject)), 400

    _, token = auth_header.split(" ")

    print(f"{token = }")

    _, err = _decode_auth_token(token)
    if err:
        responseObject = {"status": "fail", "message": err}
        return make_response(jsonify(responseObject)), 400

    BlackJWToken(token).commit()

    responseObject = {"status": "success", "message": "Successfully logged out."}
    return make_response(jsonify(responseObject)), 200
