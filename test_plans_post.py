import json
import pytest
import params
import helpers
import random
from plans_endpoint import plans_post_payload, plans_get_by_id
from copy import deepcopy
from time import sleep


@pytest.mark.functionality
@pytest.mark.smoke
def test_plans_post_response_validation(env, api, auth, level):
    """
    Test to verify the fields are correct in a plans post response. We will be validating the key exists,
    not NULL and correct type.

    return: None
    """
    payload = deepcopy(params.payload)
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
def test_plans_post_field_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field key is missing

    return: None
    """

    payload = deepcopy(params.payload)
    del payload['field']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response['message'] == "Unable to create plan with invalid input: Expected parameter field is" \
                                       " required, but none was provided."


@pytest.mark.exception
def test_plans_post_constraints_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the constraints key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['constraints']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response['message'] == "Unable to create plan with invalid input: Expected parameter constraints" \
                                       " is required, but none was provided."


@pytest.mark.exception
def test_plans_post_constraints_payload_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the constraints payload is missing

    return: None
    """
    payload = deepcopy(params.payload)
    payload['constraints'] = []
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected parameter constraints " \
                                       "is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_id_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field_id key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['field_id']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response['message'] == "Unable to create plan with invalid input: Expected parameter field_id " \
                                       "is required, but none was provided."


@pytest.mark.exception
def test_plans_post_is_ctf_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the is_ctf key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['is_ctf']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response['message'] == "Unable to create plan with invalid input: Expected parameter is_ctf " \
                                       "is required, but none was provided."


@pytest.mark.exception
def test_plans_post_headland_width_optimized_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the headland_width_optimized key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['headland_width_optimized']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response['message'] == "Unable to create plan with invalid input: Expected parameter " \
                                       "headland_width_optimized is required, but none was provided."


@pytest.mark.exception
def test_plans_post_headland_width_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the headland_width key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['headland_width']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response['message'] == "Unable to create plan with invalid input: Expected parameter headland_width" \
                                       " is required, but none was provided."


@pytest.mark.exception
def test_plans_post_constraints_width_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the constraints width key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['constraints'][0]['width']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected constraints parameter" \
                                       " width is required, but none was provided."


@pytest.mark.exception
def test_plans_post_constraints_priority_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the constraints priority key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['constraints'][0]['priority']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected constraints parameter" \
                                       " priority is required, but none was provided."


@pytest.mark.exception
def test_plans_post_constraints_turning_radius_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the constraints turning_radius key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['constraints'][0]['turning_radius']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected constraints parameter " \
                                       "turning_radius is required, but none was provided."


@pytest.mark.exception
def test_plans_post_constraints_ramp_up_distance_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the constraints ramp_up_distance key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['constraints'][0]['ramp_up_distance']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected constraints parameter " \
                                       "ramp_up_distance is required, but none was provided."


@pytest.mark.exception
def test_plans_post_constraints_ramp_down_distance_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the constraints ramp_down_distance key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['constraints'][0]['ramp_down_distance']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected constraints parameter" \
                                       " ramp_down_distance is required, but none was provided."


@pytest.mark.skip(reason="deprecated on July 14 2020")
def test_plans_post_field_name_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field name key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['field']['name']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    json_response = response.json()
    print(json_response)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_field_boundary_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field boundary key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['field']['boundary']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response['message'] == "Unable to create plan with invalid input: Expected field parameter " \
                                       "boundary is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_boundary_boundary_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field boundary_boundary key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['field']['boundary']['boundary']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response['message'] == "Unable to create plan with invalid input: Expected field parameter" \
                                       " boundary boundary is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_boundary_boundary_lat_long_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if an empty field boundary_boundary payload is sent

    return: None
    """
    payload = deepcopy(params.payload)
    payload['field']['boundary']['boundary'] = []
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected field parameter " \
                                       "boundary boundary is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_boundary_boundary_lat_null(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field boundary boundary lat value is null

    return: None
    """
    null_lat = None

    payload = deepcopy(params.payload)
    payload['field']['boundary']['boundary'][0]['lat'] = null_lat
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected field boundary" \
                                       " boundary point parameter lat is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_boundary_boundary_lng_null(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field boundary boundary lng value is null

    return: None
    """
    null_lng = None

    payload = deepcopy(params.payload)
    payload['field']['boundary']['boundary'][0]['lng'] = null_lng
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected field boundary " \
                                       "boundary point parameter lng is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_boundary_boundary_lat_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field boundary boundary lat key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['field']['boundary']['boundary'][0]['lat']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected field boundary " \
                                       "boundary point parameter lat is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_boundary_boundary_lng_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field boundary boundary lng key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['field']['boundary']['boundary'][0]['lng']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected field boundary" \
                                       " boundary point parameter lng is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_gates_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field gates key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['field']['gates']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response['message'] == "Unable to create plan with invalid input: Expected field parameter gates" \
                                       " is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_gates_lng_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field gates lng key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['field']['gates'][0]['point']['lng']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected field gates point " \
                                       "parameter lng is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_gates_lat_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field gates lat key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['field']['gates'][0]['point']['lat']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected field gates point " \
                                       "parameter lat is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_gates_lat_null(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field gates lat value is null

    return: None
    """
    null_lat = None

    payload = deepcopy(params.payload)
    payload['field']['gates'][0]['point']['lat'] = null_lat
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected field gates point" \
                                       " parameter lat is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_gates_lng_null(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field gates lng value is null

    return: None
    """
    null_lng = None

    payload = deepcopy(params.payload)
    payload['field']['gates'][0]['point']['lng'] = null_lng
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected field gates point " \
                                       "parameter lng is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_gates_lat_long_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field gates payload is empty

    return: None
    """
    payload = deepcopy(params.payload)
    payload['field']['gates'] = []
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected field parameter" \
                                       " gates is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_gates_point_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field gates point key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['field']['gates'][0]['point']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected field gates parameter" \
                                       " point is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_gates_point_lat_long_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field gates point payload is empty

    return: None
    """
    payload = deepcopy(params.payload)
    payload['field']['gates'][0]['point'] = []
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected field gates point" \
                                       " parameter lat is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_obstacles_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 200 status if the field obstacles key is missing

    return: None
    """
    payload = deepcopy(params.payload)

    payload['field']['boundary']['boundary'] = params.quarter_circle_field
    payload['field']['gates'][0]['point'] = payload['field']['boundary']['boundary'][0]
    payload['row_direction'][0] = payload['field']['boundary']['boundary'][0]
    payload['row_direction'][1] = payload['field']['boundary']['boundary'][1]

    del payload['field']['obstacles']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()
    assert response.status_code == 200

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
        elif json_response['status']['is_complete'] is True and json_response['status']['has_error'] is True:
            assert json_response['status']['is_complete'] is True
            assert json_response['status']['has_error'] is False, "hasError is not False\n{0}".format(json_response)

        elif json_response['status']['is_complete'] is True and json_response['status']['has_error'] is False:
            ## Need to Write ---> Add assert to validate failed in the correct step
            assert json_response['status']['is_complete'] is True
            assert json_response['status']['has_error'] is False


@pytest.mark.exception
def test_plans_post_field_obstacles_key_validation(env, api, auth, level):
    """
    Test to verify we receive a 200 status if the field obstacles lat/long data has sent

    return: None
    """
    payload = deepcopy(params.payload)

    payload['field']['boundary']['boundary'] = params.quarter_circle_field
    payload['field']['gates'][0]['point'] = payload['field']['boundary']['boundary'][0]
    payload['row_direction'][0] = payload['field']['boundary']['boundary'][0]
    payload['row_direction'][1] = payload['field']['boundary']['boundary'][1]

    payload['field']['obstacles'] = random.choice(payload['field']['boundary']['boundary'])

    payload = json.dumps(payload)
    print(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()
    assert response.status_code == 200

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
        elif json_response['status']['is_complete'] is True and json_response['status']['has_error'] is True:
            assert json_response['status']['is_complete'] is True
            assert json_response['status']['has_error'] is False, "hasError is not False\n{0}".format(json_response)

        elif json_response['status']['is_complete'] is True and json_response['status']['has_error'] is False:
            ## Need to Write ---> Add assert to validate failed in the correct step
            assert json_response['status']['is_complete'] is True
            assert json_response['status']['has_error'] is False


@pytest.mark.exception
def test_plans_post_field_obstacles_lat_long_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 200 status if the field obstacles payload is empty

    return: None
    """
    payload = deepcopy(params.payload)
    payload['field']['obstacles'] = []
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 200


@pytest.mark.exception
def test_plans_post_row_direction_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the row_direction key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['row_direction']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response['message'] == "Unable to create plan with invalid input: Expected parameter row_direction " \
                                       "is required, but none was provided."


@pytest.mark.exception
def test_plans_post_row_direction_lat_null(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the row_direction lat value is null

    return: None
    """
    null_lat = None

    payload = deepcopy(params.payload)
    payload['row_direction'][0]['lat'] = null_lat
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected row_direction" \
                                       " parameter lat is required, but none was provided."


@pytest.mark.exception
def test_plans_post_row_direction_lng_null(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the row_direction lng value is null

    return: None
    """
    null_lng = None

    payload = deepcopy(params.payload)
    payload['row_direction'][0]['lng'] = null_lng
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected row_direction " \
                                       "parameter lng is required, but none was provided."


@pytest.mark.exception
def test_plans_post_row_direction_lat_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the row_direction lat key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['row_direction'][0]['lat']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected row_direction " \
                                       "parameter lat is required, but none was provided."


@pytest.mark.exception
def test_plans_post_row_direction_lng_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the row_direction lng key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['row_direction'][0]['lng']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected row_direction" \
                                       " parameter lng is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_soil_type_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field soil type key is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['field']['soil_type']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response['message'] == "Unable to create plan with invalid input: Expected field parameter " \
                                       "soil_type is required, but none was provided."


@pytest.mark.exception
def test_plans_post_row_direction_lat_long_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the row_direction payload is empty

    return: None
    """
    payload = deepcopy(params.payload)
    payload['row_direction'] = []
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected parameter " \
                                       "row_direction is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_id_key_value_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field id payload is empty

    return: None
    """
    payload = deepcopy(params.payload)
    payload['field_id'] = ""
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected parameter " \
                                       "field_id is required, but none was provided."


@pytest.mark.skip(reason="not in prod")
def test_plans_post_implement_width_key_value_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if implement_width data is missing

    return: None
    """
    payload = deepcopy(params.payload)
    del payload['implement_width']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected parameter " \
                                       "implement_width is required, but none was provided."

@pytest.mark.exception
def test_plans_post_payload_empty(env, api, auth, level):
    """
    Test to ensure an error is returned with an empty payload is sent

    return: None
    """
    payload = '{}'
    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response['message'] == "Unable to create plan with invalid input: Expected parameter " \
                                       "field_id is required, but none was provided."


@pytest.mark.exception
def test_plans_post_field_boundary_in_dms_format(env, api, auth, level):
    """
    Test to ensure an error is returned when sending lat/lng's in DMS format (37°45'50.7 N).

    return: None
    """
    payload = deepcopy(params.payload)
    payload['field']['boundary']['boundary'] = deepcopy(params.three_hundred_acre_field)

    payload['field']['gates'][0]['point'] = helpers.helper_random_gate(payload['field']['boundary']['boundary'][0],
                                                                       payload['field']['boundary']['boundary'][2])
    payload['row_direction'][0] = helpers.helper_random_fieldpoint(payload['field']['boundary']['boundary'][0],
                                                                   payload['field']['boundary']['boundary'][2])
    payload['row_direction'][1] = helpers.helper_random_fieldpoint(payload['field']['boundary']['boundary'][1],
                                                                   payload['field']['boundary']['boundary'][3])

    payload['field']['boundary']['boundary'][0]['lat'] = "37°45'50.7 N"
    payload['field']['boundary']['boundary'][0]['lng'] = "97°38'40.4 W"

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_field_boundary_in_dmm_format(env, api, auth, level):
    """
    Test to ensure an error is returned when sending lat/lng's in DMM format (37°45.8445 N).

    return: None
    """
    payload = deepcopy(params.payload)
    payload['field']['boundary']['boundary'] = deepcopy(params.three_hundred_acre_field)

    payload['field']['gates'][0]['point'] = helpers.helper_random_gate(payload['field']['boundary']['boundary'][0],
                                                                       payload['field']['boundary']['boundary'][2])
    payload['row_direction'][0] = helpers.helper_random_fieldpoint(payload['field']['boundary']['boundary'][0],
                                                                   payload['field']['boundary']['boundary'][2])
    payload['row_direction'][1] = helpers.helper_random_fieldpoint(payload['field']['boundary']['boundary'][1],
                                                                   payload['field']['boundary']['boundary'][3])

    payload['field']['boundary']['boundary'][0]['lat'] = "37°45.8445 N"
    payload['field']['boundary']['boundary'][0]['lng'] = "97°38.6734 W"

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_field_soil_type_invalid_choice(env, api, auth, level):
    """
    Test to ensure an error is returned when sending a field soil_type that is invalid

    return: None
    """
    payload = deepcopy(params.payload)
    payload['field']['soil_type'] = "ocean_salt_water"
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response['message'] == "Unable to create plan with invalid input: Expected field parameter" \
                                       " soil_type has an incorrect value."


if __name__ == "__main__":
    test_plans_post_status_code()
    test_plans_post_plan_id()
    test_plans_post_status_id()
    test_plans_post_created()
