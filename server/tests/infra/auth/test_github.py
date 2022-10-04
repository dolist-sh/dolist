import pytest, requests

from src.infra.auth.github import GitHubAuthAdaptor
from tests.mocks import MockResponse


@pytest.fixture
def github_auth_adaptor():
    return GitHubAuthAdaptor(requests)


@pytest.mark.asyncio
async def test_get_github_access_token(monkeypatch, github_auth_adaptor):
    # https://docs.github.com/en/developers/apps/building-oauth-apps/authorizing-oauth-apps#response
    mock_res = {
        "access_token": "gho_16C7e42F292c6912E7710c838347Ae178B4a",
        "scope": "repo,gist",
        "token_type": "bearer",
    }

    def mock_post(host, headers, params):
        print(f"host: {host}, headers: {headers}, params: {params}")
        return MockResponse(201, mock_res)

    with monkeypatch.context() as m:
        m.setattr(requests, "post", mock_post)
        result = await github_auth_adaptor.get_github_access_token(
            "c371618c76a4d9c0ec463f17597be01c1db528a4"
        )
        assert result == mock_res["access_token"]


@pytest.mark.asyncio
async def test_get_github_user(monkeypatch, github_auth_adaptor):
    # https://docs.github.com/en/rest/users/users#get-the-authenticated-user

    mock_res = {
        "login": "octocat",
        "id": 1,
        "node_id": "MDQ6VXNlcjE=",
        "avatar_url": "https://github.com/images/error/octocat_happy.gif",
        "gravatar_id": "",
        "url": "https://api.github.com/users/octocat",
        "html_url": "https://github.com/octocat",
        "followers_url": "https://api.github.com/users/octocat/followers",
        "following_url": "https://api.github.com/users/octocat/following{/other_user}",
        "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
        "organizations_url": "https://api.github.com/users/octocat/orgs",
        "repos_url": "https://api.github.com/users/octocat/repos",
        "events_url": "https://api.github.com/users/octocat/events{/privacy}",
        "received_events_url": "https://api.github.com/users/octocat/received_events",
        "type": "User",
        "site_admin": False,
        "name": "monalisa octocat",
        "company": "GitHub",
        "blog": "https://github.com/blog",
        "location": "San Francisco",
        "email": "octocat@github.com",
        "hireable": False,
        "bio": "There once was...",
        "twitter_username": "monatheoctocat",
        "public_repos": 2,
        "public_gists": 1,
        "followers": 20,
        "following": 0,
        "created_at": "2008-01-14T04:33:35Z",
        "updated_at": "2008-01-14T04:33:35Z",
        "private_gists": 81,
        "total_private_repos": 100,
        "owned_private_repos": 100,
        "disk_usage": 10000,
        "collaborators": 8,
        "two_factor_authentication": True,
        "plan": {
            "name": "Medium",
            "space": 400,
            "private_repos": 20,
            "collaborators": 0,
        },
    }

    def mock_get(host, headers):
        print(f"host: {host}, headers: {headers}")
        return MockResponse(200, mock_res)

    with monkeypatch.context() as m:
        m.setattr(requests, "get", mock_get)
        result = await github_auth_adaptor.get_github_user(
            "0cc89a63a781058d1babcc2a018b65dc830cec84"
        )
        assert result == mock_res


@pytest.mark.asyncio
async def test_get_github_user_email(monkeypatch, github_auth_adaptor):
    # https://docs.github.com/en/rest/users/emails#list-email-addresses-for-the-authenticated-userw

    mock_res = [
        {
            "email": "octocat@github.com",
            "verified": True,
            "primary": True,
            "visibility": "public",
        }
    ]

    def mock_get(host, auth):
        print(f"host: {host}, headers: {auth}")
        return MockResponse(200, mock_res)

    with monkeypatch.context() as m:
        m.setattr(requests, "get", mock_get)
        result = await github_auth_adaptor.get_github_user_email(
            "octocat", "0cc89a63a781058d1babcc2a018b65dc830cec84"
        )
        assert result == mock_res[0]["email"]
