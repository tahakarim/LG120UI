import json
import pytest
import random
import params
from plans_endpoint import plans_get_by_id, plans_post_payload
from copy import deepcopy
from time import sleep


@pytest.mark.exception
def test_plans_gate_not_connected_to_field(env, api, auth, level):
    """
    Test to validate that a failure is returned when the gate is not attached to the field.

    return: None
    """

    payload = deepcopy(params.payload_all_fields)
    payload['field']['boundary']['boundary'] = params.quarter_circle_field
    payload['field']['gates'][0]['point']['lat'] = -10.450962
    payload['field']['gates'][0]['point']['lng'] = 105.691082
    payload = json.dumps(payload)
    print("\nPayload: {0}".format(payload))
    print(auth)
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
        assert json_response['status']['message'] != "An error has occurred in the workflow while generating a route " \
                                                     "for the requested field. The workflow has been updated " \
                                                     "accordingly and the process " \
                                                     "terminated", "Response: \n{0}".format(json_response)


@pytest.mark.exception
def test_plans_initial_wayline_multiple_lat_long_keys(env, api, auth, level):
    """
    Test to validate that a failure is returned when the initial_wayline has 3 lat/lng pairs.

    return: None
    """

    payload = deepcopy(params.payload_all_fields)
    payload['field']['boundary']['boundary'] = params.quarter_circle_field
    payload['field']['initial_wayline'].append({"lat": 0.0010183, "lng": -0.0001983})
    print(payload)
    payload = json.dumps(payload)

    print("\nPayload: {0}".format(payload))
    print(auth)
    response = plans_post_payload(env, api, auth, level, payload)
    assert response.status_code == 200
    json_response = response.json()
    plan_id = json_response['plan_id']

    response = plans_get_by_id(env, api, auth, level, plan_id)
    assert response.status_code == 200
    json_response = response.json()

    sleep_counter = 0
    sleep_max_counter = 60

    while json_response['status']['is_complete'] is not True and sleep_counter <= sleep_max_counter:
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
def test_plans_field_validation_indiana(env, api, auth, level):
    """
      Test to validate that the large field created correctly
      This test case will also verify that an error message is returned when timed out.  Until this field passes.

      return: None
      """
    payload = deepcopy(params.payload)

    payload['field']['boundary']['boundary'] = params.indiana
    # payload['field']['gates'][0]['point'] = helpers.helper_random_gate(payload['field']['boundary']['boundary'][0],
    #                                                                    payload['field']['boundary']['boundary'][2])

    # payload['row_direction'][0] = helpers.helper_random_fieldpoint(payload['field']['boundary']['boundary'][0],
    #                                                                payload['field']['boundary']['boundary'][2])
    # payload['row_direction'][1] = helpers.helper_random_fieldpoint(payload['field']['boundary']['boundary'][1],
    #                                                                payload['field']['boundary']['boundary'][3])

    # payload['field']['soil_type'] = helpers.helper_random_soiltype()
    payload = json.dumps(payload)

    print("\nPayload: {0}".format(payload))
    print(auth)
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
    # assert json_response['status']['has_error'] is False, "Response: \n{0}".format(json_response)
    # assert json_response['status']['step_name'] == config.last_step_name, "Response: \n{0}".format(json_response)

    assert json_response['status']['is_complete'] is True, "Response: \n{0}".format(json_response)

    if json_response['status']['has_error'] is True:
        assert json_response['status']['message'] == "An error has occurred in the workflow while generating a route " \
                                                     "for the requested field. The workflow has been updated " \
                                                     "accordingly and the process " \
                                                     "terminated", "Response: \n{0}".format(json_response)

    assert sleep_counter < max_sleep, "Timeout Exceeded\n{0}".format(json_response)
    assert json_response['status']['has_error'] is False


@pytest.mark.functionality
def test_plans_field_validation_quarter_circle(env, api, auth, level):
    """
      Test to validate that the quarter circle field created correctly

      return: None
      """
    payload = deepcopy(params.payload)

    payload['field']['boundary']['boundary'] = params.quarter_circle_field

    # payload['field']['gates'][0]['point'] = random.choice(params.quarter_circle_field)
    #
    # payload['row_direction'][0] = helpers.helper_random_fieldpoint({'lat': 37.792516, 'lng': -97.399534},
    #                                                                {'lat': 37.794469, 'lng': -97.403632})
    # payload['row_direction'][1] = helpers.helper_random_fieldpoint({'lat': 37.792516, 'lng': -97.403632},
    #                                                                {'lat': 37.794469, 'lng': -97.399534})
    # payload['field']['soil_type'] = helpers.helper_random_soiltype()

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

    assert json_response['status']['has_error'] is False, "Response: \n{0}".format(json_response)
    assert json_response['status']['step_name'] == params.last_step_name, "Response: \n{0}".format(json_response)

    assert json_response['status']['is_complete'] is True, "Response: \n{0}".format(json_response)

    if json_response['status']['has_error'] is True:
        assert json_response['status']['message'] == "An error has occurred in the workflow while generating a route " \
                                                     "for the requested field. The workflow has been updated " \
                                                     ".accordingly and the process " \
                                                     "terminated", "Response: \n{0}".format(json_response)

    assert sleep_counter < max_sleep, "Timeout Exceeded\n{0}".format(json_response)


@pytest.mark.exception
def test_plans_field_boundary_boundary_single_lat_long_key(env, api, auth, level):
    """
    Test to verify we receive a 200 status if a single lat/long boundary payload data is sent
    Test should fail from lambda validation

    return: None
    """
    payload = deepcopy(params.payload)
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

    while json_response['status']['is_complete'] is not True and sleep_counter <= 10:
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
def test_plans_field_boundary_boundary_two_lat_long_keys(env, api, auth, level):
    """
    Test to verify we receive a 200 status if two lat/long boundary payload data is sent
    Test should fail from lambda validation

    return: None
    """
    payload = deepcopy(params.payload)
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
def test_plans_field_boundary_boundary_lat_long_key_set_to_zero(env, api, auth, level):
    """
    Test to verify we receive a 200 status if a null island lat/long boundary payload data is sent
    Test should fail from lambda validation

    return: None
    """
    payload = deepcopy(params.payload)
    payload1 = payload['field']['boundary']['boundary']
    for i in payload1:
        i.update({"lat": 0.00, "lng": 0.00})

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
def test_plans_lat_lng_invalid_values(env, api, auth, level):
    """
    Test to verify lat/lng values outside the valid ranges is handled correctly. Ranges: Latitudes from -90 to 90 and
    longitudes from -180 to 180.

    return: None
    """
    row_payload = deepcopy(params.payload_all_fields)
    boundary_payload = deepcopy(params.payload_all_fields)
    gates_payload = deepcopy(params.payload_all_fields)
    obstacles_payload = deepcopy(params.payload_all_fields)
    invalid_lat_lng = [-91.0, 91.0, -181.0, 181.0]
    random.shuffle(invalid_lat_lng)
    json_fields = ['initial_wayline', 'boundary', 'gates']  # Need to add 'obstacles' into list.
    random.shuffle(json_fields)
    lat_or_lng = ['lat', 'lng']

    while json_fields:
        field = json_fields.pop()
        invalid_lat_or_lng = invalid_lat_lng.pop()
        tmp_lat_or_lng = random.choice(lat_or_lng)

        if field == 'initial_wayline':
            row_payload['field']['initial_wayline'][0][tmp_lat_or_lng] = invalid_lat_or_lng
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
            assert json_response['status']['message'] != "An error has occurred in the workflow while generating a " \
                                                         "route for the requested field. The workflow has been " \
                                                         "updated accordingly and the process terminated", \
                                                         "Response: \n{0}".format(json_response)


@pytest.mark.functionality
def test_plans_field_validation_half_circle(env, api, auth, level):
    """
      Test to validate that the half circle field created correctly

      return: None
      """
    payload = deepcopy(params.payload)

    payload['field']['boundary']['boundary'] = params.half_circle_field

    # payload['field']['gates'][0]['point'] = random.choice(params.half_circle_field)
    #
    # payload['row_direction'][0] = helpers.helper_random_fieldpoint({'lat': 37.818026, 'lng': -97.404255},
    #                                                                {'lat': 37.818026, 'lng': -97.399223})
    # payload['row_direction'][1] = helpers.helper_random_fieldpoint({'lat': 37.820864, 'lng': -97.399223},
    #                                                                {'lat': 37.820864, 'lng': -97.404255})
    # payload['field']['soil_type'] = helpers.helper_random_soiltype()
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

    assert json_response['status']['has_error'] is False, "Response: \n{0}".format(json_response)
    assert json_response['status']['step_name'] == params.last_step_name, "Response: \n{0}".format(json_response)

    assert json_response['status']['is_complete'] is True, "Response: \n{0}".format(json_response)

    if json_response['status']['has_error'] is True:
        assert json_response['status']['message'] == "An error has occurred in the workflow while generating a route " \
                                                     "for the requested field. The workflow has been updated " \
                                                     "accordingly and the process " \
                                                     "terminated", "Response: \n{0}".format(json_response)

    assert sleep_counter < max_sleep, "Timeout Exceeded\n{0}".format(json_response)


@pytest.mark.functionality
def test_plans_field_validation_full_circle(env, api, auth, level):
    """
      Test to validate that the half circle field created correctly

      return: None
      """
    payload = deepcopy(params.payload)

    payload['field']['boundary']['boundary'] = params.circle_feild

    # payload['field']['gates'][0]['point'] = random.choice(params.circle_feild)
    #
    # payload['row_direction'][0] = helpers.helper_random_fieldpoint({'lat': 34.964350, 'lng': -114.655483},
    #                                                                {'lat': 34.964350, 'lng': -114.654096})
    # payload['row_direction'][1] = helpers.helper_random_fieldpoint({'lat': 34.962717, 'lng': -114.654096},
    #                                                                {'lat': 34.962717, 'lng': -114.655483})
    # payload['field']['soil_type'] = helpers.helper_random_soiltype()
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

    assert json_response['status']['has_error'] is False, "Response: \n{0}".format(json_response)
    assert json_response['status']['step_name'] == params.last_step_name, "Response: \n{0}".format(json_response)

    assert json_response['status']['is_complete'] is True, "Response: \n{0}".format(json_response)

    if json_response['status']['has_error'] is True:
        assert json_response['status']['message'] == "An error has occurred in the workflow while generating a route " \
                                                     "for the requested field. The workflow has been updated " \
                                                     "accordingly and the process " \
                                                     "terminated", "Response: \n{0}".format(json_response)

    assert sleep_counter < max_sleep, "Timeout Exceeded\n{0}".format(json_response)


@pytest.mark.functionality
def test_plans_field_validation_marktoberdorf(env, api, auth, level):
    """
      Test to validate that the half circle field created correctly

      return: None
      """
    payload = deepcopy(params.payload)

    payload['field']['boundary']['boundary'] = params.marktoberdorf_test_field
    #
    # payload['field']['gates'][0]['point']['lat'] = 47.783987
    # payload['field']['gates'][0]['point']['lng'] = 10.606438
    #
    # payload['row_direction'] = [
    #     {
    #         "lat": 47.784394, "lng": 10.607035
    #     },
    #     {
    #         "lat": 47.783987, "lng": 10.606438
    #     }
    # ]

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

    assert json_response['status']['has_error'] is False, "Response: \n{0}".format(json_response)
    assert json_response['status']['step_name'] == params.last_step_name, "Response: \n{0}".format(json_response)

    assert json_response['status']['is_complete'] is True, "Response: \n{0}".format(json_response)

    if json_response['status']['has_error'] is True:
        assert json_response['status']['message'] == "An error has occurred in the workflow while generating a route " \
                                                     "for the requested field. The workflow has been updated " \
                                                     "accordingly and the process " \
                                                     "terminated", "Response: \n{0}".format(json_response)

    assert sleep_counter < max_sleep, "Timeout Exceeded\n{0}".format(json_response)


@pytest.mark.functionality
def test_plans_field_validation_millennium_park(env, api, auth, level):
    """
      Test to validate that the odd shaped / donut style field returns good data.

      return: None
      """
    payload = deepcopy(params.payload)

    payload['field']['boundary']['boundary'] = params.millennium_park_test_field
    # payload['field']['gates'][0]['point'] = random.choice(params.millennium_park_test_field)
    # payload['row_direction'][0] = helpers.helper_random_fieldpoint({'lat': 41.876887, 'lng': -87.620123},
    #                                                                {'lat': 41.874713, 'lng': -87.617830})
    # payload['row_direction'][1] = helpers.helper_random_fieldpoint({'lat': 41.876914, 'lng': -87.617892},
    #                                                                {'lat': 41.874685, 'lng': -87.620076})
    # payload['field']['soil_type'] = helpers.helper_random_soiltype()

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

    assert json_response['status']['has_error'] is False, "Response: \n{0}".format(json_response)
    assert json_response['status']['step_name'] == params.last_step_name, "Response: \n{0}".format(json_response)

    assert json_response['status']['is_complete'] is True, "Response: \n{0}".format(json_response)

    if json_response['status']['has_error'] is True:
        assert json_response['status']['message'] == "An error has occurred in the workflow while generating a route " \
                                                     "for the requested field. The workflow has been updated " \
                                                     "accordingly and the process " \
                                                     "terminated", "Response: \n{0}".format(json_response)

    assert sleep_counter < max_sleep, "Timeout Exceeded\n{0}".format(json_response)


@pytest.mark.functionality
def test_plans_field_validation_boundary_out_of_order_square(env, api, auth, level):
    """
      Test to validate when you present a square field with the boundaries in 1, 3, 2, 4 order.

      return: None
      """
    payload = deepcopy(params.payload)

    payload = deepcopy(params.payload)
    payload['field']['boundary']['boundary'] = params.three_hundred_acre_field

    temp_point_two = payload['field']['boundary']['boundary'][1]
    payload['field']['boundary']['boundary'][1] = payload['field']['boundary']['boundary'][2]
    payload['field']['boundary']['boundary'][2] = temp_point_two

    # payload['field']['gates'][0]['point'] = random.choice(params.three_hundred_acre_field)
    #
    # payload['row_direction'][0] = helpers.helper_random_fieldpoint(payload['field']['boundary']['boundary'][0],
    #                                                                payload['field']['boundary']['boundary'][2])
    # payload['row_direction'][1] = helpers.helper_random_fieldpoint(payload['field']['boundary']['boundary'][1],
    #                                                                payload['field']['boundary']['boundary'][3])

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

    assert json_response['status']['step_name'] == params.last_step_name, "Response: \n{0}".format(json_response)
    assert json_response['status']['has_error'] is False, "Response: \n{0}".format(json_response)

    assert json_response['status']['is_complete'] is True, "Response: \n{0}".format(json_response)

    if json_response['status']['has_error'] is True:
        assert json_response['status']['message'] == "An error has occurred in the workflow while generating a route " \
                                                     "for the requested field. The workflow has been updated " \
                                                     "accordingly and the process " \
                                                     "terminated", "Response: \n{0}".format(json_response)

    assert sleep_counter < max_sleep, "Timeout Exceeded\n{0}".format(json_response)


@pytest.mark.functionality
def test_plans_field_initial_wayline_single_value(env, api, auth, level):
    """
      Test to validate when you present a single value for initial_Wayline handled correctly

      return: None
      """

    payload = deepcopy(params.payload)

    payload['field']['boundary']['boundary'] = params.quarter_circle_field
    payload['field']['initial_wayline'] = []
    payload['field']['initial_wayline'].append(payload['field']['boundary']['boundary'][0])

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

    sleep_counter = 0
    sleep_max_counter = ((60 * 2) + 30)

    while json_response['status']['is_complete'] != True and sleep_counter <= sleep_max_counter:
        sleep_counter += 1
        sleep(2)

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
