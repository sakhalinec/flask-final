from flask import Blueprint, request, make_response, jsonify

from flaskr.validations import validate_auth_form
from flaskr.models import User, BlackJWToken
from flaskr.token import decode_auth_token, encode_auth_token

auth_blueprint = Blueprint("authAPI", __name__, url_prefix="/api/auth")


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
        auth_token = encode_auth_token(user.id)
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

    _, err = decode_auth_token(token)
    if err:
        responseObject = {"status": "fail", "message": err}
        return make_response(jsonify(responseObject)), 400

    BlackJWToken(token).commit()

    responseObject = {"status": "success", "message": "Successfully logged out."}
    return make_response(jsonify(responseObject)), 200
