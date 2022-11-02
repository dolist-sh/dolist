import pytest

from src.app.domain.mrepo import MonitoredRepo, CreateMonitoredReposInput
from src.infra.storage.mrepodb import MonitoredRepoDBAccess


@pytest.mark.asyncio
async def test_create_monitored_repo(mrepodb: MonitoredRepoDBAccess, test_user_dataset):
    payload: CreateMonitoredReposInput = {
        "name": "new_repo",
        "fullName": "octocat/new_repo",
        "defaultBranch": "main",
        "language": "python",
        "url": "https://www.awesomebranch.com/octocat/new_repo",
        "provider": "github",
        "visibility": "public",
    }

    result = await mrepodb.create_monitored_repo(payload, test_user_dataset[0]["id"])

    assert (type(result).__name__) is MonitoredRepo.__name__
    assert result.userId == test_user_dataset[0]["id"]
    assert result.name == payload["name"]
    assert result.fullName == payload["fullName"]


@pytest.mark.asyncio
async def test_read_monitored_repo_by_fullname(
    mrepodb: MonitoredRepoDBAccess, test_mrepo_dataset
):
    result = await mrepodb.read_monitored_repo_by_fullname(
        test_mrepo_dataset[1]["fullName"], test_mrepo_dataset[1]["provider"]
    )

    assert (type(result).__name__) is MonitoredRepo.__name__
    assert result.id == test_mrepo_dataset[1]["id"]
    assert result.name == test_mrepo_dataset[1]["name"]


@pytest.mark.asyncio
async def test_null_case_read_monitored_repo_by_fullname(
    mrepodb: MonitoredRepoDBAccess,
):
    result = await mrepodb.read_monitored_repo_by_fullname("randome_repo", "github")

    assert result is None


@pytest.mark.asyncio
async def test_read_monitored_repo(mrepodb: MonitoredRepoDBAccess, test_mrepo_dataset):
    result = await mrepodb.read_monitored_repo(test_mrepo_dataset[1]["id"])

    assert (type(result).__name__) is MonitoredRepo.__name__
    assert result.id == test_mrepo_dataset[1]["id"]
    assert result.name == test_mrepo_dataset[1]["name"]
    assert len(result.parsedComments) == 10


@pytest.mark.asyncio
async def test_null_case_read_monitored_repo(mrepodb: MonitoredRepoDBAccess):
    from uuid import uuid4

    result = await mrepodb.read_monitored_repo(uuid4())

    assert result is None


@pytest.mark.asyncio
async def test_read_monitored_repos(
    mrepodb: MonitoredRepoDBAccess, test_user_dataset, test_mrepo_dataset
):
    result = await mrepodb.read_monitored_repos(
        test_user_dataset[1]["id"], "active", 100, 0
    )

    mrepo_with_comments = list(
        filter(
            lambda repo: True if repo.id == test_mrepo_dataset[1]["id"] else False,
            result,
        )
    )

    assert type(result[-1]).__name__ == MonitoredRepo.__name__
    assert len(result) == 5
    assert (
        result[0].userId == test_user_dataset[1]["id"]
    )  # All test mrepo datasets should have been created this user_id.
    assert (
        len(mrepo_with_comments[0].parsedComments) == 10
    )  # There is only one mrepo with parsedComments and length should be 10.


@pytest.mark.asyncio
async def test_read_monitored_repos_nullcase(mrepodb: MonitoredRepoDBAccess):
    from uuid import uuid4

    result = await mrepodb.read_monitored_repos(uuid4(), "active", 100, 0)

    assert len(result) == 0


@pytest.mark.asyncio
async def test_create_parse_report(mrepodb: MonitoredRepoDBAccess, test_mrepo_dataset):
    mrepo_id = test_mrepo_dataset[3]["id"]
    payload = {
        "parseResult": [
            {
                "type": "TODO",
                "commentStyle": "oneline",
                "title": "test comment - 1",
                "fullComment": ["test comment - 1"],
                "path": "/path/file.py",
                "lineNumber": 10,
            },
            {
                "type": "TODO",
                "commentStyle": "oneline",
                "title": "test comment - 2",
                "fullComment": ["test comment - 2"],
                "path": "/path/file_1.py",
                "lineNumber": 14,
            },
            {
                "type": "TODO",
                "commentStyle": "oneline",
                "title": "test comment - 5",
                "fullComment": ["test comment - 5"],
                "path": "/path/file_5.py",
                "lineNumber": 20,
            },
        ],
    }

    dummy_commit = "bc62999e99df7576af9381d69d52d0c59f9bbe14"

    await mrepodb.create_parse_report(dummy_commit, payload, mrepo_id)
    mrepo = await mrepodb.read_monitored_repo(test_mrepo_dataset[3]["id"])

    assert mrepo.lastCommit == dummy_commit


""" 
    Testing private methods
"""

# fmt: off
def test_find_resolved_comments(mrepodb: MonitoredRepoDBAccess):

    dummy_parsed_comments = [
        {
            "id": "85136c79cbf9fe36bb9d05d0639c70c265c18d37",
            "title": "Refactor the methods",
        },
        {
            "id": "535e775e273d93844920103bad8e8d709639f7f9", 
            "title": "Add test"
        },
        {
            "id": "bd073433caebf2f73f9440ab4815f665d84fd1b8",
            "title": "Improve performance",
        },
    ]

    dummy_comments_from_db = [
        {
            "id": "85136c79cbf9fe36bb9d05d0639c70c265c18d37",
            "title": "Refactor the methods",
        },
        {
            "id": "535e775e273d93844920103bad8e8d709639f7f9", 
            "title": "Add test"
        },
        {
            "id": "bd073433caebf2f73f9440ab4815f665d84fd1b8",
            "title": "Improve performance",
        },
        {
            "id": "b56e396f011f1159207e1a33453db14fdc741f0c", 
            "title": "Resolved comment"
        },
        {
            "id": "df211ccdd94a63e0bcb9e6ae427a249484a49d60",
            "title": "Resolved comment - 2",
        },
    ]
    resolved = mrepodb._find_resolved_comments(dummy_comments_from_db, dummy_parsed_comments)

    assert len(resolved) == 2


def test_find_new_comments(mrepodb: MonitoredRepoDBAccess):
    dummy_parsed_comments = [
        {
            "id": "85136c79cbf9fe36bb9d05d0639c70c265c18d37",
            "title": "Refactor the methods",
        },
        {
            "id": "535e775e273d93844920103bad8e8d709639f7f9", 
            "title": "Add test"
        },
        {
            "id": "bd073433caebf2f73f9440ab4815f665d84fd1b8",
            "title": "Improve performance",
        },
                {
            "id": "b56e396f011f1159207e1a33453db14fdc741f0c", 
            "title": "New comment"
        },
        {
            "id": "df211ccdd94a63e0bcb9e6ae427a249484a49d60",
            "title": "New comment - 2",
        },
    ]

    dummy_comments_from_db = [
        {
            "id": "85136c79cbf9fe36bb9d05d0639c70c265c18d37",
            "title": "Refactor the methods",
        },
        {
            "id": "535e775e273d93844920103bad8e8d709639f7f9", 
            "title": "Add test"
        },
        {
            "id": "bd073433caebf2f73f9440ab4815f665d84fd1b8",
            "title": "Improve performance",
        },
    ]
    new = mrepodb._find_new_comments(dummy_comments_from_db, dummy_parsed_comments)

    assert len(new) == 2
# fmt: on
