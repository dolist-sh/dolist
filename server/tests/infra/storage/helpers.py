from uuid import uuid4
from time import time
import hashlib


def generate_test_user_dataset(size: int = 100):
    """
    Generate n users to save in the test database
    if argument is not given, generate 100 records
    """
    result = []

    for n in range(1, size + 1):
        num_in_str = str(n)

        sha_val = hashlib.sha1(f"random_string_{num_in_str}".encode()).hexdigest()

        payload = dict(
            id=uuid4(),
            type="admin",
            email=f"test_email_{num_in_str}@test.com",
            name=f"test_user_{num_in_str}",
            profileUrl=f"https://example.com/profile_pic_{num_in_str}.png",
            oauth=[{"type": "github", "token": sha_val}],
            createdAt=int(time()),
        )

        result.append(payload)

    return result


def generate_test_mrepo_dataset(user_id, size: int = 100):
    """
    Generate n monitored repos to save in the test database
    if argument is not given, generate 100 records
    """
    result = []

    for n in range(1, size + 1):
        num_in_str = str(n)

        mrepo_id = uuid4()
        sha_val = hashlib.sha1(f"random_string_{num_in_str}".encode()).hexdigest()

        payload = dict(
            id=mrepo_id,
            name=f"repo_{num_in_str}",
            fullName=f"test_user/repo_{num_in_str}",
            defaultBranch="main",
            language="python",
            userId=user_id,
            provider="github",
            status="active",
            visibility="private",
            lastCommit=sha_val,
            createdAt=int(time()),
            lastUpdated=int(time()),
        )

        result.append(payload)

    return result


def generate_test_parsed_comments_dataset(mrepo_id, size: int = 100):
    """
    Generate n parsed_comments to save in the test database
    if argument is not given, generate 100 records
    """
    result = []

    for n in range(1, size + 1):
        num_in_str = str(n)

        payload = dict(
            id=uuid4(),
            mrepoId=mrepo_id,
            title=f"test comment - {num_in_str}",
            type="TODO",
            status="Normal",
            commentStyle="oneline",
            fullComment=[f"test comment - {num_in_str}"],
            filePath="/src/main.py",
            lineNumber=10,
            createdAt=int(time()),
            lastUpdated=int(time()),
        )

        result.append(payload)

    return result
