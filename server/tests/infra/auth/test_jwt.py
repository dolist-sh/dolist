import pytest

from src.infra.auth.jwt import JWTAdaptor, CreateMachineTokenInput, MachineToken, jwt


@pytest.fixture
def jwt_adaptor():
    return JWTAdaptor(jwt)


def test_issue_token(jwt_adaptor: JWTAdaptor):
    token = jwt_adaptor.issue_token("awesome_user@gmail.com")

    assert (type(token) is str) == True


def test_issue_machine_token(jwt_adaptor: JWTAdaptor):
    payload: CreateMachineTokenInput = {
        "audience": "worker",
        "grant_type": "client_credentials",
        "client_id": "009ca4b55b89633cd79f930d71df2d846d699d2d",
        "client_secret": "491b15b6b08f721376c22e06e640b5126d86da58",
    }

    machine_token = jwt_adaptor.issue_machine_token(payload)

    assert (type(machine_token) is MachineToken) == True
