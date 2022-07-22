import jwt
from datetime import datetime, timedelta, timezone


def issue_token(email: str) -> str:
    from config import JWT_SECRET

    payload = {
        "email": email,
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=30),
    }
    encoded = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    print(encoded)

    decoded = jwt.decode(encoded, JWT_SECRET, algorithms="HS256")

    print(decoded)

    return encoded
