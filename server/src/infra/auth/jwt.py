import jwt
from datetime import datetime, timedelta, timezone
from app.domain.auth import CreateMachineTokenInput, MachineToken
from fastapi import Header, HTTPException

from config import JWT_SECRET, WORKER_OAUTH_CLIENT_ID, WORKER_OAUTH_CLIENT_SECRET
from logger import logger


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


def _verify_token_cred(token_claim) -> bool:
    result = True

    if (token_claim["client_id"] != WORKER_OAUTH_CLIENT_ID) or (
        token_claim["client_secret"] != WORKER_OAUTH_CLIENT_SECRET
    ):
        result = False

    return result


def verify_machine_token(Authorization: str = Header()) -> bool:
    try:
        token = Authorization.split(" ")[1]
        options = dict(
            verify_signature=True,
            require=["aud", "iss", "client_id", "client_secret", "exp"],
            verify_exp=True,
        )

        decoded = jwt.decode(
            token,
            JWT_SECRET,
            audience="worker",
            issuer="dolist_server",
            algorithms="HS256",
            options=options,
        )
        print(decoded)
        return _verify_token_cred(decoded)

    except Exception as e:
        logger.warning(f"Invalid machine token | {str(e)}")
        return False


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
