import json
import logging
import pytest
from plans_endpoint import plans_get, plans_post

'''
@pytest.fixture
def response(env, api, auth, level):
    """
    Fixture to get an api response to use in testing.

    :return: api response
    """
    response = plans_post(env, api, auth, level)

    return response
'''


def test_plans_post_status_code(env, api, auth, level):
    """
    Test to check status code of of plans post function

    return: None
    """

    response = plans_post(env, api, auth, level)
    assert response.status_code == 200


def test_plans_post_plan_id(env, api, auth, level):
    """
    Test to check that the plan id exists, is not empty and is a string

    return: None
    """

    response = plans_post(env, api, auth, level)
    json_response = response.json()

    assert 'plan_id' in json_response
    if 'plan_id' in json_response:
        id = json_response['plan_id']
    assert isinstance(id, str)
    assert id is not None


def test_plans_post_status_id(env, api, auth, level):
    """
    Test to check that the status id exists, is not empty and is a string

    return: None
    """

    response = plans_post(env, api, auth, level)
    json_response = response.json()

    assert 'status_id' in json_response
    if 'status_id' in json_response:
        id = json_response['status_id']
    assert isinstance(id, str)
    assert id is not None


def test_plans_post_created(env, api, auth, level):
    """
    Test to check that the created date exists, is not empty and is a string

    return: None
    """

    response = plans_post(env, api, auth, level)
    json_response = response.json()

    assert 'created' in json_response
    if 'created' in json_response:
        id = json_response['created']
    assert isinstance(id, str)
    assert id is not None


def test_plans_get_response_validation(env, api, auth, level):
    """
    Test to verify the fields are correct in a plans get response
    We will be validating the key exists, not NULL and correct type.

    return: None
    """

    response = plans_get(env, api, auth, level)
    json_response = response.json()

    assert response.status_code == 200

    for x in json_response:

        assert 'plan_id' in json_response[x]
        if 'plan_id' in json_response[x]:
            id = json_response['plan_id']
        assert isinstance(id, str)
        assert id is not None

        assert 'status_id' in json_response[x]
        if 'status_id' in json_response[x]:
            id = json_response['status_id']
        assert isinstance(id, str)
        assert id is not None

        assert 'created' in json_response[x]
        if 'created' in json_response[x]:
            id = json_response['created']
        assert isinstance(id, str)
        assert id is not None

        assert 'status' in json_response[x]
        if 'status' in json_response[x]:
            id = json_response['status']
        assert isinstance(id, str)
        assert id is not None

        assert 'result_location' in json_response[x]
        if 'result_location' in json_response[x]:
            id = json_response['result_location']
        assert isinstance(id, str)
        assert id is not None


def test_plans_get_response_at_least_one_returned(env, api, auth, level):
    """
    Test to verify at least status is returned.

    return: None
    """
    logger = logging.getLogger('api_testing')
    logger.setLevel(level)

    response = plans_get(env, api, auth, level)
    json_response = response.json()

    logger.info("Response Length: {0}".format(len(json_response)))

    assert response.status_code == 200
    assert len(json_response) >= 1


if __name__ == "__main__":
    test_plans_post_status_code()
    test_plans_post_plan_id()
    test_plans_post_status_id()
    test_plans_post_created()
