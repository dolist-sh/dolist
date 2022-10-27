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

from src.app.interactors.mrepo import (
    GetMonitoredRepoUseCase,
    GetMonitoredReposUseCase,
    WriteParseResultUseCase,
    AddMonitoredReposUseCase,
)


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


@pytest.fixture
def get_mrepo(userdb, mrepodb, github_service):
    return GetMonitoredRepoUseCase(userdb, mrepodb, github_service)


@pytest.fixture
def get_mrepos(userdb, mrepodb, github_service):
    return GetMonitoredReposUseCase(userdb, mrepodb, github_service)


@pytest.fixture
def write_parse_result(userdb, mrepodb, github_service):
    return WriteParseResultUseCase(userdb, mrepodb, github_service)


@pytest.fixture
def add_mrepos(userdb, mrepodb, github_service):
    return AddMonitoredReposUseCase(
        userdb=userdb, mrepodb=mrepodb, github=github_service
    )
