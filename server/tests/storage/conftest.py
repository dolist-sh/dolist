import pytest

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

from src.infra.storage.model import (
    user_schema,
    monitored_repo_schema,
    parsed_comment_schema,
)

from src.infra.storage.mrepodb import MonitoredRepoDBAdaptor
from src.infra.storage.userdb import UserDBAdaptor

from .helpers import generate_test_user_dataset, generate_test_mrepo_dataset
from config import DB_HOST, DB_USER, DB_PWD


@pytest.fixture
def test_user_dataset():
    return generate_test_user_dataset(10)


@pytest.fixture
def test_mrepo_dataset():
    return generate_test_mrepo_dataset(5)


@pytest.fixture
def test_db_session(test_user_dataset, test_mrepo_dataset):

    engine = create_engine(f"postgresql://{DB_USER}:{DB_PWD}@{DB_HOST}:5432/testdb")

    if not database_exists(engine.url):
        create_database(engine)

    user_schema.create(engine, checkfirst=True)
    monitored_repo_schema.create(engine, checkfirst=True)
    parsed_comment_schema.create(engine, checkfirst=True)

    # Prepopulate DB with test dataset
    engine.execute(user_schema.insert(), test_user_dataset)
    engine.execute(monitored_repo_schema.insert(), test_mrepo_dataset)

    # Use yield instead of return to start the teardown process.
    yield engine

    # pytest will executes the following lines after test run.

    user_schema.drop(engine, checkfirst=True)
    monitored_repo_schema.drop(engine, checkfirst=True)
    parsed_comment_schema.drop(engine, checkfirst=True)

    drop_database(engine.url)


@pytest.fixture
def userdb_adaptor(test_db_session):
    return UserDBAdaptor(test_db_session, user_schema)


@pytest.fixture
def mrepodb_adaptor(test_db_session):
    import sqlalchemy
    from src.logger import logger

    return MonitoredRepoDBAdaptor(
        sqlalchemy,
        test_db_session,
        monitored_repo_schema,
        parsed_comment_schema,
        logger,
    )
