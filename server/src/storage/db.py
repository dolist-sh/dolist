from sqlalchemy import create_engine
from sqlalchemy.utils import database_exists, create_database

from config import DB_HOST, DB_USER, DB_PWD

engine = create_engine(f"postgresql://{DB_USER}:{DB_PWD}@{DB_HOST}:5432/dolistdb")

if not database_exists(engine.url):
    create_database(engine.url)
