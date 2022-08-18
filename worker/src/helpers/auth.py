import requests, json
from config import WORKER_OAUTH_CLIENT_ID, WORKER_OAUTH_CLIENT_SECRET, SERVER_HOST
from helpers.logger import logger


def get_auth_token():
    try:
        payload = {
            "audience": "worker",
            "grant_type": "client_credentials",
            "client_id": WORKER_OAUTH_CLIENT_ID,
            "client_secret": WORKER_OAUTH_CLIENT_SECRET,
        }
        res = requests.post(f"{SERVER_HOST}/auth/worker", data=json.dumps(payload))

        token = res.json()
        print("Updated token from the post call")
        print(token)
        return token
    except Exception as e:
        logger.critical(f"Authentication request has failed | {str(e)}")
        raise e
