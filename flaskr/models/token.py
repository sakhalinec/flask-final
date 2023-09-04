from datetime import datetime
from flaskr.db import get_db


class BlackJWToken:
    def __init__(self, token: str) -> None:
        self.token = token
        self.blacklisted_on = datetime.now()
        self.id = -1

    def commit(self) -> None:
        db = get_db()

        db.execute(
            "INSERT INTO invalidtokens (token, blacklisted_on) VALUES (?, ?)",
            (self.token, self.blacklisted_on),
        )
        db.commit()

    def is_blacklisted(self) -> bool:
        db = get_db()
        return bool(db.execute(
            f"SELECT token from invalidtokens WHERE token='{self.token}'",
        ).fetchone())
