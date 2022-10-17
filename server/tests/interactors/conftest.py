import pytest, sqlalchemy, requests

from src.infra.storage.db import engine
from src.infra.storage.model import (
    parsed_comment_schema,
    user_schema,
    monitored_repo_schema,
)
from src.infra.storage.mrepodb import MonitoredRepoDBAccess
from src.infra.storage.userdb import UserDBAccess
from src.infra.integration.github import GitHubService
from src.logger import logger


@pytest.fixture
def mrepodb():
    return MonitoredRepoDBAccess(
        sqlalchemy, engine, monitored_repo_schema, parsed_comment_schema, logger
    )


@pytest.fixture
def userdb():
    return UserDBAccess(engine, user_schema)


@pytest.fixture
def github_service():
    return GitHubService(requests, logger)
