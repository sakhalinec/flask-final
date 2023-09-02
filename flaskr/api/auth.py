from datetime import datetime, timedelta

import jwt
from flask import Flask, Blueprint, request, make_response, jsonify, current_app
from werkzeug.security import check_password_hash, generate_password_hash


from flaskr.db import get_db
from flaskr.validations import validate_auth_form
from flaskr.models import User

auth_blueprint = Blueprint("authAPI", __name__, url_prefix="/api/auth")


def _encode_auth_token(user_id: str) -> str:
    payload = {
        "exp": datetime.utcnow() + timedelta(days=0, seconds=5),
        "iat": datetime.utcnow(),
        "sub": user_id,
    }
    return jwt.encode(payload, current_app.config.get("SECRET_KEY"), algorithm="HS256")


def _decode_auth_token(auth_token: str) -> str:
    try:
        payload = jwt.decode(auth_token, current_app.config.get("SECRET_KEY"))
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return "Signature expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."


@auth_blueprint.route("/register", methods=["POST"])
def register():
    # get the post data
    post_data = request.get_json()

    if err := validate_auth_form(post_data):
        response = {"status": "fail", "message": err}
        return make_response(jsonify(response)), 400

    resp, code = User(post_data).commit()
    return make_response(jsonify(resp)), code
