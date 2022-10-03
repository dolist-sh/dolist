from fastapi import Request, Header, HTTPException
from logger import logger
from config import JWT_SECRET, WORKER_OAUTH_CLIENT_ID, WORKER_OAUTH_CLIENT_SECRET
import json, jwt


async def get_json_body(request: Request):
    body = await request.body()
    return json.loads(body)


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
        return _verify_token_cred(decoded)

    except Exception as e:
        logger.warning(f"Invalid machine token | {str(e)}")
        return False


def get_email_from_token(auth_header: str = Header()) -> str:
    try:
        token = auth_header.split(" ")[1]
        options = dict(verify_signature=True, require=["email", "exp"], verify_exp=True)

        decoded = jwt.decode(token, JWT_SECRET, algorithms="HS256", options=options)
        # TODO: Should check if the email is associated with the user, returning the status is required
        return decoded["email"]

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
