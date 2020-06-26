import os
from pytest import fixture


def pytest_addoption(parser):
    """
    pytest command line parser to store command line arguments.

    return: None
    """

    parser.addoption("--env", action="store", default="stg", dest="env",
                     choices=['dev', 'stg', 'prod'])
    parser.addoption("--api", action="store", default="v1alpha1", dest="api",
                     choices=['v1alpha1'])
    parser.addoption("--auth", action="store", default="aaat", dest="auth",
                     choices=['aaa', 'aaat'])
    parser.addoption("--level", action="store", default='INFO', dest="level",
                     choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])


@fixture()
def env(request):
    return request.config.getoption("--env")


@fixture()
def api(request):
    return request.config.getoption("--api")


@fixture()
def auth(request):
    return request.config.getoption("--auth")


@fixture()
def level(request):
    return request.config.getoption("--level")
