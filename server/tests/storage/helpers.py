from uuid import uuid4
from time import time


def generate_test_user_dataset(size: int = 100):
    """
    Generate n users to save in the test database
    if argument is not given, generate 100 records
    """
    result = []

    for n in range(1, size + 1):
        num_in_str = str(n)

        payload = dict(
            id=uuid4(),
            type="admin",
            podcastTitle=f"test_email_{num_in_str}@test.com",
            name=f"test_user_{num_in_str}",
            profileUrl=f"https://example.com/profile_pic_{num_in_str}.png",
            oauth=[],
            createdAt=int(time()),
        )

        result.append(payload)

    return result


def generate_test_mrepo_dataset(size: int = 100):
    """
    Generate n monitored repos to save in the test database
    if argument is not given, generate 100 records
    """
    result = []

    for n in range(1, size + 1):
        num_in_str = str(n)

        payload = dict(
            id=uuid4(),
            name=f"mrepo_{num_in_str}",
            fullName=f"test/mrepo{num_in_str}",
            defaultBranch="main",
            userId=uuid4(),
            provider="github",
            visibility="public",
            status="active",
            createdAt=int(time()),
            lastUpdated=int(time()),
        )

        result.append(payload)

    return result
