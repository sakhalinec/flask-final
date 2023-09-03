from datetime import datetime
from dataclasses import dataclass, field
from typing import Iterable, Optional, Self

from flaskr.db import get_db


@dataclass(kw_only=True)
class Post:
    author_id: int
    title: str
    body: str
    id: int = -1
    created: datetime = datetime(year=1999, month=1, day=1)

    @classmethod
    def get_all(cls) -> Iterable[Self]:
        db = get_db()
        posts = db.execute(
            "SELECT id, title, body, created, author_id FROM post"
        ).fetchall()
        for post in posts:
            yield cls(**post)

    @classmethod
    def get_by_id(cls, id: int) -> Optional[Self]:
        db = get_db()
        post = db.execute(
            "SELECT title, body, created, author_id, id FROM post WHERE id = ?",
            (id,),
        ).fetchone()

        if post is None:
            return None

        return cls(**post)

    def commit(self) -> None:
        db = get_db()
        db.execute(
            "INSERT INTO post (title, body, author_id)" " VALUES (?, ?, ?)",
            (self.title, self.body, self.author_id),
        )
        db.commit()

    def update(self, title: str, body: str) -> None:
        self.title = title
        self.body = body
        db = get_db()
        db.execute(
            "UPDATE post SET title = ?, body = ?" " WHERE id = ?",
            (self.title, self.body, self.id),
        )
        db.commit()
