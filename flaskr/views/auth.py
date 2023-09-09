import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from flaskr.models import User
from flaskr.validations import validate_auth_form

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        print("handling POST")
        post_data = {
            "username": request.form.get("username"),
            "password": request.form.get("password"),
        }

        if err := validate_auth_form(post_data):
            flash(err)

        if err := User.from_post_data(post_data).commit():
            flash(err)
        else:
            print("redirecting")
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        post_data = {
            "username": request.form.get("username"),
            "password": request.form.get("password"),
        }

        if err := validate_auth_form(post_data):
            flash(err)

        if user := User.get_one(post_data):
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("index"))
        else:
            flash("Try Again!")

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    g.user = User.get_by_id(session.get("user_id") or -1)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
