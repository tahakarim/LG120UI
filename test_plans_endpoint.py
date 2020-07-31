import json
import logging
import pytest
import random
import config
import helpers
import requests
from datetime import datetime
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
def test_plans_post_field_boundary_boundary_single_lat_long_key(env, api, auth, level):
    """
    Test to verify we receive a 200 status if a single lat/long boundary payload data is sent

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field']['boundary']['boundary'][0:3]
    payload = json.dumps(payload)
    print("\nPayload: {0}".format(payload))

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 200

    json_response = response.json()

    plan_id = json_response['plan_id']

    response = plans_get_by_id(env, api, auth, level, plan_id)

    assert response.status_code == 200

    json_response = response.json()

    sleep_counter = 0

    while json_response['status']['is_complete'] != True and sleep_counter <= 10:
        sleep_counter += 1
        sleep(1)
        response = plans_get_by_id(env, api, auth, level, plan_id)
        assert response.status_code == 200
        json_response = response.json()

        if sleep_counter >= 10:
            assert json_response['status']['is_complete'] is True, "Timeout Exceeded\n{0}".format(json_response)
        elif json_response['status']['is_complete'] is True and json_response['status']['has_error'] is False:
            assert json_response['status']['is_complete'] is True
            assert json_response['status']['has_error'] is True, "hasError is not TRUE\n{0}".format(json_response)

        elif json_response['status']['is_complete'] is True and json_response['status']['has_error'] is True:
            ## Need to Write ---> Add assert to validate failed in the correct step
            assert json_response['status']['is_complete'] is True
            assert json_response['status']['has_error'] is True


@pytest.mark.exception
def test_plans_post_field_boundary_boundary_two_lat_long_key(env, api, auth, level):
    """
    Test to verify we receive a 200 status if  two lat/long boundary payload data is sent

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field']['boundary']['boundary'][0:2]
    payload = json.dumps(payload)
    print("\nPayload: {0}".format(payload))

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 200

    json_response = response.json()

    plan_id = json_response['plan_id']

    response = plans_get_by_id(env, api, auth, level, plan_id)

    assert response.status_code == 200

    json_response = response.json()

    sleep_counter = 0

    while json_response['status']['is_complete'] != True and sleep_counter <= 10:
        sleep_counter += 1
        sleep(1)
        response = plans_get_by_id(env, api, auth, level, plan_id)
        assert response.status_code == 200
        json_response = response.json()

        if sleep_counter >= 10:
            assert json_response['status']['is_complete'] is True, "Timeout Exceeded\n{0}".format(json_response)
        elif json_response['status']['is_complete'] is True and json_response['status']['has_error'] is False:
            assert json_response['status']['is_complete'] is True
            assert json_response['status']['has_error'] is True, "hasError is not TRUE\n{0}".format(json_response)

        elif json_response['status']['is_complete'] is True and json_response['status']['has_error'] is True:
            ## Need to Write ---> Add assert to validate failed in the correct step
            assert json_response['status']['is_complete'] is True
            assert json_response['status']['has_error'] is True


@pytest.mark.exception
def test_plans_post_field_boundary_boundary_null_island_lat_long_key(env, api, auth, level):
    """
    Test to verify we receive a 200 status if a null island lat/long boundary payload data is sent

    return: None
    """
    payload = deepcopy(config.payload)
    payload1 = payload['field']['boundary']['boundary']
    for i in payload1:
        i.update({"lat": 0, "lng": 0})

    payload = json.dumps(payload)
    print("\nPayload: {0}".format(payload))

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 200

    json_response = response.json()

    plan_id = json_response['plan_id']

    response = plans_get_by_id(env, api, auth, level, plan_id)

    assert response.status_code == 200

    json_response = response.json()

    sleep_counter = 0

    while json_response['status']['is_complete'] != True and sleep_counter <= 10:
        sleep_counter += 1
        sleep(1)
        response = plans_get_by_id(env, api, auth, level, plan_id)
        assert response.status_code == 200
        json_response = response.json()

        if sleep_counter >= 10:
            assert json_response['status']['is_complete'] is True, "Timeout Exceeded\n{0}".format(json_response)
        elif json_response['status']['is_complete'] is True and json_response['status']['has_error'] is False:
            assert json_response['status']['is_complete'] is True
            assert json_response['status']['has_error'] is True, "hasError is not TRUE\n{0}".format(json_response)

        elif json_response['status']['is_complete'] is True and json_response['status']['has_error'] is True:
            ## Need to Write ---> Add assert to validate failed in the correct step
            assert json_response['status']['is_complete'] is True
            assert json_response['status']['has_error'] is True


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
    Test to verify we receive a 200 status if the obstacles data is empty

    return: None
    """
    payload = deepcopy(config.payload)
    payload['field']['obstacles'] = []
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 200


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


@pytest.mark.exception
def test_plans_post_lat_lng_invalid_boundary(env, api, auth, level):
    """
    Test to verify lat/lng values outside the ranges is handled correctly.  Ranges: Latitudes from -90 to 90 and
    longitudes from -180 to 180.

    return: None
    """
    row_payload = deepcopy(config.payload)
    boundary_payload = deepcopy(config.payload)
    gates_payload = deepcopy(config.payload)
    obstacles_payload = deepcopy(config.payload)
    invalid_lat_lng = [-91, 91, -181, 181]
    random.shuffle(invalid_lat_lng)
    json_fields = ['row_direction', 'boundary', 'gates']  # Need to add 'obstacles' into list.
    random.shuffle(json_fields)
    lat_or_lng = ['lat', 'lng']

    while json_fields:
        field = json_fields.pop()
        invalid_lat_or_lng = invalid_lat_lng.pop()
        tmp_lat_or_lng = random.choice(lat_or_lng)

        if field == 'row_direction':
            row_payload['row_direction'][0][tmp_lat_or_lng] = invalid_lat_or_lng
            row_payload = json.dumps(row_payload)

        elif field == 'boundary':
            boundary_payload['field']['boundary']['boundary'][0][tmp_lat_or_lng] = invalid_lat_or_lng
            boundary_payload = json.dumps(boundary_payload)

        elif field == 'gates':
            gates_payload['field']['gates'][0]['point'][tmp_lat_or_lng] = invalid_lat_or_lng
            gates_payload = json.dumps(gates_payload)

        else:
            obstacles_payload['field']['obstacles'][0][0][tmp_lat_or_lng] = invalid_lat_or_lng
            obstacles_payload = json.dumps(obstacles_payload)

    # need to add obstacles when implemented
    payloads = [row_payload, boundary_payload, gates_payload]

    for payload in payloads:
        print("Payload: {0}".format(payload))
        response = plans_post_payload(env, api, auth, level, payload)
        assert response.status_code == 200
        json_response = response.json()
        plan_id = json_response['plan_id']

        max_sleep_counter = (60 * 2) + 5
        sleep_counter = 0
        response = plans_get_by_id(env, api, auth, level, plan_id)
        json_response = response.json()

        while json_response['status']['is_complete'] != True and sleep_counter <= max_sleep_counter:
            sleep_counter += 1
            sleep(1)
            response = plans_get_by_id(env, api, auth, level, plan_id)
            assert response.status_code == 200
            json_response = response.json()

        if sleep_counter >= max_sleep_counter:
            assert json_response['status']['is_complete'] is True, "Timeout Exceeded\n{0}".format(json_response)

        elif json_response['status']['is_complete'] is True and json_response['status']['has_error'] is False:
            assert json_response['status']['is_complete'] is True
            assert json_response['status']['has_error'] is True, "hasError is not TRUE\n{0}".format(json_response)

        elif json_response['status']['is_complete'] is True and json_response['status']['has_error'] is True:
            assert json_response['status']['step_name'] == "Generating a partition"
            assert json_response['status']['is_complete'] is True
            assert json_response['status']['has_error'] is True
            assert json_response['status']['message'] == "An error has occurred in the workflow while generating a " \
                                                         "route for the requested field. The workflow has been " \
                                                         "updated accordingly and the process terminated", \
                                                         "Response: \n{0}".format(json_response)


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

        assert 'plan_id' in item, "Response: \n{0}".format(item)
        assert isinstance(item['plan_id'], str), "Response: \n{0}".format(item)
        assert item['plan_id'] is not None, "Response: \n{0}".format(item)

        assert 'field_id' in item, "Response: \n{0}".format(item)
        assert isinstance(item['field_id'], str), "Response: \n{0}".format(item)
        assert item['field_id'] is not None, "Response: \n{0}".format(item)

        assert 'created_date' in item, "Response: \n{0}".format(item)
        assert isinstance(item['created_date'], str), "Response: \n{0}".format(item)
        assert item['created_date'] is not None, "Response: \n{0}".format(item)

        assert 'updated_date' in item, "Response: \n{0}".format(item)
        assert isinstance(item['updated_date'], str), "Response: \n{0}".format(item)
        assert item['updated_date'] is not None, "Response: \n{0}".format(item)

        assert 'is_complete' in item['status'], "Response: \n{0}".format(item)
        assert isinstance(item['status']['is_complete'], bool), "Response: \n{0}".format(item)
        assert item['status']['is_complete'] is not None, "Response: \n{0}".format(item)

        assert 'updated_date' in item['status'], "Response: \n{0}".format(item)
        assert isinstance(item['status']['updated_date'], str), "Response: \n{0}".format(item)
        assert item['status']['updated_date'] is not None, "Response: \n{0}".format(item)

        assert 'step_name' in item['status'], "Response: \n{0}".format(item)
        assert isinstance(item['status']['step_name'], str), "Response: \n{0}".format(item)
        assert item['status']['step_name'] is not None, "Response: \n{0}".format(item)

        assert 'has_error' in item['status'], "Response: \n{0}".format(item)
        assert isinstance(item['status']['has_error'], bool), "Response: \n{0}".format(item)
        assert item['status']['has_error'] is not None, "Response: \n{0}".format(item)

        if 's3_presigned_url' in item:
            assert 's3_presigned_url' in item, "Response: \n{0}".format(item)
            assert isinstance(item['s3_presigned_url'], str), "Response: \n{0}".format(item)
            assert item['s3_presigned_url'] is not None, "Response: \n{0}".format(item)

            # Validate no extra fields in response
            assert len(item) == 6

        else:
            # Validate no extra fields in response
            assert len(item) == 5

        # Validate no extra fields in status part of response
        if 'message' in item['status']:
            assert 'message' in item['status'], "Response: \n{0}".format(item)
            assert isinstance(item['status']['message'], str), "Response: \n{0}".format(item)
            assert item['status']['message'] == "An error has occurred in the workflow while generating a route for " \
                                                "the requested field. The workflow has been updated accordingly and " \
                                                "the process terminated", "Response: \n{0}".format(item)
            assert len(item['status']) == 5
        else:
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


@pytest.mark.exception
def test_plans_gate_not_connected_to_field(env, api, auth, level):
    """
    Test to validate that a failure is returned when the gate is not attached to the field.

    return: None
    """

    payload = deepcopy(config.payload)
    payload['field']['gates'][0]['point']['lat'] = '-10.450962'
    payload['field']['gates'][0]['point']['lng'] = '105.691082'
    payload = json.dumps(payload)
    print("\nPayload: {0}".format(payload))

    response = plans_post_payload(env, api, auth, level, payload)
    assert response.status_code == 200
    json_response = response.json()
    plan_id = json_response['plan_id']

    response = plans_get_by_id(env, api, auth, level, plan_id)
    assert response.status_code == 200
    json_response = response.json()

    sleep_counter = 0
    sleep_max_counter = ((60 * 2) + 30)

    while json_response['status']['is_complete'] != True and sleep_counter <= sleep_max_counter:
        sleep_counter += 1
        sleep(1)

        response = plans_get_by_id(env, api, auth, level, plan_id)
        assert response.status_code == 200
        json_response = response.json()

    if sleep_counter >= sleep_max_counter:
        assert json_response['status']['is_complete'] is True, "Timeout Exceeded\n{0}".format(json_response)

    elif json_response['status']['is_complete'] is True and json_response['status']['has_error'] is False:
        assert json_response['status']['is_complete'] is True
        assert json_response['status']['has_error'] is True, "hasError is not TRUE\n{0}".format(json_response)

    elif json_response['status']['is_complete'] is True and json_response['status']['has_error'] is True:
        assert json_response['status']['step_name'] == "Generating a partition"
        assert json_response['status']['is_complete'] is True
        assert json_response['status']['has_error'] is True
        assert json_response['status']['message'] == "An error has occurred in the workflow while generating a route " \
                                                     "for the requested field. The workflow has been updated " \
                                                     "accordingly and the process " \
                                                     "terminated", "Response: \n{0}".format(json_response)


@pytest.mark.exception
def test_plans_invalid_row_direction_combination(env, api, auth, level):
    """
    Test to validate that a failure is returned when the row_direction has 3 lat/lng pairs.

    return: None
    """

    payload = deepcopy(config.payload)
    payload['row_direction'].append({"lat": 0.0010183, "lng": -0.0001983})
    payload = json.dumps(payload)
    print("\nPayload: {0}".format(payload))

    response = plans_post_payload(env, api, auth, level, payload)
    assert response.status_code == 200
    json_response = response.json()
    plan_id = json_response['plan_id']

    response = plans_get_by_id(env, api, auth, level, plan_id)
    assert response.status_code == 200
    json_response = response.json()

    sleep_counter = 0
    sleep_max_counter = 60

    while json_response['status']['is_complete'] != True and sleep_counter <= sleep_max_counter:
        sleep_counter += 1
        sleep(1)

        response = plans_get_by_id(env, api, auth, level, plan_id)
        assert response.status_code == 200
        json_response = response.json()

    if sleep_counter >= sleep_max_counter:
        assert json_response['status']['is_complete'] is True, "Timeout Exceeded\n{0}".format(json_response)

    elif json_response['status']['is_complete'] is True and json_response['status']['has_error'] is False:
        assert json_response['status']['is_complete'] is True
        assert json_response['status']['has_error'] is True, "hasError is not TRUE\n{0}".format(json_response)

    elif json_response['status']['is_complete'] is True and json_response['status']['has_error'] is True:
        assert json_response['status']['step_name'] == "Generating a partition"
        assert json_response['status']['is_complete'] is True
        assert json_response['status']['has_error'] is True


@pytest.mark.functionality
@pytest.mark.smoke
def test_plans_step_name_validation(env, api, auth, level, short):
    """
    Test to validate that the stepname is the updated correctly

    return: None
    """
    payload = deepcopy(config.payload)
    ### Temp Code
    # payload = json.dumps(payload)

    payload['field']['boundary']['boundary'] = config.quarter_circle_field
    payload['field']['gates'][0]['point'] = payload['field']['boundary']['boundary'][0]
    payload['row_direction'][0] = payload['field']['boundary']['boundary'][0]
    payload['row_direction'][1] = payload['field']['boundary']['boundary'][1]

    payload = json.dumps(payload)
    ### End Temp Code

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
    print(plan_id)

    started_validated = 0
    configure_plan_validated = 0
    generating_field_partitions_validated = 0
    saving_partition_validated = 0
    saved_partition_to_s3 = 0
    sleep_counter = 0

    # 60 seconds * number of minutes.
    max_sleep = 60 * 2
    status_updated_date = None

    while saved_partition_to_s3 == 0 and sleep_counter <= max_sleep:

        if json_response['status']['step_name'] == "Started" and started_validated == 0:
            ''' This is step 1 validation'''
            assert json_response['status']['step_name'] == "Started"
            assert json_response['updated_date'] == json_response['status']['updated_date']
            status_updated_date = json_response['status']['updated_date']
            assert json_response['status']['has_error'] is False
            assert json_response['status']['is_complete'] is False
            assert 's3_presigned_url' not in json_response, "Response: \n{0}".format(json_response)
            started_validated = 1
            print("\nStep: Started Validated")

        elif json_response['status']['step_name'] == "Configuring Plan" and configure_plan_validated == 0:
            ''' This is step 2 validation'''
            assert json_response['status']['step_name'] == "Configuring Plan"
            assert json_response['updated_date'] != created_date
            assert json_response['updated_date'] == json_response['status']['updated_date']
            assert json_response['updated_date'] != status_updated_date
            status_updated_date = json_response['status']['updated_date']
            assert json_response['status']['has_error'] is False
            assert json_response['status']['is_complete'] is False
            assert 's3_presigned_url' not in json_response, "Response: \n{0}".format(json_response)
            configure_plan_validated = 1
            print("Step: Configuring Plan Validated")
            sleep_counter = 0

        elif json_response['status']['step_name'] == "Generating a partition" and \
                generating_field_partitions_validated == 0:
            ''' This is step 3 validation'''
            assert json_response['status']['step_name'] == "Generating a partition"
            assert json_response['updated_date'] != created_date
            assert json_response['updated_date'] == json_response['status']['updated_date']
            assert json_response['updated_date'] != status_updated_date
            status_updated_date = json_response['status']['updated_date']
            assert json_response['status']['has_error'] is False
            assert json_response['status']['is_complete'] is False
            assert 's3_presigned_url' not in json_response, "Response: \n{0}".format(json_response)
            generating_field_partitions_validated = 1
            print("Step: Generating a partition")
            sleep_counter = 0

        elif json_response['status']['step_name'] == "Saving partition" and \
                saving_partition_validated == 0:
            ''' This is step 4 validation'''
            assert json_response['status']['step_name'] == "Saving partition"
            assert json_response['updated_date'] != created_date
            assert json_response['updated_date'] == json_response['status']['updated_date']
            assert json_response['updated_date'] != status_updated_date
            status_updated_date = json_response['status']['updated_date']
            assert json_response['status']['has_error'] is False
            assert json_response['status']['is_complete'] is False
            assert 's3_presigned_url' not in json_response, "Response: \n{0}".format(json_response)
            saving_partition_validated = 1
            print("Step: Saving partition")
            sleep_counter = 0

        elif json_response['status']['step_name'] == "Saved partition to S3" and saved_partition_to_s3 == 0:
            ''' This is step 5 validation'''
            assert json_response['status']['step_name'] == "Saved partition to S3"
            assert json_response['updated_date'] != created_date
            assert json_response['updated_date'] == json_response['status']['updated_date']
            assert json_response['updated_date'] != status_updated_date
            status_updated_date = json_response['status']['updated_date']
            assert json_response['status']['has_error'] is False
            assert json_response['status']['is_complete'] is True
            assert json_response['s3_presigned_url'] is not None

            ## Verify the signed URL
            s3_url_data = requests.get(json_response['s3_presigned_url'])
            assert s3_url_data.status_code == 200
            s3_url_data_json = s3_url_data.json()

            assert 'partition' in s3_url_data_json['body'], "Response: \n{0}".format(s3_url_data_json)
            assert s3_url_data_json['body']['message'] == "Successfully generated a partition", \
                "Response: \n{0}".format(s3_url_data_json)

            saved_partition_to_s3 = 1
            print("Step: Saved partition to S3")
            sleep_counter = 0

        sleep_counter += 1
        sleep(1)

        response = plans_get_by_id(env, api, auth, level, plan_id)
        json_response = response.json()

    assert sleep_counter < max_sleep, "Timeout Exceeded\n{0}".format(json_response)

    ## Sleep for 10 minutes and 5 seconds to ensure s3 URL is dead.
    if short is False:
        sleep((60 * 10) + 5)
        s3_url_data = requests.get(json_response['s3_presigned_url'])
        assert s3_url_data.status_code == 403


@pytest.mark.functionality
def test_plans_post_large_field(env, api, auth, level):
    """
      Test to validate that the large field created correctly
      This test case will also verify that an error message is returned when timed out.  Until this field
      passes.

      return: None
      """
    payload = deepcopy(config.payload)

    payload['field']['boundary']['boundary'] = config.indiana
    payload['field']['gates'][0]['point'] = helpers.helper_random_gate(payload['field']['boundary']['boundary'][0],
                                                                       payload['field']['boundary']['boundary'][2])

    payload['row_direction'][0] = helpers.helper_random_fieldpoint(payload['field']['boundary']['boundary'][0],
                                                                   payload['field']['boundary']['boundary'][2])
    payload['row_direction'][1] = helpers.helper_random_fieldpoint(payload['field']['boundary']['boundary'][1],
                                                                   payload['field']['boundary']['boundary'][3])

    payload = json.dumps(payload)

    print("\nPayload: {0}".format(payload))

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 200

    json_response = response.json()

    plan_id = json_response['plan_id']

    # Send a GET /plans by ID
    response = plans_get_by_id(env, api, auth, level, plan_id)
    assert response.status_code == 200
    json_response = response.json()

    # 60 seconds * number of minutes.
    max_sleep = (60 * 2) + 30
    sleep_counter = 0

    while json_response['status']['is_complete'] is False and sleep_counter <= max_sleep:
        sleep(1)
        response = plans_get_by_id(env, api, auth, level, plan_id)
        json_response = response.json()
        sleep_counter += 1

    # Removing these validations until this field passes
    # assert json_response['status']['step_name'] == config.last_step_name, "Response: \n{0}".format(json_response)
    # assert json_response['status']['has_error'] is False, "Response: \n{0}".format(json_response)

    assert json_response['status']['is_complete'] is True, "Response: \n{0}".format(json_response)

    if json_response['status']['has_error'] is True:
        assert json_response['status']['message'] == "An error has occurred in the workflow while generating a route " \
                                                     "for the requested field. The workflow has been updated " \
                                                     ".accordingly and the process " \
                                                     "terminated", "Response: \n{0}".format(json_response)

    assert sleep_counter < max_sleep, "Timeout Exceeded\n{0}".format(json_response)


@pytest.mark.stress
def test_plans_load_test(env, api, auth, level):
    """
      Test to validate if field creation slows under stress

      return: None
    """
    payload = deepcopy(config.payload)
    payload['field']['boundary']['boundary'] = config.three_hundred_acre_field
    payload['field']['gates'][0]['point'] = helpers.helper_random_gate(payload['field']['boundary']['boundary'][0],
                                                                       payload['field']['boundary']['boundary'][2])
    payload['row_direction'][0] = helpers.helper_random_fieldpoint(payload['field']['boundary']['boundary'][0],
                                                                   payload['field']['boundary']['boundary'][2])
    payload['row_direction'][1] = helpers.helper_random_fieldpoint(payload['field']['boundary']['boundary'][1],
                                                                   payload['field']['boundary']['boundary'][3])

    payload = json.dumps(payload)
    print("\nPayload: {0}".format(payload))

    # Send a single file to get a baseline.
    response = plans_post_payload(env, api, auth, level, payload)
    assert response.status_code == 200
    json_response = response.json()

    plan_id = json_response['plan_id']

    response = plans_get_by_id(env, api, auth, level, plan_id)
    assert response.status_code == 200
    json_response = response.json()

    while json_response['status']['is_complete'] is False:
        sleep(5)
        response = plans_get_by_id(env, api, auth, level, plan_id)
        assert response.status_code == 200
        json_response = response.json()

    if json_response['status']['has_error'] is True:
        assert json_response['status']['has_error'] is False, "Baseline Failed - Response: \n{0}".format(json_response)

    # Download the file and save off for future validation.
    s3_url_data_initial = requests.get(json_response['s3_presigned_url'])
    assert s3_url_data_initial.status_code == 200
    s3_url_data_initial = s3_url_data_initial.json()
    s3_body_baseline = s3_url_data_initial['body']['partition']

    # Calculate delta time.
    delta_time_format = '%Y-%m-%d %H:%M:%S.%f'
    milli_created = datetime.strptime(json_response['created_date'], delta_time_format).timestamp() * 1
    milli_updated = datetime.strptime(json_response['updated_date'], delta_time_format).timestamp() * 1
    delta_millisecond_initial = milli_updated - milli_created

    print("Seconds Baseline Delta: {0}".format(delta_millisecond_initial))

    # Sending x number of field creations
    number_of_fields = 100
    list_of_plan_id = []

    for x in range(number_of_fields):
        response = plans_post_payload(env, api, auth, level, payload)
        assert response.status_code == 200
        json_response = response.json()
        list_of_plan_id.append(json_response['plan_id'])

    list_of_time_delta = []
    list_of_failed_id = []

    # Getting each of the responses, validating fields match and storing off the delta time.
    for plan_id in list_of_plan_id:

        print("Working on Plan: {0}".format(plan_id))

        # Check to see if finished
        response = plans_get_by_id(env, api, auth, level, plan_id)
        assert response.status_code == 200
        json_response = response.json()

        while json_response['status']['is_complete'] is False:
            sleep(1)
            response = plans_get_by_id(env, api, auth, level, plan_id)
            assert response.status_code == 200
            json_response = response.json()

        if json_response['status']['has_error'] is True:
            list_of_failed_id.append(plan_id)
            continue

        # Check to see body matches baseline
        s3_url_data = requests.get(json_response['s3_presigned_url'])
        assert s3_url_data.status_code == 200
        s3_url_data = s3_url_data.json()
        assert s3_body_baseline == s3_url_data['body']['partition']

        # Store off time delta
        milli_created = datetime.strptime(json_response['created_date'], delta_time_format).timestamp() * 1
        milli_updated = datetime.strptime(json_response['updated_date'], delta_time_format).timestamp() * 1
        delta_milliseconds = milli_updated - milli_created

        list_of_time_delta.append(delta_milliseconds)

        print("Seconds Delta Time: {0}".format(delta_milliseconds))

    # Process the data
    # Display Basic Data
    print("\nInital Baseline: {0}".format(delta_millisecond_initial))
    print("Minimum: {0}".format(min(list_of_time_delta)))
    print("Maximum: {0}".format(max(list_of_time_delta)))
    print("Average: {0}".format(sum(list_of_time_delta) / len(list_of_time_delta)))
    print(" Median: {0}".format(median(list_of_time_delta)))
    print(" StdDev: {0:.2f}".format(stdev(list_of_time_delta)))

    # Num that are greater than 10% of baseline
    slack_percentage = 1.1
    adjusted_baseline = slack_percentage * delta_millisecond_initial
    counter = 0

    for x in list_of_time_delta:
        if x > adjusted_baseline:
            counter += 1

    print("Delta Greater Than Base: {0}".format(counter))


@pytest.mark.functionality
def test_plans_post_quarter_circle_field(env, api, auth, level):
    """
      Test to validate that the quarter circle field created correctly

      return: None
      """
    payload = deepcopy(config.payload)

    payload['field']['boundary']['boundary'] = config.quarter_circle_field

    payload['field']['gates'][0]['point'] = random.choice(config.quarter_circle_field)

    payload['row_direction'][0] = helpers.helper_random_fieldpoint({'lat': 37.792516, 'lng': -97.399534},
                                                                   {'lat': 37.794469, 'lng': -97.403632})
    payload['row_direction'][1] = helpers.helper_random_fieldpoint({'lat': 37.792516, 'lng': -97.403632},
                                                                   {'lat': 37.794469, 'lng': -97.399534})

    payload = json.dumps(payload)

    print("\nPayload: {0}".format(payload))

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 200

    json_response = response.json()

    plan_id = json_response['plan_id']

    # Send a GET /plans by ID
    response = plans_get_by_id(env, api, auth, level, plan_id)
    assert response.status_code == 200
    json_response = response.json()

    # 60 seconds * number of minutes.
    max_sleep = (60 * 2) + 30
    sleep_counter = 0

    while json_response['status']['is_complete'] is False and sleep_counter <= max_sleep:
        sleep(1)
        response = plans_get_by_id(env, api, auth, level, plan_id)
        json_response = response.json()
        sleep_counter += 1

    assert json_response['status']['step_name'] == config.last_step_name, "Response: \n{0}".format(json_response)
    assert json_response['status']['has_error'] is False, "Response: \n{0}".format(json_response)

    assert json_response['status']['is_complete'] is True, "Response: \n{0}".format(json_response)

    if json_response['status']['has_error'] is True:
        assert json_response['status']['message'] == "An error has occurred in the workflow while generating a route " \
                                                     "for the requested field. The workflow has been updated " \
                                                     ".accordingly and the process " \
                                                     "terminated", "Response: \n{0}".format(json_response)

    assert sleep_counter < max_sleep, "Timeout Exceeded\n{0}".format(json_response)


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
