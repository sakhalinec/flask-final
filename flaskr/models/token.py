from datetime import datetime
from dataclasses import dataclass
from flaskr.db import get_db


@dataclass
class BlackJWToken:
    token: str
    blacklisted_on = datetime.now()
    id = -1

    def commit(self) -> None:
        db = get_db()

        db.execute(
            "INSERT INTO invalidtokens (token, blacklisted_on) VALUES (?, ?)",
            (self.token, self.blacklisted_on),
        )
        db.commit()

    def is_blacklisted(self) -> bool:
        db = get_db()
        return bool(
            db.execute(
                "SELECT token from invalidtokens WHERE token = ? ", (self.token,)
            ).fetchone()
        )
