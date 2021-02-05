import pytest


def pytest_addoption(parser):
    parser.addoption("--username", action="store", default="")
    parser.addoption("--password", action="store", default="")


@pytest.fixture(scope="session")
def username(request):
    return request.config.getoption("--username")


@pytest.fixture(scope="session")
def password(request):
    return request.config.getoption("--password")
