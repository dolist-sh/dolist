import pytest

from uuid import uuid4
from time import time

from src.app.domain.user import User
from src.app.domain.mrepo import MonitoredRepo, ParsedComment
from src.app.interactors.mrepo import MonitoredRepoInteractor
from uuid import UUID
from typing import List

user_id = uuid4()
mrepo_id = uuid4()

MOCK_USER = User(
    id=user_id,
    type="admin",
    email="awesome_user@email.com",
    oauth=[{"type": "github", "token": "ee977806d7286510da8b9a7492ba58e2484c0ecc"}],
    profileUrl="https://www.awesomeprofile.com/profile",
    createdAt=int(time()),
)
MOCK_MREPOS: List[MonitoredRepo] = [
    MonitoredRepo(
        id=mrepo_id,
        name="repo_1",
        fullName="test_user/repo_1",
        defaultBranch="main",
        language="python",
        userId=user_id,
        provider="github",
        status="active",
        visibility="private",
        lastCommit="4015b57a143aec5156fd1444a017a32137a3fd0f",
        parsedComments=[
            ParsedComment(
                id=uuid4(),
                mrepoId=mrepo_id,
                title="test comment",
                type="TODO",
                status="Normal",
                commentStyle="oneline",
                fullComment=["test comment"],
                filePath="/src/main.py",
                lineNumber=10,
                createdAt=int(time()),
                lastUpdated=int(time()),
            ),
            ParsedComment(
                id=uuid4(),
                mrepoId=mrepo_id,
                title="second test comment",
                type="TODO",
                status="New",
                commentStyle="multiline",
                fullComment=[
                    "second test comment",
                    "this was created sometimes ago.",
                ],
                filePath="/src/main.py",
                lineNumber=20,
                createdAt=int(time()),
                lastUpdated=int(time()),
            ),
        ],
        createdAt=int(time()),
        lastUpdated=int(time()),
    ),
    MonitoredRepo(
        id=uuid4(),
        name="repo_2",
        fullName="test_user/repo_2",
        defaultBranch="main",
        language="python",
        userId=user_id,
        provider="github",
        status="active",
        visibility="private",
        createdAt=int(time()),
        lastUpdated=int(time()),
    ),
    MonitoredRepo(
        id=uuid4(),
        name="repo_3",
        fullName="test_user/repo_3",
        defaultBranch="main",
        language="javascript",
        userId=user_id,
        provider="github",
        status="active",
        visibility="private",
        createdAt=int(time()),
        lastUpdated=int(time()),
    ),
]


@pytest.fixture
def mock_read_user_by_email(monkeypatch, userdb):
    async def mock_func(email: str):
        return MOCK_USER if email == MOCK_USER.email else None

    monkeypatch.setattr(userdb, "read_user_by_email", mock_func)


@pytest.fixture
def mock_read_monitored_repos(monkeypatch, mrepodb):
    async def mock_func(user_id: UUID):
        return [
            repo
            for repo in MOCK_MREPOS
            if repo.userId == user_id and repo.status == "active"
        ]

    monkeypatch.setattr(mrepodb, "read_monitored_repos", mock_func)


@pytest.fixture
def mrepo_interactor(
    userdb, mrepodb, github_service, mock_read_user_by_email, mock_read_monitored_repos
):
    return MonitoredRepoInteractor(userdb, mrepodb, github_service)


@pytest.mark.asyncio
async def test_get_monitored_repos_success(mrepo_interactor: MonitoredRepoInteractor):
    result = await mrepo_interactor.execute_get_monitored_repos(
        "awesome_user@email.com"
    )

    assert len(result) == 3
    assert len(result[0].parsedComments) == 2
    assert type(result[0]).__name__ is MonitoredRepo.__name__


@pytest.mark.asyncio
async def test_get_monitored_repos_fail_invalid_email(
    mrepo_interactor: MonitoredRepoInteractor,
):
    with pytest.raises(ValueError) as exception:
        await mrepo_interactor.execute_get_monitored_repos("null_email@email.com")
        assert "unknown user" is str(exception.value)
