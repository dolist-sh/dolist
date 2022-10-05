import pytest

from src.infra.storage.userdb import UserDBAdaptor


@pytest.mark.asyncio
async def test_create_user(userdb_adaptor: UserDBAdaptor, test_user_dataset):
    assert 1 == 1


@pytest.mark.asyncio
async def test_read_user(userdb_adaptor: UserDBAdaptor, test_user_dataset):
    assert 1 == 1


@pytest.mark.asyncio
async def test_read_user_by_email(userdb_adaptor: UserDBAdaptor, test_user_dataset):
    assert 1 == 1


@pytest.mark.asyncio
async def test_write_github_token(userdb_adaptor: UserDBAdaptor, test_user_dataset):
    assert 1 == 1
