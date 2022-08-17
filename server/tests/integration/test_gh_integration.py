import pytest, requests

from src.integration.github import (
    register_push_github_repos,
    RegisterPushGitHubRepoOutput,
)


@pytest.mark.asyncio
async def test_register_push_github_repos(monkeypatch):
    class MockResponse:
        def __init__(self, status_code: int):
            self.status_code = status_code

    def mock_post_res(host, headers, data):
        print(f"host: {host}, headers: {headers}, data: {data}")
        return MockResponse(status_code=204)

    monkeypatch.setattr(requests, "post", mock_post_res)

    res: RegisterPushGitHubRepoOutput = await register_push_github_repos(
        "mock_token", "test_repo"
    )
    assert res["status"] == "success"
