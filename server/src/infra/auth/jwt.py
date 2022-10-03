import jwt
from datetime import datetime, timedelta, timezone
from app.domain.auth import CreateMachineTokenInput, MachineToken
from config import JWT_SECRET


def issue_token(email: str) -> str:
    payload = {
        "email": email,
        "exp": datetime.now(tz=timezone.utc) + timedelta(days=30),
    }
    encoded = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    return encoded


def issue_machine_token(input: CreateMachineTokenInput) -> MachineToken:
    exp_at = datetime.now(tz=timezone.utc) + timedelta(days=30)

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
