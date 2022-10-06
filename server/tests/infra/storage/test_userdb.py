import pytest

from src.app.domain.user import CreateUserInput, User
from src.infra.storage.userdb import UserDBAdaptor


@pytest.mark.asyncio
async def test_create_user(userdb_adaptor: UserDBAdaptor):
    payload: CreateUserInput = {
        "email": "awesome_test_user@gmail.com",
        "name": "awesome test user",
        "profileUrl": "https://www.awesome_user.com/profile",
        "oauthInUse": {
            "type": "github",
            "token": "b95b37605c1a4cb82fd8a032e6541f6e08733745",
        },
    }
    result = await userdb_adaptor.create_user(payload)

    assert (type(result).__name__) is User.__name__
    assert result.email == payload["email"]
    assert result.name == payload["name"]
    assert result.profileUrl == payload["profileUrl"]


@pytest.mark.asyncio
async def test_read_user(userdb_adaptor: UserDBAdaptor, test_user_dataset):
    result = await userdb_adaptor.read_user(test_user_dataset[5]["id"])

    assert (type(result).__name__) is User.__name__
    assert result.id == test_user_dataset[5]["id"]
    assert result.email == test_user_dataset[5]["email"]


@pytest.mark.asyncio
async def test_read_user_null_case(userdb_adaptor: UserDBAdaptor):
    from uuid import uuid4

    assert await userdb_adaptor.read_user(uuid4()) == None


@pytest.mark.asyncio
async def test_read_user_by_email(userdb_adaptor: UserDBAdaptor, test_user_dataset):
    result = await userdb_adaptor.read_user_by_email(test_user_dataset[2]["email"])

    assert (type(result).__name__) is User.__name__
    assert result.id == test_user_dataset[2]["id"]
    assert result.email == test_user_dataset[2]["email"]


@pytest.mark.asyncio
async def test_read_user_by_email_null_case(userdb_adaptor: UserDBAdaptor):
    assert await userdb_adaptor.read_user_by_email("null_email@gmail.com") == None


@pytest.mark.asyncio
async def test_write_github_token(userdb_adaptor: UserDBAdaptor, test_user_dataset):
    new_token = "b456c2a3c88f7d28342eefcfe82aeb2354b96493"

    result = await userdb_adaptor.write_github_token(
        test_user_dataset[1]["email"], new_token
    )

    assert result == new_token
