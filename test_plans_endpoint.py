import json
import logging
import pytest
import random
import config
from plans_endpoint import plans_get, plans_get_by_id, plans_get_status, plans_post_payload
from requests_toolbelt.utils import dump
from statistics import median, stdev
from slack import post_message_to_slack
from copy import deepcopy
from time import sleep


@pytest.mark.functionality
@pytest.mark.smoke
def test_plans_post_response_validation(env, api, auth, level):
    """
    Test to verify the fields are correct in a plans post response
    We will be validating the key exists, not NULL and correct type.

    return: None
    """
    payload = deepcopy(config.payload)
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
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
def test_plans_post_missing_field_key(env, api, auth, level):
    """
        Test to verify we receive a 400 status if the field data is missing

        return: None
        """

    payload = deepcopy(config.payload)
    del payload['field']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_constraints_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the constraints data is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['constraints']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_constraints_payload(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the constraints payload is missing

    return: None
    """
    payload = deepcopy(config.payload)
    payload['constraints'] = []
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_field_id_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field_id data is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field_id']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_is_ctf_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the is_ctf data is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['is_ctf']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_headland_width_optimized_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the headland_width_optimized data is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['headland_width_optimized']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_headland_width_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the headland_width data is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['headland_width']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_constraints_width_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the width data is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['constraints'][0]['width']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_constraints_priority_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the priority data is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['constraints'][0]['priority']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_constraints_turning_radius_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the turning_radius data is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['constraints'][0]['turning_radius']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_constraints_ramp_up_distance_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the ramp_up_distance data is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['constraints'][0]['ramp_up_distance']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_constraints_ramp_down_distance_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the ramp_down_distance data is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['constraints'][0]['ramp_down_distance']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.skip(reason="deprecated on July 14 2020")
def test_plans_post_missing_field_name_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the name data is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field']['name']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_field_boundary_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the boundary data is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field']['boundary']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_field_boundary_boundary_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the boundary data is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field']['boundary']['boundary']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_field_boundary_boundary_lat_long_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if an empty boundary payload data is sent

    return: None
    """
    payload = deepcopy(config.payload)
    payload['field']['boundary']['boundary'] = []
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_field_gates_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the gates key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field']['gates']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_field_gates_lat_long_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the gates data is empty

    return: None
    """
    payload = deepcopy(config.payload)
    payload['field']['gates'] = []
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_field_gates_point_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the point key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field']['gates'][0]['point']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_field_gates_point_lat_long_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the point data is empty

    return: None
    """
    payload = deepcopy(config.payload)
    payload['field']['gates'][0]['point'] = []
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_field_obstacles_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the obstacles key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field']['obstacles']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_field_obstacles_lat_long_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the obstacles data is empty

    return: None
    """
    payload = deepcopy(config.payload)
    payload['field']['obstacles'] = []
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_row_direction_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the row_direction data is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['row_direction']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_field_soil_type_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the soil type key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field']['soil_type']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_row_direction_lat_long_key(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the row_direction data is empty

    return: None
    """
    payload = deepcopy(config.payload)
    payload['row_direction'] = []
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_missing_key_field_id_value(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the row_direction data is empty

    return: None
    """
    payload = deepcopy(config.payload)
    payload['field_id'] = ""
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_response_no_payload(env, api, auth, level):
    """
    Test to ensure an error is returned with an empty payload

    return: None
    """
    payload = '{}'

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


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
    response = plans_get_by_id(env, api, auth, level, 'acebdfac-ebdf-aceb-dfac-ebdfacebdfac')
    json_response = response.json()

    assert response.status_code == 404

    # Validating the error message
    assert json_response['message'] == 'Could not find a plan with plan id acebdfac-ebdf-aceb-dfac-ebdfacebdfac.'


@pytest.mark.exception
def test_plans_get_by_invalid_non_guid_id(env, api, auth, level):
    """
    Test to validate that we get an error when passing in an invalid format for
    an ID

    return: None
    """
    response = plans_get_by_id(env, api, auth, level, 'spider-man_heart_gwen_stacey')

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
    response = plans_get_status(env, api, auth, level, 'acebdfac-ebdf-aceb-dfac-ebdfacebdfac')
    json_response = response.json()

    assert response.status_code == 404

    # Validating the error message
    assert json_response['message'] == 'Could not find a status with the plan id acebdfac-ebdf-aceb-dfac-ebdfacebdfac'


@pytest.mark.exception
def test_plans_get_status_invalid_non_guid_id(env, api, auth, level):
    """
    Test to validate that we get an error when passing in an invalid formatted
    ID

    return: None
    """
    response = plans_get_status(env, api, auth, level, 'spider-man_heart_gwen_stacey')

    assert response.status_code == 400


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
    iterations = 100
    response_time_list = []

    while count <= iterations:
        response = plans_get(env, api, auth, level)

        # converting total_seconds to milliseconds and truncating decimal
        response_time_list.append(int(response.elapsed.total_seconds() * 1000))
        count += 1

    print("\nMinimum: {0}".format(min(response_time_list)))
    print("Maximum: {0}".format(max(response_time_list)))
    print("Average: {0}".format((sum(response_time_list) / len(response_time_list))))
    print(" Median: {0}".format(median(response_time_list)))
    print(" StdDev: {0:.2f}".format(stdev(response_time_list)))

    test_data = "Response Time Performance Data for GET /plans:\nMinimum: {0}\nMaximum: {1}\nAverage: {2}" \
                "\n Median: {3}\n StdDev: {4:.2f}\nCount 0 to 199:  {5} -- Count 200 to 399:  {6} -- Count 400 to " \
                "599:  {7} -- Count 600 to 999:  {8} -- Count 1000+:  {9}".format(
        min(response_time_list), max(response_time_list), sum(response_time_list) / len(response_time_list),
        median(response_time_list), stdev(response_time_list), sum(1 for i in response_time_list if 0 < i <= 199),
        sum(1 for i in response_time_list if 200 <= i <= 399), sum(1 for i in response_time_list if 400 <= i <= 599),
        sum(1 for i in response_time_list if 600 <= i <= 999), sum(1 for i in response_time_list if i >= 1000))

    print(test_data)

    post_message_to_slack(test_data, level)

    logger = logging.getLogger('api_testing')
    logger.setLevel(level)

    logger.debug(response_time_list)


@pytest.mark.performance
def test_plans_get_id_response_performance(env, api, auth, level):
    """
    Test to validate the response time of GET /plans by id over
    multiple iterations.

    return: None
    """

    count = 1
    iterations = 100
    response_time_list = []

    response = plans_get(env, api, auth, level)
    json_response = response.json()

    ## Grab a random ID
    plan_id = random.choice(json_response)['plan_id']

    while count <= iterations:
        response = plans_get_by_id(env, api, auth, level, plan_id)

        # converting total_seconds to milliseconds and truncating decimal
        response_time_list.append(int(response.elapsed.total_seconds() * 1000))
        count += 1

    print("\nMinimum: {0}".format(min(response_time_list)))
    print("Maximum: {0}".format(max(response_time_list)))
    print("Average: {0}".format((sum(response_time_list) / len(response_time_list))))
    print(" Median: {0}".format(median(response_time_list)))
    print(" StdDev: {0:.2f}".format(stdev(response_time_list)))

    test_data = "Response Time Performance Data for GET /plans by ID:\nMinimum: {0}\nMaximum: {1}\nAverage: {2}" \
                "\n Median: {3}\n StdDev: {4:.2f}\nCount 0 to 199:  {5} -- Count 200 to 399:  {6} -- Count 400 to " \
                "599:  {7} -- Count 600 to 999:  {8} -- Count 1000+:  {9}".format(
        min(response_time_list), max(response_time_list), sum(response_time_list) / len(response_time_list),
        median(response_time_list), stdev(response_time_list), sum(1 for i in response_time_list if 0 < i <= 199),
        sum(1 for i in response_time_list if 200 <= i <= 399), sum(1 for i in response_time_list if 400 <= i <= 599),
        sum(1 for i in response_time_list if 600 <= i <= 999), sum(1 for i in response_time_list if i >= 1000))

    print(test_data)

    post_message_to_slack(test_data, level)

    logger = logging.getLogger('api_testing')
    logger.setLevel(level)

    logger.debug(response_time_list)


@pytest.mark.performance
def test_plans_get_status_response_performance(env, api, auth, level):
    """
    Test to validate the response time of GET /plans by id over
    multiple iterations.

    return: None
    """

    count = 1
    iterations = 100
    response_time_list = []

    response = plans_get(env, api, auth, level)
    json_response = response.json()

    ## Grab a random ID
    plan_id = random.choice(json_response)['plan_id']

    while count <= iterations:
        response = plans_get_status(env, api, auth, level, plan_id)

        # converting total_seconds to milliseconds and truncating decimal
        response_time_list.append(int(response.elapsed.total_seconds() * 1000))
        count += 1

    print("\nMinimum: {0}".format(min(response_time_list)))
    print("Maximum: {0}".format(max(response_time_list)))
    print("Average: {0}".format((sum(response_time_list) / len(response_time_list))))
    print(" Median: {0}".format(median(response_time_list)))
    print(" StdDev: {0:.2f}".format(stdev(response_time_list)))

    test_data = "Response Time Performance Data for GET /plans STATUS:\nMinimum: {0}\nMaximum: {1}\nAverage: {2}" \
                "\n Median: {3}\n StdDev: {4:.2f}\nCount 0 to 199:  {5} -- Count 200 to 399:  {6} -- Count 400 to " \
                "599:  {7} -- Count 600 to 999:  {8} -- Count 1000+:  {9}".format(
        min(response_time_list), max(response_time_list), sum(response_time_list) / len(response_time_list),
        median(response_time_list), stdev(response_time_list), sum(1 for i in response_time_list if 0 < i <= 199),
        sum(1 for i in response_time_list if 200 <= i <= 399), sum(1 for i in response_time_list if 400 <= i <= 599),
        sum(1 for i in response_time_list if 600 <= i <= 999), sum(1 for i in response_time_list if i >= 1000))

    print(test_data)

    post_message_to_slack(test_data, level)

    logger = logging.getLogger('api_testing')
    logger.setLevel(level)

    logger.debug(response_time_list)


@pytest.mark.functionality
@pytest.mark.smoke
def test_plans_step_name_validation(env, api, auth, level):
    """
    Test to validate that the stepname is the updated correctly

    return: None
    """
    payload = deepcopy(config.payload)
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 200

    json_response = response.json()

    created_date = json_response['created_date']
    plan_id = json_response['plan_id']

    # Send a GET /plans by ID
    response = plans_get_by_id(env, api, auth, level, plan_id)
    assert response.status_code == 200
    json_response = response.json()

    assert json_response['plan_id'] == plan_id
    assert json_response['created_date'] == created_date

    started_validated = 0
    configure_plan_validated = 0
    exit_flag = 0
    sleep_counter = 0

    while exit_flag == 0 and sleep_counter <= 20:

        if json_response['status']['step_name'] == "Started" and started_validated == 0:
            ''' This is step 1 validation'''
            assert json_response['status']['step_name'] == "Started"
            assert json_response['updated_date'] != created_date
            assert json_response['updated_date'] == json_response['status']['updated_date']
            assert json_response['status']['has_error'] is False
            assert json_response['status']['is_complete'] is False
            started_validated = 1
            print("\nStep_Started Validated")

        elif json_response['status']['step_name'] == "Configuring Plan" and configure_plan_validated == 0:
            ''' This is step 2 validation'''
            assert json_response['status']['step_name'] == "Configuring Plan"
            assert json_response['updated_date'] != created_date
            assert json_response['updated_date'] == json_response['status']['updated_date']
            assert json_response['status']['has_error'] is False
            assert json_response['status']['is_complete'] is False
            configure_plan_validated = 1
            print("Step_Configuring Plan Validated")
            exit_flag = 1
            sleep_counter = 0

        sleep_counter += 1
        sleep(1)

        response = plans_get_by_id(env, api, auth, level, plan_id)
        json_response = response.json()


@pytest.mark.skip(reason="Not written - future test")
def test_plans_post_single_lat_long_boundary(env, api, auth, level):
    """
    To Do - Test to verify we error when providing only one lat/long field boundary (ie a single point as a field)

    return: None
    """
    print("This is not written yet")


@pytest.mark.skip(reason="Not written - future test")
def test_plans_post_multiple_gate_lat_long_boundary(env, api, auth, level):
    """
    To Do - Test to verify we error when providing more than one lat/long for field gate


    return: None
    """
    print("This is not written yet")


@pytest.mark.skip(reason="Not written - future test")
def test_plans_post_multiple_row_direction_lat_long_boundary(env, api, auth, level):
    """
    To Do - Test to verify we error when providing more than one lat/long for field row_direction


    return: None
    """
    print("This is not written yet")


@pytest.mark.skip(reason="Not written - future test")
def test_plans_post_field_boundary_lat_long_DMM(env, api, auth, level):
    """
    To Do - Test to verify we error when field boundary lat/long are provided in DMM format
    Degrees and decimal minutes (DMM): 41 24.2028, 2 10.4418

    return: None
    """
    print("This is not written yet")


@pytest.mark.skip(reason="Not written - future test")
def test_plans_post_field_boundary_lat_long_DMS(env, api, auth, level):
    """
    To Do - Test to verify we error when field boundary lat/long are provided in DMS format
    Degrees, minutes, and seconds (DMS): 41°24'12.2"N 2°10'26.5"E

    return: None
    """
    print("This is not written yet")


@pytest.mark.skip(reason="Not written - future test")
def test_plans_post_multiple_constraints(env, api, auth, level):
    """
    To Do - Test to verify we don't fail when payload has multiple constraints

    return: None
    """
    print("This is not written yet")


if __name__ == "__main__":
    test_plans_post_status_code()
    test_plans_post_plan_id()
    test_plans_post_status_id()
    test_plans_post_created()
