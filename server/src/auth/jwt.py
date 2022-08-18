import jwt
from fastapi import Header, HTTPException
from config import JWT_SECRET
from datetime import datetime, timedelta, timezone


def issue_token(email: str) -> str:

    payload = {
        "email": email,
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=30),
    }
    encoded = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return encoded


def get_email_from_token(Authorization: str = Header()) -> str:
    try:

        token = Authorization.split(" ")[1]
        options = dict(verify_signature=True, require=["email", "exp"], verify_exp=True)

        decoded = jwt.decode(token, JWT_SECRET, algorithms="HS256", options=options)
        #TODO: Should check if the email is associated with the user, returning the status is required
        return decoded["email"]

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=401, detail="Invalid token")
