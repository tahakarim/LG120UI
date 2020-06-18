import json
import logging
import pytest
import random
from plans_endpoint import plans_get, plans_post, plans_get_by_id, \
    plans_get_status, plans_post_payload_exception
from requests_toolbelt.utils import dump

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


def test_plans_post_response_validation(env, api, auth, level):
    """
    Test to verify the fields are correct in a plans post response
    We will be validating the key exists, not NULL and correct type.

    return: None
    """

    response = plans_post(env, api, auth, level)
    json_response = response.json()

    assert response.status_code == 200

    assert 'plan_id' in json_response
    if 'plan_id' in json_response:
        id = json_response['plan_id']
    assert isinstance(id, str)
    assert id is not None

    assert 'created_date' in json_response
    if 'created_date' in json_response:
        id = json_response['created_date']
    assert isinstance(id, str)
    assert id is not None


def test_plans_post_response_no_payload(env, api, auth, level):
    """
    Test to ensure an error is returned with an empty payload

    return: None
    """
    payload = '{}'

    response = plans_post_payload_exception(env, api, auth, level, payload)
    #json_response = response.json()

    assert response.status_code == 400

    # Validating the error message is not present
    #assert 'message' not in json_response


def test_plans_get_response_validation(env, api, auth, level):
    """
    Test to verify the fields are correct in a plans get response
    We will be validating the key exists, not NULL and correct type.

    return: None
    """

    response = plans_get(env, api, auth, level)
    json_response = response.json()

    assert response.status_code == 200

    for item in json_response:

        #print(item['plan_id'])

        assert 'plan_id' in item
        if 'plan_id' in item:
            id = item['plan_id']
        assert isinstance(id, str)
        assert id is not None

        assert 'field_id' in item
        if 'field_id' in item:
            id = item['field_id']
        assert isinstance(id, str)
        assert id is not None

        assert 'created_date' in item
        if 'created_date' in item:
            id = item['created_date']
        assert isinstance(id, str)
        assert id is not None

        assert 'updated_date' in item
        if 'updated_date' in item:
            id = item['updated_date']
        assert isinstance(id, str)
        assert id is not None

        assert 'is_complete' in item['status']
        if 'is_complete' in item['status']:
            id = item['status']['is_complete']
        assert isinstance(id, bool)
        assert id is not None

        assert 'updated_date' in item['status']
        if 'updated_date' in item['status']:
            id = item['status']['updated_date']
        assert isinstance(id, str)
        assert id is not None

        assert 'step_name' in item['status']
        if 'step_name' in item['status']:
            id = item['status']['step_name']
        assert isinstance(id, str)
        assert id is not None

        assert 'has_error' in item['status']
        if 'has_error' in item['status']:
            id = item['status']['has_error']
        assert isinstance(id, bool)
        assert id is not None

        # Validate no extra fields in response
        assert len(item) == 5

        # Validate no extra fields in status part of response
        assert len(item['status']) == 4


def test_plans_get_response_at_least_one_returned(env, api, auth, level):
    """
    Test to verify at least one status is returned.

    return: None
    """

    logger = logging.getLogger('api_testing')
    logger.setLevel(level)

    response = plans_get(env, api, auth, level)
    json_response = response.json()

    logger.info("Response Length: {0}".format(len(json_response)))

    assert response.status_code == 200
    assert len(json_response) >= 1


def test_plans_get_by_id_response_validation(env, api, auth, level):
    """
    Test to validate that we are returning one status and that it is
    the correct status

    return: None
    """
    response = plans_get(env, api, auth, level)
    json_response = response.json()

    assert response.status_code == 200

    plan_id = random.choice(json_response)['plan_id']

    # Request to get a single ID resposne
    response = plans_get_by_id(env, api, auth, level, plan_id)
    json_response = response.json()

    assert response.status_code == 200

    # Validating we get 1 response back
    assert type(json_response) is not list

    # Validating plan_id equals what was requested
    assert json_response['plan_id'] == plan_id


def test_plans_get_by_invalid_guid_id(env, api, auth, level):
    """
    Test to validate that we get an error when passing in an invalid ID

    return: None
    """
    response = plans_get_by_id(env, api, auth, level,
                               'acebdfac-ebdf-aceb-dfac-ebdfacebdfac')
    json_response = response.json()

    assert response.status_code == 404

    # Validating the error message
    assert json_response['message'] == 'Could not find a plan with plan id ' \
            'acebdfac-ebdf-aceb-dfac-ebdfacebdfac.'


def test_plans_get_by_invalid_non_guid_id(env, api, auth, level):
    """
    Test to validate that we get an error when passing in an invalid format for
    an ID

    return: None
    """
    response = plans_get_by_id(env, api, auth, level,
                               'spider-man_heart_gwen_stacey')

    assert response.status_code == 400


def test_plans_get_status_response_validation(env, api, auth, level):
    """
    Test to validate that we are returning one status and that it is
    the correct status

    return: None
    """
    response = plans_get(env, api, auth, level)
    json_response = response.json()

    assert response.status_code == 200

    # Grab a plan id and save off the status updated_date
    r_index = random.choice(json_response)
    plan_id = r_index['plan_id']
    status_updated_date = r_index['status']['updated_date']

    # Request to get a single ID resposne
    response = plans_get_status(env, api, auth, level, plan_id)
    json_response = response.json()

    assert response.status_code == 200

    # Validating we get 1 response back
    assert type(json_response) is not list

    # Validating plan_id equals what was requested
    assert json_response['updated_date'] == status_updated_date


def test_plans_get_status_invalid_guid_id(env, api, auth, level):
    """
    Test to validate that we get an error when passing in an invalid ID

    return: None
    """
    response = plans_get_status(env, api, auth, level,
                                'acebdfac-ebdf-aceb-dfac-ebdfacebdfac')
    json_response = response.json()

    assert response.status_code == 404

    # Validating the error message
    assert json_response['message'] == 'Could not find a status with the ' \
            'plan id acebdfac-ebdf-aceb-dfac-ebdfacebdfac'


def test_plans_get_status_invalid_non_guid_id(env, api, auth, level):
    """
    Test to validate that we get an error when passing in an invalid formatted
    ID

    return: None
    """
    response = plans_get_status(env, api, auth, level,
                                'spider-man_heart_gwen_stacey')

    assert response.status_code == 400


def test_plans_created_date_validation(env, api, auth, level):
    """
    Test to validate that the created_date is the same between POST and GET

    return: None
    """
    response = plans_post(env, api, auth, level)
    json_response = response.json()

    assert response.status_code == 200

    created_date = json_response['created_date']
    plan_id = json_response['plan_id']

    # Send a GET /plans by ID
    response = plans_get_by_id(env, api, auth, level, plan_id)
    json_response = response.json()

    assert response.status_code == 200

    assert json_response['plan_id'] == plan_id
    assert json_response['created_date'] == created_date


def test_plans_get_status_no_id(env, api, auth, level):
    """
    Test to validate that the created_date is the same between POST and GET

    return: None
    """

    # We are calling plans_get_by_id so we don't end up with /plans//status
    # in the URL.  Using this method, we will end up with /plans/status
    plan_id = "status"
    response = plans_get_by_id(env, api, auth, level, plan_id)

    # Left in on purpose
    print("\n" + response.url)

    assert response.status_code == 400


if __name__ == "__main__":
    test_plans_post_status_code()
    test_plans_post_plan_id()
    test_plans_post_status_id()
    test_plans_post_created()
