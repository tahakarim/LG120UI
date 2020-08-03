import json
import logging
import pytest
import random
import config
import requests
from plans_endpoint import plans_get, plans_get_by_id, plans_get_status, plans_post_payload
from copy import deepcopy
from time import sleep


@pytest.mark.functionality
@pytest.mark.smoke
def test_plans_get_response_validation(env, api, auth, level):
    """
    Test to verify the fields are correct in a plans get response. We will be validating the key exists,
    not NULL and correct type.

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
def test_plans_get_response_at_least_one_plan_id_returned(env, api, auth, level):
    """
    Test to verify at least one plan id is returned from GET/plans.

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
    Test to validate that we are returning one status and that it is the correct status

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
def test_plans_get_by_id_invalid_guid_id(env, api, auth, level):
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
def test_plans_get_by_id_non_guid_id(env, api, auth, level):
    """
    Test to validate that we get an error when passing in an invalid format for an ID

    return: None
    """
    response = plans_get_by_id(env, api, auth, level, 'spider-man_heart_gwen_stacey')

    assert response.status_code == 400


@pytest.mark.functionality
@pytest.mark.smoke
def test_plans_get_status_response_validation(env, api, auth, level):
    """
    Test to validate that we are returning one status and that it is the correct status

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
    Test to validate that we get an error when passing in an invalid ID to GET/plans/status

    return: None
    """
    response = plans_get_status(env, api, auth, level, 'acebdfac-ebdf-aceb-dfac-ebdfacebdfac')
    json_response = response.json()

    assert response.status_code == 404

    # Validating the error message
    assert json_response['message'] == 'Could not find a status with the plan id acebdfac-ebdf-aceb-dfac-ebdfacebdfac'


@pytest.mark.exception
def test_plans_get_status_non_guid_id(env, api, auth, level):
    """
    Test to validate that we get an error when passing in an invalid formatted ID to GET/plans/status

    return: None
    """
    response = plans_get_status(env, api, auth, level, 'spider-man_heart_gwen_stacey')

    assert response.status_code == 400


@pytest.mark.exception
def test_plans_get_status_no_id(env, api, auth, level):
    """
    Test to validate that we get an error when passing no ID to GET/plans/status

    return: None
    """

    # We are calling plans_get_by_id so we don't end up with /plans//status
    # in the URL.  Using this method, we will end up with /plans/status
    plan_id = "status"
    response = plans_get_by_id(env, api, auth, level, plan_id)

    # Left in on purpose
    print("\n" + response.url)

    assert response.status_code == 400


@pytest.mark.functionality
@pytest.mark.smoke
def test_plans_get_response_data_validation(env, api, auth, level, short):
    """
    Test to validate that the stepname is updated correctly.
    Test to validate we can receive data from s3_presigned_URL
    Test to validate s3_presigned_URL expires after ten minutes

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

