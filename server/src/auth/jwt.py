import jwt
from fastapi import Header, HTTPException
from config import JWT_SECRET
from datetime import datetime, timedelta, timezone

from domain.auth import CreateMachineTokenInput, MachineToken


def issue_token(email: str) -> str:
    payload = {
        "email": email,
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=30),
    }
    encoded = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return encoded


def issue_machine_token(input: CreateMachineTokenInput) -> MachineToken:
    exp_at = datetime.now(tz=timezone.utc) + timedelta(days=30)
    print(exp_at)

    payload = {
        "aud": input["audience"],
        "iss": "dolist_server",
        "client_id": input["client_id"],
        "client_secret": input["client_secret"],
        "exp": exp_at,
    }
    access_token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return MachineToken(
        token_type="Bearer", access_token=access_token, expires_at=exp_at
    )


def get_email_from_token(Authorization: str = Header()) -> str:
    try:

        token = Authorization.split(" ")[1]
        options = dict(verify_signature=True, require=["email", "exp"], verify_exp=True)

        decoded = jwt.decode(token, JWT_SECRET, algorithms="HS256", options=options)
        # TODO: Should check if the email is associated with the user, returning the status is required
        return decoded["email"]

    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=401, detail="Invalid token")
