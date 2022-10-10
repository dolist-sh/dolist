import pytest

from src.infra.integration.github import requests, GitHubService
from src.logger import logger

from tests.mocks import MockResponse


@pytest.fixture
def github_adaptor():
    return GitHubService(requests, logger)


@pytest.mark.asyncio
async def test_get_github_repo(monkeypatch, github_adaptor: GitHubService):
    # https://docs.github.com/en/rest/repos/repos#get-a-repository

    # Some fields are omitted to keep the code brief, refer to GitHub doc for full example response.
    mock_res = {
        "id": 1296269,
        "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
        "name": "Hello-World",
        "full_name": "octocat/Hello-World",
        "owner": {
            "login": "octocat",
            "id": 1,
            "node_id": "MDQ6VXNlcjE=",
            "avatar_url": "https://github.com/images/error/octocat_happy.gif",
            "gravatar_id": "",
            "url": "https://api.github.com/users/octocat",
            "html_url": "https://github.com/octocat",
            "followers_url": "https://api.github.com/users/octocat/followers",
            "following_url": "https://api.github.com/users/octocat/following{/other_user}",
            "repos_url": "https://api.github.com/users/octocat/repos",
            "events_url": "https://api.github.com/users/octocat/events{/privacy}",
            "received_events_url": "https://api.github.com/users/octocat/received_events",
            "type": "User",
            "site_admin": False,
        },
        "private": False,
        "html_url": "https://github.com/octocat/Hello-World",
        "description": "This your first repo!",
        "fork": False,
        "url": "https://api.github.com/repos/octocat/Hello-World",
        "homepage": "https://github.com",
        "language": None,
        "forks_count": 9,
        "forks": 9,
        "stargazers_count": 80,
        "watchers_count": 80,
        "watchers": 80,
        "size": 108,
        "default_branch": "master",
        "open_issues_count": 0,
        "open_issues": 0,
        "is_template": False,
        "topics": ["octocat", "atom", "electron", "api"],
        "has_issues": True,
        "has_downloads": True,
        "archived": False,
        "disabled": False,
        "visibility": "public",
        "pushed_at": "2011-01-26T19:06:43Z",
        "created_at": "2011-01-26T19:01:12Z",
        "updated_at": "2011-01-26T19:14:43Z",
        "permissions": {"pull": True, "push": False, "admin": False},
        "allow_rebase_merge": True,
    }

    def mock_get(host, headers):
        print(f"host: {host}, headers: {headers}")
        return MockResponse(200, mock_res)

    with monkeypatch.context() as m:
        m.setattr(requests, "get", mock_get)

        result = await github_adaptor.get_github_repo(
            "c371618c76a4d9c0ec463f17597be01c1db528a4",
            mock_res["full_name"],
        )
        assert result["status"] == "success"
        assert result["data"] == mock_res


@pytest.mark.asyncio
async def test_get_github_repo_list(monkeypatch, github_adaptor: GitHubService):
    # https://docs.github.com/en/rest/repos/repos#list-repositories-for-the-authenticated-user

    mock_res = [
        {
            "id": 1296269,
            "node_id": "MDEwOlJlcG9zaXRvcnkxMjk2MjY5",
            "name": "Hello-World",
            "full_name": "octocat/Hello-World",
            "owner": {
                "login": "octocat",
                "id": 1,
                "node_id": "MDQ6VXNlcjE=",
                "avatar_url": "https://github.com/images/error/octocat_happy.gif",
                "gravatar_id": "",
                "url": "https://api.github.com/users/octocat",
                "html_url": "https://github.com/octocat",
                "repos_url": "https://api.github.com/users/octocat/repos",
                "events_url": "https://api.github.com/users/octocat/events{/privacy}",
                "received_events_url": "https://api.github.com/users/octocat/received_events",
                "type": "User",
                "site_admin": False,
            },
            "private": False,
            "html_url": "https://github.com/octocat/Hello-World",
            "description": "This your first repo!",
            "fork": False,
            "url": "https://api.github.com/repos/octocat/Hello-World",
            "archive_url": "https://api.github.com/repos/octocat/Hello-World/{archive_format}{/ref}",
            "assignees_url": "https://api.github.com/repos/octocat/Hello-World/assignees{/user}",
            "homepage": "https://github.com",
            "language": None,
            "forks_count": 9,
            "stargazers_count": 80,
            "watchers_count": 80,
            "size": 108,
            "default_branch": "master",
            "open_issues_count": 0,
            "is_template": True,
            "topics": ["octocat", "atom", "electron", "api"],
            "visibility": "public",
            "pushed_at": "2011-01-26T19:06:43Z",
            "created_at": "2011-01-26T19:01:12Z",
            "updated_at": "2011-01-26T19:14:43Z",
            "subscribers_count": 42,
            "network_count": 0,
            "license": {
                "key": "mit",
                "name": "MIT License",
                "url": "https://api.github.com/licenses/mit",
                "spdx_id": "MIT",
                "node_id": "MDc6TGljZW5zZW1pdA==",
                "html_url": "https://github.com/licenses/mit",
            },
            "forks": 1,
            "open_issues": 1,
            "watchers": 1,
        }
    ]

    def mock_get(host, headers):
        print(f"host: {host}, headers: {headers}")
        return MockResponse(200, mock_res)

    with monkeypatch.context() as m:
        m.setattr(requests, "get", mock_get)

        result = await github_adaptor.get_github_repo_list(
            "c371618c76a4d9c0ec463f17597be01c1db528a4",
        )
        assert result["status"] == "success"
        assert result["data"] == mock_res


@pytest.mark.asyncio
async def test_get_github_repo_last_commit(monkeypatch, github_adaptor: GitHubService):
    mock_res = {
        "name": "main",
        "commit": {
            "sha": "7fd1a60b01f91b314f59955a4e4d4e80d8edf11d",
            "node_id": "MDY6Q29tbWl0MTI5NjI2OTo3ZmQxYTYwYjAxZjkxYjMxNGY1OTk1NWE0ZTRkNGU4MGQ4ZWRmMTFk",
            "commit": {
                "author": {
                    "name": "The Octocat",
                    "email": "octocat@nowhere.com",
                    "date": "2012-03-06T23:06:50Z",
                },
                "committer": {
                    "name": "The Octocat",
                    "email": "octocat@nowhere.com",
                    "date": "2012-03-06T23:06:50Z",
                },
                "message": "Merge pull request #6 from Spaceghost/patch-1\n\nNew line at end of file.",
                "tree": {
                    "sha": "b4eecafa9be2f2006ce1b709d6857b07069b4608",
                    "url": "https://api.github.com/repos/octocat/Hello-World/git/trees/b4eecafa9be2f2006ce1b709d6857b07069b4608",
                },
                "url": "https://api.github.com/repos/octocat/Hello-World/git/commits/7fd1a60b01f91b314f59955a4e4d4e80d8edf11d",
                "comment_count": 77,
            },
        },
    }

    def mock_get_res(host, headers):
        print(f"host: {host}, headers: {headers}")
        return MockResponse(200, mock_res)

    with monkeypatch.context() as m:
        m.setattr(requests, "get", mock_get_res)

        result = await github_adaptor.get_github_repo_last_commit(
            "c371618c76a4d9c0ec463f17597be01c1db528a4", "/owner/octocat", "main"
        )

        assert result["status"] == "success"
        assert result["commit"] == mock_res["commit"]["sha"]


@pytest.mark.asyncio
async def test_register_push_github_repo(monkeypatch, github_adaptor: GitHubService):
    def mock_post_res(host, headers, data):
        print(f"host: {host}, headers: {headers}, data: {data}")
        return MockResponse(status_code=204, data=data)

    with monkeypatch.context() as m:
        m.setenv("GITHUB_WEBHOOK_CALLBACK", "http://dummy_callback", prepend=None)
        m.setattr(requests, "post", mock_post_res)

        result = await github_adaptor.register_push_github_repo(
            "c371618c76a4d9c0ec463f17597be01c1db528a4", "test_repo"
        )
        assert result["status"] == "success"
