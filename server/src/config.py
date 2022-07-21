from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_OAUTH_CLIENT_ID = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
GITHUB_OAUTH_CLIENT_SECRET = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
GITHUB_OAUTH_REDIRECT_URI = os.environ.get("GITHUB_OAUTH_REDIRECT_URI")
GITHUB_OAUTH_CONFIRM_URI = os.environ.get("GITHUB_OAUTH_CONFIRM_URI")

DB_HOST = "localhost"
DB_USER =  os.environ.get("POSTGRES_USERNAME")
DB_PWD = os.environ.get("POSTGRES_PASSWORD")
