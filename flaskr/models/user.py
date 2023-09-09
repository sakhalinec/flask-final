from dataclasses import dataclass
from typing import Self, Optional
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db


@dataclass
class User:
    username: str
    password: str
    id: int = -1

    @classmethod
    def from_post_data(cls, form: dict) -> Self:
        return cls(
            username=form["username"], password=generate_password_hash(form["password"])
        )

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

    @classmethod
    def get_one(cls, data: dict) -> Optional[Self]:
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (data["username"],)
        ).fetchone()

        if not user:
            return None
        if not check_password_hash(user["password"], data["password"]):
            return None

        return cls(username=user["username"], password=user["password"], id=user["id"])

    @classmethod
    def get_by_id(cls, id: int) -> Optional[Self]:
        db = get_db()
        user = db.execute("SELECT * FROM user WHERE id = ?", (id,)).fetchone()
        if not user:
            return None

        return cls(username=user["username"], password=user["password"], id=user["id"])
