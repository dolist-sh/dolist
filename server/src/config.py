from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_OAUTH_CLIENT_ID = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
GITHUB_OAUTH_CLIENT_SECRET = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
GITHUB_WEBHOOK_CALLBACK = os.environ.get("GITHUB_WEBHOOK_CALLBACK")

DB_HOST = "postgres" if os.environ.get("RUN_DOCKER") else "localhost"
DB_USER = os.environ.get("POSTGRES_USERNAME")
DB_PWD = os.environ.get("POSTGRES_PASSWORD")

JWT_SECRET = os.environ.get("JWT_SECRET")
ENV = os.environ.get("ENV")

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
