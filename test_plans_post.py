import json
import pytest
import random
import config
from plans_endpoint import plans_get_by_id, plans_post_payload
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
def test_plans_post_field_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field key is missing

    return: None
    """

    payload = deepcopy(config.payload)
    del payload['field']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_constraints_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the constraints key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['constraints']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_constraints_payload_missing(env, api, auth, level):
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
def test_plans_post_field_id_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field_id key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field_id']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_is_ctf_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the is_ctf key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['is_ctf']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_headland_width_optimized_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the headland_width_optimized key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['headland_width_optimized']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_headland_width_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the headland_width key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['headland_width']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_constraints_width_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the constraints width key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['constraints'][0]['width']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_constraints_priority_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the constraints priority key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['constraints'][0]['priority']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_constraints_turning_radius_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the constraints turning_radius key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['constraints'][0]['turning_radius']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_constraints_ramp_up_distance_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the constraints ramp_up_distance key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['constraints'][0]['ramp_up_distance']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_constraints_ramp_down_distance_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the constraints ramp_down_distance key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['constraints'][0]['ramp_down_distance']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.skip(reason="deprecated on July 14 2020")
def test_plans_post_field_name_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field name key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field']['name']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_field_boundary_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field boundary key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field']['boundary']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_field_boundary_boundary_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field boundary_boundary key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field']['boundary']['boundary']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_field_boundary_boundary_lat_long_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if an empty field boundary_boundary payload is sent

    return: None
    """
    payload = deepcopy(config.payload)
    payload['field']['boundary']['boundary'] = []
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_field_gates_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field gates key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field']['gates']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_field_gates_lat_long_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field gates payload is empty

    return: None
    """
    payload = deepcopy(config.payload)
    payload['field']['gates'] = []
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_field_gates_point_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field gates point key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field']['gates'][0]['point']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_field_gates_point_lat_long_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field gates point payload is empty

    return: None
    """
    payload = deepcopy(config.payload)
    payload['field']['gates'][0]['point'] = []
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_field_obstacles_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field obstacles key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field']['obstacles']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_field_obstacles_lat_long_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 200 status if the field obstacles payload is empty

    return: None
    """
    payload = deepcopy(config.payload)
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
    payload = deepcopy(config.payload)
    del payload['row_direction']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_field_soil_type_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field soil type key is missing

    return: None
    """
    payload = deepcopy(config.payload)
    del payload['field']['soil_type']
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_row_direction_lat_long_key_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the row_direction payload is empty

    return: None
    """
    payload = deepcopy(config.payload)
    payload['row_direction'] = []
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_field_id_key_value_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field id payload is empty

    return: None
    """
    payload = deepcopy(config.payload)
    payload['field_id'] = ""
    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_post_payload_empty(env, api, auth, level):
    """
    Test to ensure an error is returned with an empty payload is sent

    return: None
    """
    payload = '{}'

    response = plans_post_payload(env, api, auth, level, payload)

    assert response.status_code == 400


if __name__ == "__main__":
    test_plans_post_status_code()
    test_plans_post_plan_id()
    test_plans_post_status_id()
    test_plans_post_created()
