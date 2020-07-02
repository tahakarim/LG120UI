import json
import logging
import pytest
import random
from plans_endpoint import plans_get, plans_post, plans_get_by_id, \
    plans_get_status, plans_post_payload_exception
from requests_toolbelt.utils import dump
from statistics import median, stdev
from slack import post_message_to_slack


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


@pytest.mark.functionality
@pytest.mark.smoke
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


@pytest.mark.exception
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


@pytest.mark.functionality
@pytest.mark.smoke
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


@pytest.mark.functionality
@pytest.mark.smoke
def test_plans_get_response_at_least_one_returned(env, api, auth, level):
    """
    Test to verify at least one plan id is returned.

    return: None
    """

    logger = logging.getLogger('api_testing')
    logger.setLevel(level)

    response = plans_get(env, api, auth, level)
    json_response = response.json()

    logger.info("Response Length: {0}".format(len(json_response)))

    assert response.status_code == 200
    assert len(json_response) >= 1


@pytest.mark.functionality
@pytest.mark.smoke
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


@pytest.mark.exception
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


@pytest.mark.exception
def test_plans_get_by_invalid_non_guid_id(env, api, auth, level):
    """
    Test to validate that we get an error when passing in an invalid format for
    an ID

    return: None
    """
    response = plans_get_by_id(env, api, auth, level,
                               'spider-man_heart_gwen_stacey')

    assert response.status_code == 400


@pytest.mark.functionality
@pytest.mark.smoke
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


@pytest.mark.exception
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


@pytest.mark.exception
def test_plans_get_status_invalid_non_guid_id(env, api, auth, level):
    """
    Test to validate that we get an error when passing in an invalid formatted
    ID

    return: None
    """
    response = plans_get_status(env, api, auth, level,
                                'spider-man_heart_gwen_stacey')

    assert response.status_code == 400


@pytest.mark.functionality
@pytest.mark.smoke
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


@pytest.mark.exception
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


@pytest.mark.performance
def test_plans_get_response_performance(env, api, auth, level):
    """
    Test to validate the response time of GET /plans over
    multiple iterations.

    return: None
    """

    count = 1
    iterations = 2
    response_time_list = []

    while count <= iterations:
        response = plans_get(env, api, auth, level)

        # converting total_seconds to milliseconds and truncating decimal
        response_time_list.append(int(response.elapsed.total_seconds() * 1000))
        count += 1

    print("\nMinimum: {0}".format(min(response_time_list)))
    print("Maximum: {0}".format(max(response_time_list)))
    print("Average: {0}".format((sum(response_time_list)/len(response_time_list))))
    print(" Median: {0}".format(median(response_time_list)))
    print(" StdDev: {0:.2f}".format(stdev(response_time_list)))

    test_data = "Minimum: {0}\nMaximum: {1}\nAverage: {2}\n Median: {3}\n StdDev: {4:.2f}".format\
                                                    (min(response_time_list),
                                                    max(response_time_list),
                                                    sum(response_time_list) / len(response_time_list),
                                                    median(response_time_list),
                                                    stdev(response_time_list))


    post_message_to_slack(test_data, level)

    logger = logging.getLogger('api_testing')
    logger.setLevel(level)

    logger.debug(response_time_list)


if __name__ == "__main__":
    test_plans_post_status_code()
    test_plans_post_plan_id()
    test_plans_post_status_id()
    test_plans_post_created()
