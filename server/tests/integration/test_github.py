import pytest, requests

from src.infra.integration.github import (
    get_github_repo_list,
    GetGitHubRepoListOutput,
    register_push_github_repo,
    RegisterPushGitHubRepoOutput,
)

from typing import List


@pytest.mark.asyncio
async def test_get_github_repos(monkeypatch):

    mock_data = ["object_1", "object_2"]

    class MockResponse:
        def __init__(self, status_code: int, data: List[str]) -> None:
            self.status_code = status_code
            self.data = data

        def json(self) -> List[str]:
            return self.data

    def mock_get_res(host, headers):
        print(f"host: {host}, headers: {headers}")
        return MockResponse(status_code=200, data=mock_data)

    monkeypatch.setattr(requests, "get", mock_get_res)

    res: GetGitHubRepoListOutput = await get_github_repo_list("mock_token")
    assert res["status"] == "success"
    assert res["data"] == mock_data


@pytest.mark.asyncio
async def test_register_push_github_repo(monkeypatch):
    class MockResponse:
        def __init__(self, status_code: int) -> None:
            self.status_code = status_code

    def mock_post_res(host, headers, data):
        print(f"host: {host}, headers: {headers}, data: {data}")
        return MockResponse(status_code=204)

    monkeypatch.setenv("GITHUB_WEBHOOK_CALLBACK", "http://dummy_callback", prepend=None)
    monkeypatch.setattr(requests, "post", mock_post_res)

    res: RegisterPushGitHubRepoOutput = await register_push_github_repo(
        "mock_token", "test_repo"
    )
    assert res["status"] == "success"
