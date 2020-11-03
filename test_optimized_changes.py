import json
import pytest
import params
import random
from plans_endpoint import plans_post_payload, plans_get_by_id
from copy import deepcopy
from time import sleep
import requests


@pytest.mark.exception
def test_plans_post_initial_wayline_lat_value_null(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field boundary boundary lat value is null

    return: None
    """
    value = None
    payload = deepcopy(params.payload_all_fields)

    payload['field']['boundary']['boundary'] = params.quarter_circle_field
    payload['field']['gates'][0]['point'] = payload['field']['boundary']['boundary'][3]
    payload['field']['initial_wayline'][0]['lat'] = value

    payload = json.dumps(payload)

    print(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected initial_wayline" \
                                       " parameter lat is required, but none was provided."


@pytest.mark.exception
def test_plans_post_initial_wayline_lng_value_null(env, api, auth, level):
    """
    Test to verify we receive a 400 status if the field boundary boundary lat value is null

    return: None
    """
    value = None

    payload = deepcopy(params.payload_all_fields)
    payload['field']['boundary']['boundary'] = params.quarter_circle_field
    payload['field']['gates'][0]['point'] = payload['field']['boundary']['boundary'][0]
    payload['field']['initial_wayline'][0]['lng'] = value

    payload = json.dumps(payload)

    print(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected initial_wayline" \
                                       " parameter lng is required, but none was provided."

@pytest.mark.exception
def test_plans_post_initial_wayline_lat_key_value_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if field unoptimized lat key value is null

    return: None
    """

    payload = deepcopy(params.payload_all_fields)

    payload['field']['boundary']['boundary'] = params.quarter_circle_field
    payload['field']['gates'][0]['point'] = payload['field']['boundary']['boundary'][0]

    del payload['field']['initial_wayline'][0]['lat']

    payload = json.dumps(payload)

    print(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected initial_wayline" \
                                       " parameter lat is required, but none was provided."


@pytest.mark.exception
def test_plans_post_initial_wayline_lng_key_value_missing(env, api, auth, level):
    """
    Test to verify we receive a 400 status if field unoptimized lng key value is missing

    return: None
    """

    payload = deepcopy(params.payload_all_fields)

    payload['field']['boundary']['boundary'] = params.quarter_circle_field
    payload['field']['gates'][0]['point'] = payload['field']['boundary']['boundary'][0]

    del payload['field']['initial_wayline'][0]['lng']

    payload = json.dumps(payload)

    print(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response["message"] == "Unable to create plan with invalid input: Expected initial_wayline" \
                                       " parameter lng is required, but none was provided."

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
    payload = deepcopy(params.payload_all_fields)
    payload['field']['boundary']['boundary'] = params.quarter_circle_field
    payload['field']['gates'][0]['point'] = payload['field']['boundary']['boundary'][0]

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
    assert json_response['optimized'] is not None, "Response: \n{0}".format(json_response)

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
    assert json_response['initial_wayline'] is not None, "Response: \n{0}".format(json_response)

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
    Test to validate optimized value is true if unoptimized wayline not passed in payload
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
    assert json_response['optimized'] is not None, "Response: \n{0}".format(json_response)

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
def test_plans_field_initial_wayline_single_value(env, api, auth, level):
    """
      Test to validate when you present a single value for initial_Wayline handled correctly

      return: None
      """

    payload = deepcopy(params.payload_all_fields)

    payload['field']['boundary']['boundary'] = params.quarter_circle_field
    payload['field']['gates'][0]['point'] = payload['field']['boundary']['boundary'][0]

    del payload['field']['initial_wayline'][1]

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


@pytest.mark.exception
def test_plans_field_initial_wayline_no_values(env, api, auth, level):
    """
      Test to validate when empty list value for initial_wayline field handled correctly

      return: None
      """

    payload = deepcopy(params.payload_all_fields)

    payload['field']['boundary']['boundary'] = params.quarter_circle_field
    payload['field']['gates'][0]['point'] = payload['field']['boundary']['boundary'][0]
    del payload['field']['initial_wayline'][0:2]

    payload = json.dumps(payload)
    print(payload)

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
    assert json_response['optimized'] is not None, "Response: \n{0}".format(json_response)

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
            assert 'initial_wayline' in json_response, "Response: \n{0}".format(json_response)
            assert isinstance(json_response['initial_wayline'], list), "Response: \n{0}".format(json_response)
            assert json_response['initial_wayline'] is not None, "Response: \n{0}".format(json_response)
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
            assert 'initial_wayline' in json_response, "Response: \n{0}".format(json_response)
            assert isinstance(json_response['initial_wayline'], list), "Response: \n{0}".format(json_response)
            assert json_response['initial_wayline'] is not None, "Response: \n{0}".format(json_response)
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
            assert 'initial_wayline' in json_response, "Response: \n{0}".format(json_response)
            assert isinstance(json_response['initial_wayline'], list), "Response: \n{0}".format(json_response)
            assert json_response['initial_wayline'] is not None, "Response: \n{0}".format(json_response)
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
            assert 'initial_wayline' in json_response, "Response: \n{0}".format(json_response)
            assert isinstance(json_response['initial_wayline'], list), "Response: \n{0}".format(json_response)
            assert json_response['initial_wayline'] is not None, "Response: \n{0}".format(json_response)
            assert json_response['s3_presigned_url'] is not None
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


@pytest.mark.exception
def test_plans_post_field_id_as_numeric_value(env, api, auth, level):
    """
    Test to ensure an error is returned when sending a field_id as numeric value

    return: None
    """

    payload = deepcopy(params.payload)
    payload['field_id'] = 12345
    payload['field']['boundary']['boundary'] = params.quarter_circle_field
    payload = json.dumps(payload)
    print(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response['message'] == "Unable to create plan with invalid input: Expected parameter field_id is " \
                                       "required as string type, but other was provided."


@pytest.mark.exception
def test_plans_post_field_id_as_bool_value(env, api, auth, level):
    """
    Test to ensure an error is returned when sending a field_id as boolean value

    return: None
    """
    field_list = [True, False]
    payload = deepcopy(params.payload)
    payload['field_id'] = random.choice(field_list)
    payload['field']['boundary']['boundary'] = params.quarter_circle_field
    payload = json.dumps(payload)
    print(payload)

    response = plans_post_payload(env, api, auth, level, payload)
    json_response = response.json()

    assert response.status_code == 400
    assert json_response['message'] == "Unable to create plan with invalid input: Expected parameter field_id is " \
                                       "required as string type, but other was provided."
