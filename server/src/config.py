from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_OAUTH_CLIENT_ID = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
GITHUB_OAUTH_CLIENT_SECRET = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")

DB_HOST = "postgres" if os.environ.get("RUN_DOCKER") else "localhost"
DB_USER = os.environ.get("POSTGRES_USERNAME")
DB_PWD = os.environ.get("POSTGRES_PASSWORD")

JWT_SECRET = os.environ.get("JWT_SECRET")
