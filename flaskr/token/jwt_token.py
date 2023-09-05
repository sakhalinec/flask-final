from datetime import datetime, timedelta
from typing import Optional


from flask import current_app

import jwt


def encode_auth_token(user_id: int) -> str:
    payload = {
        "exp": datetime.utcnow() + timedelta(days=0, seconds=5),
        "iat": datetime.utcnow(),
        "sub": user_id,
    }
    return jwt.encode(payload, current_app.config.get("SECRET_KEY"), algorithm="HS256")


def decode_auth_token(auth_token: str) -> tuple[Optional[str], Optional[str]]:
    try:
        payload = jwt.decode(
            auth_token, current_app.config.get("SECRET_KEY"), algorithms=["HS256"]
        )
        return payload["sub"], None
    except jwt.ExpiredSignatureError:
        return None, "Signature expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"
