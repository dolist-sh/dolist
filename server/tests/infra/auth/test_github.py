import pytest, requests

from src.infra.auth.github import GitHubAuthAdaptor


class MockRequests:
    def __init__(self, status_code: int, data) -> None:
        self.status_code = status_code
        self.data = data

    def json(self):
        return self.data


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
        return MockRequests(201, mock_res)

    with monkeypatch.context() as m:
        m.setattr(requests, "post", mock_post)
        result = await github_auth_adaptor.get_github_access_token("mock_token")
        assert result == mock_res["access_token"]


# mock response from https://api.github.com/user

# mock response from https://api.github.com/user/emails
