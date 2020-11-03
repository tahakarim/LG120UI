import json
import logging
import pytest
import params
import requests
from plans_endpoint import plans_get, plans_get_by_id, plans_get_status, plans_post_payload
from copy import deepcopy
from time import sleep


@pytest.mark.skipif(params.global_api == 'v1alpha1', reason="Not supported in api version: {0}".format(
    params.global_api))
@pytest.mark.exception
def test_plans_get_deprecation_failure(env, api, auth, level):
    """
    Test to verify GET/plans returns a 400 after v1alpha1.

    return: None
    """

    logger = logging.getLogger('api_testing')
    logger.setLevel(level)

    response = plans_get(env, api, auth, level)

    assert response.status_code == 403


@pytest.mark.functionality
@pytest.mark.smoke
def test_plans_get_by_id_response_validation(env, api, auth, level):
    """
    Test to validate that we are returning one status and that it is the correct status

    return: None
    """
    # Request to get a single ID response
    response = plans_get_by_id(env, api, auth, level, params.test_plan_id)
    json_response = response.json()

    assert response.status_code == 200

    # Validating we get 1 response back
    assert type(json_response) is not list

    # Validating plan_id equals what was requested
    assert json_response['plan_id'] == params.test_plan_id


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
    response = plans_get_by_id(env, api, auth, level, params.test_plan_id)
    json_response = response.json()

    assert response.status_code == 200

    # Grab a status update date and save off the status updated_date
    status_updated_date = json_response['status']['updated_date']

    # Request to get a single ID response
    response = plans_get_status(env, api, auth, level, params.test_plan_id)
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

@pytest.mark.exception
def test_plans_get_status_empty_id(env, api, auth, level):
    """
    Test to validate that we get an error when passing an empty ID to GET/plans/status

    return: None
    """
    plan_id = ""
    response = plans_get_status(env, api, auth, level, plan_id)

    # Left in on purpose
    print("\n" + response.url)

    assert response.status_code == 400


@pytest.mark.functionality
@pytest.mark.smoke
def test_plans_get_response_data_validation_with_initial_wayline(env, api, auth, level, short):
    """
    Test to validate that the stepname is updated correctly.
    Test to validate optimized value is false if unoptimized wayline passed in payload
    Test to validate we can receive data from s3_presigned_URL
    Test to validate s3_presigned_URL expires after ten minutes

    return: None
    """
    payload = deepcopy(params.payload)
    payload['field']['boundary']['boundary'] = params.quarter_circle_field

    payload['field']['initial_wayline'] = []
    payload['field']['initial_wayline'].append(payload['field']['boundary']['boundary'][0])
    payload['field']['initial_wayline'].append(payload['field']['boundary']['boundary'][1])

    initial_wayline_value = payload['field']['initial_wayline']
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

    assert 'plan_id' in json_response, "Response: \n{0}".format(json_response)
    assert isinstance(json_response['plan_id'], str), "Response: \n{0}".format(json_response)
    assert json_response['plan_id'] is not None, "Response: \n{0}".format(json_response)

    assert 'field_id' in json_response, "Response: \n{0}".format(json_response)
    assert isinstance(json_response['field_id'], str), "Response: \n{0}".format(json_response)
    assert json_response['field_id'] is not None, "Response: \n{0}".format(json_response)

    assert 'created_date' in json_response, "Response: \n{0}".format(json_response)
    assert isinstance(json_response['created_date'], str), "Response: \n{0}".format(json_response)
    assert json_response['created_date'] is not None, "Response: \n{0}".format(json_response)

    assert 'updated_date' in json_response, "Response: \n{0}".format(json_response)
    assert isinstance(json_response['updated_date'], str), "Response: \n{0}".format(json_response)
    assert json_response['updated_date'] is not None, "Response: \n{0}".format(json_response)

    assert 'optimized' in json_response, "Response: \n{0}".format(json_response)
    assert isinstance(json_response['optimized'], bool), "Response: \n{0}".format(json_response)
    assert json_response['optimized'] is False, "Response: \n{0}".format(json_response)

    assert 'is_complete' in json_response['status'], "Response: \n{0}".format(json_response)
    assert isinstance(json_response['status']['is_complete'], bool), "Response: \n{0}".format(json_response)
    assert json_response['status']['is_complete'] is not None, "Response: \n{0}".format(json_response)

    assert 'updated_date' in json_response['status'], "Response: \n{0}".format(json_response)
    assert isinstance(json_response['status']['updated_date'], str), "Response: \n{0}".format(json_response)
    assert json_response['status']['updated_date'] is not None, "Response: \n{0}".format(json_response)

    assert 'step_name' in json_response['status'], "Response: \n{0}".format(json_response)
    assert isinstance(json_response['status']['step_name'], str), "Response: \n{0}".format(json_response)
    assert json_response['status']['step_name'] is not None, "Response: \n{0}".format(json_response)

    assert 'has_error' in json_response['status'], "Response: \n{0}".format(json_response)
    assert isinstance(json_response['status']['has_error'], bool), "Response: \n{0}".format(json_response)
    assert json_response['status']['has_error'] is not None, "Response: \n{0}".format(json_response)

    assert 'initial_wayline' in json_response, "Response: \n{0}".format(json_response)
    assert isinstance(json_response['initial_wayline'], list), "Response: \n{0}".format(json_response)
    assert json_response['initial_wayline'] == initial_wayline_value, "Response: \n{0}".format(json_response)

    assert len(json_response) == 7
    assert len(json_response['status']) == 4


    assert json_response['plan_id'] == plan_id
    assert json_response['created_date'] == created_date

    started_validated = 0
    configure_plan_validated = 0
    generating_field_partitions_validated = 0
    saving_partition_validated = 0
    saved_partition_to_s3 = 0
    calculating_partition_kpis = 0
    calculated_partition_kpis = 0
    sleep_counter = 0

    # 60 seconds * number of minutes.
    max_sleep = 60 * 2
    status_updated_date = None

    while calculated_partition_kpis == 0 and sleep_counter <= max_sleep:

        if json_response['status']['step_name'] == "Started" and started_validated == 0:
            ''' This is step 1 validation'''
            assert json_response['status']['step_name'] == "Started"
            assert json_response['updated_date'] == json_response['status']['updated_date']
            status_updated_date = json_response['status']['updated_date']
            assert json_response['status']['has_error'] is False
            assert json_response['status']['is_complete'] is False
            assert json_response['optimized'] is False
            assert json_response['initial_wayline'] == initial_wayline_value, "Response: \n{0}".format(json_response)
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
            assert json_response['optimized'] is False
            assert json_response['initial_wayline'] == initial_wayline_value, "Response: \n{0}".format(json_response)
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
            assert json_response['optimized'] is False
            assert json_response['initial_wayline'] == initial_wayline_value, "Response: \n{0}".format(json_response)
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
            assert json_response['optimized'] is False
            assert json_response['initial_wayline'] == initial_wayline_value, "Response: \n{0}".format(json_response)
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
            assert json_response['status']['is_complete'] is False
            assert json_response['optimized'] is False
            assert json_response['initial_wayline'] == initial_wayline_value, "Response: \n{0}".format(json_response)
            assert 's3_presigned_url' in json_response, "Response: \n{0}".format(json_response)
            assert isinstance(json_response['s3_presigned_url'], str), "Response: \n{0}".format(json_response)
            assert json_response['s3_presigned_url'] is not None, "Response: \n{0}".format(json_response)

            # Validate no extra fields in response
            assert len(json_response) == 8

            # Verify the signed URL
            s3_url_data = requests.get(json_response['s3_presigned_url'])
            assert s3_url_data.status_code == 200
            s3_url_data_json = s3_url_data.json()

            assert 'partition' in s3_url_data_json['body'], "Response: \n{0}".format(s3_url_data_json)
            assert s3_url_data_json['body']['message'] == "Successfully generated a partition", \
                "Response: \n{0}".format(s3_url_data_json)

            saved_partition_to_s3 = 1
            print("Step: Saved partition to S3")
            sleep_counter = 0

        elif json_response['status']['step_name'] == "Calculating Partition KPIs" and calculating_partition_kpis == 0:
            ''' This is step 6 validation'''
            assert json_response['status']['step_name'] == "Calculating Partition KPIs"
            assert json_response['updated_date'] != created_date
            assert json_response['updated_date'] == json_response['status']['updated_date']
            assert json_response['updated_date'] != status_updated_date
            status_updated_date = json_response['status']['updated_date']
            assert json_response['status']['has_error'] is False
            assert json_response['status']['is_complete'] is False
            assert json_response['optimized'] is False
            assert json_response['initial_wayline'] == initial_wayline_value, "Response: \n{0}".format(json_response)
            assert json_response['s3_presigned_url'] is not None
            assert json_response['kpis'] == []

            calculating_partition_kpis = 1
            print("Step: Calculating Partition KPIs")
            sleep_counter = 0

        elif json_response['status']['step_name'] == "Calculated Partition KPIs" and calculated_partition_kpis == 0:
            ''' This is step 7 validation'''
            assert json_response['status']['step_name'] == "Calculated Partition KPIs"
            assert json_response['updated_date'] != created_date
            assert json_response['updated_date'] == json_response['status']['updated_date']
            assert json_response['updated_date'] != status_updated_date
            status_updated_date = json_response['status']['updated_date']
            assert json_response['status']['has_error'] is False
            assert json_response['status']['is_complete'] is True
            assert json_response['optimized'] is False
            assert json_response['s3_presigned_url'] is not None
            assert json_response['initial_wayline'] == initial_wayline_value, "Response: \n{0}".format(json_response)
            assert 'kpis' in json_response, "Response: \n{0}".format(json_response)
            assert isinstance(json_response['kpis'], list), "Response: \n{0}".format(json_response)
            assert json_response['kpis'] is not None, "Response: \n{0}".format(json_response)

            kpis = json_response['kpis']
            kpi_names = ['total_wayline_length', 'wayline_count', 'total_area', 'headland_area', 'overlapped_area',
                         'primary_area', 'perimeter', 'uncovered_area', 'covered_area']
            kpi_units_name = ['metres', 'square metres']

            for kpi in kpis:
                assert kpi['name'] in kpi_names, "Response: \n{0}".format(kpi)
                kpi_names.remove(kpi['name'])

                assert 'result' in kpi, "Response: \n{0}".format(kpi)
                assert isinstance(kpi['result'], dict), "Response: \n{0}".format(kpi)
                assert kpi['result'] is not None, "Response: \n{0}".format(kpi)

                result = kpi['result']

                assert 'value' in result, "Response: \n{0}".format(result)
                assert isinstance(result['value'], str), "Response: \n{0}".format(result)
                assert result['value'] is not None, "Response: \n{0}".format(result)

                if kpi['name'] != 'wayline_count':
                    assert isinstance(result['unit'], str), "Response: \n{0}".format(result)
                    assert result['unit'] in kpi_units_name, "Response: \n{0}".format(result)

            assert len(kpis) == 9, "Response: \n{0}".format(result)
            assert len(kpi_names) == 0, "Response: \n{0}".format(result)

            calculated_partition_kpis = 1
            print("Step: Calculated Partition KPIs")
            sleep_counter = 0

        sleep_counter += 1
        sleep(1)

        response = plans_get_by_id(env, api, auth, level, plan_id)
        json_response = response.json()

    assert sleep_counter < max_sleep, "Timeout Exceeded\n{0}".format(json_response)

    if saved_partition_to_s3 == 0:
        s3_url_data = requests.get(json_response['s3_presigned_url'])
        assert s3_url_data.status_code == 200
        s3_url_data_json = s3_url_data.json()

        assert 'partition' in s3_url_data_json['body'], "Response: \n{0}".format(s3_url_data_json)
        assert s3_url_data_json['body']['message'] == "Successfully generated a partition", \
            "Response: \n{0}".format(s3_url_data_json)

    ## Sleep for 10 minutes and 5 seconds to ensure s3 URL is dead.
    if short is False:
        sleep((60 * 10) + 5)
        s3_url_data = requests.get(json_response['s3_presigned_url'])
        assert s3_url_data.status_code == 403


@pytest.mark.functionality
@pytest.mark.smoke
def test_plans_get_response_data_validation_without_initial_wayline(env, api, auth, level, short):
    """
    Test to validate that the stepname is updated correctly.
    Test to validate optimized value is false if unoptimized wayline passed in payload
    Test to validate we can receive data from s3_presigned_URL
    Test to validate s3_presigned_URL expires after ten minutes

    return: None
    """
    payload = deepcopy(params.payload)
    payload['field']['boundary']['boundary'] = params.quarter_circle_field

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

    assert 'plan_id' in json_response, "Response: \n{0}".format(json_response)
    assert isinstance(json_response['plan_id'], str), "Response: \n{0}".format(json_response)
    assert json_response['plan_id'] is not None, "Response: \n{0}".format(json_response)

    assert 'field_id' in json_response, "Response: \n{0}".format(json_response)
    assert isinstance(json_response['field_id'], str), "Response: \n{0}".format(json_response)
    assert json_response['field_id'] is not None, "Response: \n{0}".format(json_response)

    assert 'created_date' in json_response, "Response: \n{0}".format(json_response)
    assert isinstance(json_response['created_date'], str), "Response: \n{0}".format(json_response)
    assert json_response['created_date'] is not None, "Response: \n{0}".format(json_response)

    assert 'updated_date' in json_response, "Response: \n{0}".format(json_response)
    assert isinstance(json_response['updated_date'], str), "Response: \n{0}".format(json_response)
    assert json_response['updated_date'] is not None, "Response: \n{0}".format(json_response)

    assert 'optimized' in json_response, "Response: \n{0}".format(json_response)
    assert isinstance(json_response['optimized'], bool), "Response: \n{0}".format(json_response)
    assert json_response['optimized'] is True, "Response: \n{0}".format(json_response)

    assert 'is_complete' in json_response['status'], "Response: \n{0}".format(json_response)
    assert isinstance(json_response['status']['is_complete'], bool), "Response: \n{0}".format(json_response)
    assert json_response['status']['is_complete'] is not None, "Response: \n{0}".format(json_response)

    assert 'updated_date' in json_response['status'], "Response: \n{0}".format(json_response)
    assert isinstance(json_response['status']['updated_date'], str), "Response: \n{0}".format(json_response)
    assert json_response['status']['updated_date'] is not None, "Response: \n{0}".format(json_response)

    assert 'step_name' in json_response['status'], "Response: \n{0}".format(json_response)
    assert isinstance(json_response['status']['step_name'], str), "Response: \n{0}".format(json_response)
    assert json_response['status']['step_name'] is not None, "Response: \n{0}".format(json_response)

    assert 'has_error' in json_response['status'], "Response: \n{0}".format(json_response)
    assert isinstance(json_response['status']['has_error'], bool), "Response: \n{0}".format(json_response)
    assert json_response['status']['has_error'] is not None, "Response: \n{0}".format(json_response)

    assert 'initial_wayline' in json_response, "Response: \n{0}".format(json_response)
    assert isinstance(json_response['initial_wayline'], list), "Response: \n{0}".format(json_response)
    assert json_response['initial_wayline'] == [], "Response: \n{0}".format(json_response)

    assert len(json_response) == 7
    assert len(json_response['status']) == 4

    assert json_response['plan_id'] == plan_id
    assert json_response['created_date'] == created_date

    started_validated = 0
    configure_plan_validated = 0
    generating_field_partitions_validated = 0
    saving_partition_validated = 0
    saved_partition_to_s3 = 0
    calculating_partition_kpis = 0
    calculated_partition_kpis = 0
    sleep_counter = 0

    # 60 seconds * number of minutes.
    max_sleep = 60 * 2
    status_updated_date = None

    while calculated_partition_kpis == 0 and sleep_counter <= max_sleep:

        if json_response['status']['step_name'] == "Started" and started_validated == 0:
            ''' This is step 1 validation'''
            assert json_response['status']['step_name'] == "Started"
            assert json_response['updated_date'] == json_response['status']['updated_date']
            status_updated_date = json_response['status']['updated_date']
            assert json_response['status']['has_error'] is False
            assert json_response['status']['is_complete'] is False
            assert json_response['optimized'] is True
            assert json_response['initial_wayline'] == [], "Response: \n{0}".format(json_response)
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
            assert json_response['optimized'] is True
            assert json_response['initial_wayline'] == [], "Response: \n{0}".format(json_response)
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
            assert json_response['optimized'] is True
            assert json_response['initial_wayline'] == [], "Response: \n{0}".format(json_response)
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
            assert json_response['optimized'] is True
            assert json_response['initial_wayline'] != [], "Response: \n{0}".format(json_response)
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
            assert json_response['status']['is_complete'] is False
            assert json_response['optimized'] is True
            assert json_response['initial_wayline'] != [], "Response: \n{0}".format(json_response)
            assert 's3_presigned_url' in json_response, "Response: \n{0}".format(json_response)
            assert isinstance(json_response['s3_presigned_url'], str), "Response: \n{0}".format(json_response)
            assert json_response['s3_presigned_url'] is not None, "Response: \n{0}".format(json_response)

            # Validate no extra fields in response
            assert len(json_response) == 8

            # Verify the signed URL
            s3_url_data = requests.get(json_response['s3_presigned_url'])
            assert s3_url_data.status_code == 200
            s3_url_data_json = s3_url_data.json()

            assert 'partition' in s3_url_data_json['body'], "Response: \n{0}".format(s3_url_data_json)
            assert s3_url_data_json['body']['message'] == "Successfully generated a partition", \
                "Response: \n{0}".format(s3_url_data_json)

            saved_partition_to_s3 = 1
            print("Step: Saved partition to S3")
            sleep_counter = 0

        elif json_response['status']['step_name'] == "Calculating Partition KPIs" and calculating_partition_kpis == 0:
            ''' This is step 6 validation'''
            assert json_response['status']['step_name'] == "Calculating Partition KPIs"
            assert json_response['updated_date'] != created_date
            assert json_response['updated_date'] == json_response['status']['updated_date']
            assert json_response['updated_date'] != status_updated_date
            status_updated_date = json_response['status']['updated_date']
            assert json_response['status']['has_error'] is False
            assert json_response['status']['is_complete'] is False
            assert json_response['optimized'] is True
            assert json_response['initial_wayline'] != [], "Response: \n{0}".format(json_response)
            assert json_response['s3_presigned_url'] is not None
            assert json_response['kpis'] == []

            calculating_partition_kpis = 1
            print("Step: Calculating Partition KPIs")
            sleep_counter = 0

        elif json_response['status']['step_name'] == "Calculated Partition KPIs" and calculated_partition_kpis == 0:
            ''' This is step 7 validation'''
            assert json_response['status']['step_name'] == "Calculated Partition KPIs"
            assert json_response['updated_date'] != created_date
            assert json_response['updated_date'] == json_response['status']['updated_date']
            assert json_response['updated_date'] != status_updated_date
            status_updated_date = json_response['status']['updated_date']
            assert json_response['status']['has_error'] is False
            assert json_response['status']['is_complete'] is True
            assert json_response['optimized'] is True
            assert json_response['s3_presigned_url'] is not None
            assert json_response['initial_wayline'] != [], "Response: \n{0}".format(json_response)
            assert 'kpis' in json_response, "Response: \n{0}".format(json_response)
            assert isinstance(json_response['kpis'], list), "Response: \n{0}".format(json_response)
            assert json_response['kpis'] is not None, "Response: \n{0}".format(json_response)

            kpis = json_response['kpis']
            kpi_names = ['total_wayline_length', 'wayline_count', 'total_area', 'headland_area', 'overlapped_area',
                         'primary_area', 'perimeter', 'uncovered_area', 'covered_area']
            kpi_units_name = ['metres', 'square metres']

            for kpi in kpis:
                assert kpi['name'] in kpi_names, "Response: \n{0}".format(kpi)
                kpi_names.remove(kpi['name'])

                assert 'result' in kpi, "Response: \n{0}".format(kpi)
                assert isinstance(kpi['result'], dict), "Response: \n{0}".format(kpi)
                assert kpi['result'] is not None, "Response: \n{0}".format(kpi)

                result = kpi['result']

                assert 'value' in result, "Response: \n{0}".format(result)
                assert isinstance(result['value'], str), "Response: \n{0}".format(result)
                assert result['value'] is not None, "Response: \n{0}".format(result)

                if kpi['name'] != 'wayline_count':
                    assert isinstance(result['unit'], str), "Response: \n{0}".format(result)
                    assert result['unit'] in kpi_units_name, "Response: \n{0}".format(result)

            assert len(kpis) == 9, "Response: \n{0}".format(result)
            assert len(kpi_names) == 0, "Response: \n{0}".format(result)

            calculated_partition_kpis = 1
            print("Step: Calculated Partition KPIs")
            sleep_counter = 0

        sleep_counter += 1
        sleep(1)

        response = plans_get_by_id(env, api, auth, level, plan_id)
        json_response = response.json()

    assert sleep_counter < max_sleep, "Timeout Exceeded\n{0}".format(json_response)

    if saved_partition_to_s3 == 0:
        s3_url_data = requests.get(json_response['s3_presigned_url'])
        assert s3_url_data.status_code == 200
        s3_url_data_json = s3_url_data.json()

        assert 'partition' in s3_url_data_json['body'], "Response: \n{0}".format(s3_url_data_json)
        assert s3_url_data_json['body']['message'] == "Successfully generated a partition", \
            "Response: \n{0}".format(s3_url_data_json)

    ## Sleep for 10 minutes and 5 seconds to ensure s3 URL is dead.
    if short is False:
        sleep((60 * 10) + 5)
        s3_url_data = requests.get(json_response['s3_presigned_url'])
        assert s3_url_data.status_code == 403


