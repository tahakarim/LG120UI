import params
import json
import helpers
import random
from copy import deepcopy
from pytest import fixture, exit
from plans_endpoint import plans_get_by_id, plans_post_payload
from time import sleep


def pytest_addoption(parser):
    """
    pytest command line parser to store command line arguments.

    return: None
    """

    parser.addoption("--env", action="store", default="stg", dest="env",
                     choices=['dev', 'stg', 'prod'])
    parser.addoption("--api", action="store", default="v1beta1", dest="api",
                     choices=['v1alpha1', 'v1beta1', 'v1beta2'])
    parser.addoption("--auth", action="store", default='aaat', dest="auth",
                     choices=['aaa', 'aaat', 'gigya'])
    parser.addoption("--level", action="store", default='INFO', dest="level",
                     choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.addoption("--short", action="store_true", default=False, dest="short")


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


@fixture()
def short(request):
    return request.config.getoption("--short")


def pytest_configure(config):
    env = config.getoption('env')
    api = config.getoption('api')
    auth = config.getoption('auth')
    level = config.getoption('level')
    params.global_api = config.getoption('api')
    if api != 'v1beta2':
        payload = deepcopy(params.payload_optional)
        payload['field']['boundary']['boundary'] = params.quarter_circle_field
        payload['field']['gates'][0]['point'] = random.choice(params.quarter_circle_field)
        payload['row_direction'][0] = helpers.helper_random_fieldpoint({'lat': 37.792516, 'lng': -97.399534},
                                                                       {'lat': 37.794469, 'lng': -97.403632})
        payload['row_direction'][1] = helpers.helper_random_fieldpoint({'lat': 37.792516, 'lng': -97.403632},
                                                                       {'lat': 37.794469, 'lng': -97.399534})
        payload['field']['soil_type'] = helpers.helper_random_soiltype()

    else:
        payload = deepcopy(params.payload)
        payload['field']['boundary']['boundary'] = params.quarter_circle_field

    payload = json.dumps(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()
    plan_id = json_response['plan_id']
    print("Plan_ID: {0}".format(plan_id))

    response = plans_get_by_id(env, api, auth, level, plan_id)
    json_response = response.json()

    while json_response['status']['is_complete'] is False:
        sleep(5)
        response = plans_get_by_id(env, api, auth, level, plan_id)
        json_response = response.json()

    if json_response['status']['has_error'] is False:
        params.test_plan_id = json_response['plan_id']
    else:
        print(json_response)
        exit("Setup Failed")
