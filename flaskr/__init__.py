import os

from flask import Flask
from .views import auth, blog
from . import db
from .api import auth_blueprint, blog_blueprint


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint="index")

    return app
