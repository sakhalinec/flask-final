from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db


class User:
    def __init__(self, form: dict) -> None:
        self.username = form["username"]
        self.password = generate_password_hash(form["password"])
        self.id = -1

    def commit(self) -> str:
        db = get_db()

        try:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (self.username, self.password),
            )
            db.commit()
        except db.IntegrityError:
            return "User already exists. Please Log in."

        return ""
