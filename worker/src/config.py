from dotenv import load_dotenv
import os

load_dotenv()

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")

WORKER_OAUTH_CLIENT_ID = os.environ.get("WORKER_OAUTH_CLIENT_ID")
WORKER_OAUTH_CLIENT_SECRET = os.environ.get("WORKER_OAUTH_CLIENT_SECRET")

JWT_SECRET = os.environ.get("JWT_SECRET")

SERVER_HOST = (
    "http://server:8080" if os.environ.get("RUN_DOCKER") else "http://localhost:8080"
)
