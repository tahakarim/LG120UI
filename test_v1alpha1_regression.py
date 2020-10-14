import json
import pytest
import params
import requests
import logging
from plans_endpoint import plans_get, plans_get_by_id, plans_post_payload, plans_get_status
from copy import deepcopy
from time import sleep
from statistics import median, stdev
from slack import post_message_to_slack
from plans_endpoint import get_swagger


@pytest.mark.v1alpha1_tests
@pytest.mark.skipif(params.global_api != 'v1alpha1', reason="Not supported in api version: {0}".format(
    params.global_api))
def test_plans_get_response_data_validation_v1alpha1(env, api, auth, level, short):
    """
    Test to validate that the stepname is updated correctly.
    Test to validate we can receive data from s3_presigned_URL
    Test to validate s3_presigned_URL expires after ten minutes

    return: None
    """
    payload = deepcopy(params.payload_optional)
    ### Temp Code
    # payload = json.dumps(payload)

    payload['field']['boundary']['boundary'] = params.quarter_circle_field
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

    assert len(json_response) == 5
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
            assert 's3_presigned_url' in json_response, "Response: \n{0}".format(json_response)
            assert isinstance(json_response['s3_presigned_url'], str), "Response: \n{0}".format(json_response)
            assert json_response['s3_presigned_url'] is not None, "Response: \n{0}".format(json_response)

            # Validate no extra fields in response
            assert len(json_response) == 6

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
            assert json_response['s3_presigned_url'] is not None
            assert 'kpis' in json_response, "Response: \n{0}".format(json_response)
            assert isinstance(json_response['kpis'], list), "Response: \n{0}".format(json_response)
            assert json_response['kpis'] is not None, "Response: \n{0}".format(json_response)

            kpis = json_response['kpis']

            assert kpis[0]['name'] == "wayline_count", "Response: \n{0}".format(kpis[0]['name'])
            assert kpis[1]['name'] == "headland_area", "Response: \n{0}".format(kpis[1]['name'])
            assert kpis[2]['name'] == "primary_area", "Response: \n{0}".format(kpis[2]['name'])

            for kpi in kpis:
                assert isinstance(kpi['name'], str), "Response: \n{0}".format(kpi)
                assert kpi['name'] is not None, "Response: \n{0}".format(kpi)

                assert 'result' in kpi, "Response: \n{0}".format(kpi)
                assert isinstance(kpi['result'], dict), "Response: \n{0}".format(kpi)
                assert kpi['result'] is not None, "Response: \n{0}".format(kpi)

                result = kpi['result']

                assert 'value' in result, "Response: \n{0}".format(result)
                assert isinstance(result['value'], str), "Response: \n{0}".format(result)
                assert result['value'] is not None, "Response: \n{0}".format(result)

                if 'unit' in result:
                    assert isinstance(result['unit'], str), "Response: \n{0}".format(result)
                    assert result['unit'] is not None, "Response: \n{0}".format(result)

            assert len(kpis) == 3

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


@pytest.mark.v1alpha1_tests
@pytest.mark.skipif(params.global_api != 'v1alpha1', reason="Not supported in api version: {0}".format(
    params.global_api))
def test_plans_get_response_kpi_validation_v1alpha1(env, api, auth, level):
    """
        Test to verify the kpi fields are correct in a plans get by id response. We will be validating the key exists,
        not NULL and correct type.

        return: None
        """

    response = plans_get_by_id(env, api, auth, level, params.test_plan_id)
    json_response = response.json()

    assert response.status_code == 200

    assert 'kpis' in json_response, "Response: \n{0}".format(json_response)
    assert isinstance(json_response['kpis'], list), "Response: \n{0}".format(json_response)
    assert json_response['kpis'] is not None, "Response: \n{0}".format(json_response)

    kpis = json_response['kpis']

    assert kpis[0]['name'] == "wayline_count", "Response: \n{0}".format(kpis[0]['name'])
    assert kpis[1]['name'] == "headland_area", "Response: \n{0}".format(kpis[1]['name'])
    assert kpis[2]['name'] == "primary_area", "Response: \n{0}".format(kpis[2]['name'])

    for kpi in kpis:
        assert isinstance(kpi['name'], str), "Response: \n{0}".format(kpi)
        assert kpi['name'] is not None, "Response: \n{0}".format(kpi)

        assert 'result' in kpi, "Response: \n{0}".format(kpi)
        assert isinstance(kpi['result'], dict), "Response: \n{0}".format(kpi)
        assert kpi['result'] is not None, "Response: \n{0}".format(kpi)

        result = kpi['result']

        assert 'value' in result, "Response: \n{0}".format(result)
        assert isinstance(result['value'], str), "Response: \n{0}".format(result)
        assert result['value'] is not None, "Response: \n{0}".format(result)

        if 'unit' in result:
            assert isinstance(result['unit'], str), "Response: \n{0}".format(result)
            assert result['unit'] is not None, "Response: \n{0}".format(result)

    assert len(kpis) == 3


@pytest.mark.skipif(params.global_api != 'v1alpha1', reason="Not supported in api version: {0}".format(
    params.global_api))
@pytest.mark.v1alpha1_tests
def test_plans_get_response_validation_v1alpha1(env, api, auth, level):
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


@pytest.mark.skipif(params.global_api != 'v1alpha1', reason="Not supported in api version: {0}".format(
    params.global_api))
@pytest.mark.v1alpha1_tests
def test_plans_get_response_at_least_one_plan_id_returned_v1alpha1(env, api, auth, level):
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


@pytest.mark.v1alpha1_tests
@pytest.mark.skipif(params.global_api != 'v1alpha1', reason="Not supported in api version: {0}".format(
    params.global_api))
def test_plans_get_by_id_response_validation_v1alpha1(env, api, auth, level):
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


@pytest.mark.v1alpha1_tests
@pytest.mark.skipif(params.global_api != 'v1alpha1', reason="Not supported in api version: {0}".format(
    params.global_api))
def test_plans_get_status_response_validation_v1alpha1(env, api, auth, level):
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


@pytest.mark.skipif(params.global_api != 'v1alpha1', reason="Not supported in api version: {0}".format(
    params.global_api))
def test_plans_get_response_performance_v1alpha1(env, api, auth, level):
    """
    Test to validate the response time of GET /plans over multiple iterations.

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


@pytest.mark.v1alpha1_tests
@pytest.mark.skipif(params.global_api != 'v1alpha1', reason="Not supported in api version: {0}".format(
    params.global_api))
def test_plans_post_response_validation_v1alpha1(env, api, auth, level):
    """
    Test to verify the fields are correct in a plans post response. We will be validating the key exists,
    not NULL and correct type.

    return: None
    """
    payload = deepcopy(params.payload_optional)
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


@pytest.mark.v1alpha1_tests
@pytest.mark.skipif(params.global_api != 'v1alpha1', reason="Not supported in api version: {0}".format(
    params.global_api))
def test_swagger_response_validation(env, api, auth, level):
    """
    Test to verify the swagger call returns a 200 response and the JSON has not changed

    return: None
    """
    golden_v1alpha1_swagger = {"swagger": "2.0", "info": {"version": "1.0", "title": "THOR-FLEET-LOGISTICS-API-V1ALPHA1"}, "host": "logistics.dev.agco-fuse-services.com", "basePath": "/v1alpha1", "schemes": ["https"], "paths": {"/plans": {"get": {"summary": "List of plans", "description": "Returns a list of plans", "parameters": [{"in": "header", "name": "Authorization", "type": "string", "format": "Bearer", "required": True}], "responses": {"200": {"description": "OK", "schema": {"type": "array", "items": {"type": "object", "properties": {"plan_id": {"type": "string", "example": "f9c16062-e866-4fb0-a720-78234d9d8d19"}, "field_id": {"type": "string", "example": "67890"}, "created_date": {"type": "string", "example": "2020-04-10T20:24:32.938Z"}, "status": {"type": "object", "properties": {"has_error": {"type": "boolean", "example": False}, "is_complete": {"type": "boolean", "example": False}, "step_name": {"type": "string", "example": "Started"}, "updated_date": {"type": "string", "example": "2020-04-10T20:24:32.938Z"}}}, "updated_date": {"type": "string", "example": "2020-04-10T20:24:32.938Z"}}}}}, "403": {"description": "Forbidden", "schema": {"type": "object", "properties": {"message": {"type": "string", "example": "User is not authorized to access this resource with an explicit deny."}}}}, "500": {"description": "Internal Server Error", "schema": {"type": "object", "properties": {"message": {"type": "string", "example": "An error occurred while retrieving the plans."}}}}, "504": {"description": "Timeout Error", "schema": {"type": "object", "properties": {"plan_id": {"type": "string", "example": "f9c16062-e866-4fb0-a720-78234d9d8d19"}, "field_id": {"type": "string", "example": "67890"}, "created_date": {"type": "string", "example": "2020-04-10T20:24:32.938Z"}, "updated_date": {"type": "string", "example": "2020-04-10T20:24:32.938Z"}, "status": {"type": "object", "properties": {"has_error": {"type": "boolean", "example": True}, "is_complete": {"type": "boolean", "example": True}, "message": {"type": "string", "example": "An error has occurred in the workflow while generating a route for the requested field. The workflow has been updated accordingly and the process terminated"}, "step_name": {"type": "string", "example": "Saved partition to S3"}, "updated_date": {"type": "string", "example": "2020-04-10T20:24:32.938Z"}}}}}}}, "security": [{"LambdaTokenAuthorizer": []}], "x-amazon-apigateway-integration": {"uri": "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:878796470432:function:THOR-FLEET-LOGISTICS-API-FleetLogisticsGetAllPlan-NBXDLC0PMV6D/invocations", "passthroughBehavior": "when_no_match", "httpMethod": "POST", "type": "aws_proxy"}}, "post": {"summary": "Create new plan", "description": "Returns a plan_id and created date", "parameters": [{"in": "header", "name": "Authorization", "type": "string", "format": "Bearer", "required": True}, {"in": "body", "name": "Body", "schema": {"type": "object", "required": ["field_id"], "properties": {"field_id": {"type": "string", "example": "12345"}, "is_ctf": {"type": "boolean", "example": False}, "headland_width_optimized": {"type": "boolean", "example": False}, "headland_width": {"type": "integer", "example": 10}, "row_direction": {"type": "array", "items": {"type": "object", "properties": {"lat": {"type": "number", "example": 123}, "lng": {"type": "number", "example": 456}}}}, "constraints": {"type": "array", "items": {"type": "object", "properties": {"width": {"type": "number", "example": 10}, "priority": {"type": "number", "example": 1}, "turning_radius": {"type": "number", "example": 10}, "ramp_up_distance": {"type": "number", "example": 10}, "ramp_down_distance": {"type": "number", "example": 10}}}}, "field": {"type": "object", "properties": {"boundary": {"type": "object", "properties": {"boundary": {"type": "array", "items": {"type": "object", "properties": {"lat": {"type": "integer"}, "lng": {"type": "string"}}}, "example": [{"lat": 123, "lng": 456}, {"lat": 234, "lng": 567}, {"lat": 345, "lng": 678}, {"lat": 456, "lng": 789}]}}}, "gates": {"type": "array", "items": {"type": "object", "properties": {"point": {"type": "object", "properties": {"lat": {"type": "number", "example": 123}, "lng": {"type": "number", "example": 456}}}}}}, "soil_type": {"type": "string", "example": "Unknown"}}}}}}], "responses": {"200": {"description": "OK", "schema": {"type": "object", "properties": {"plan_id": {"type": "string", "example": "f9c16062-e866-4fb0-a720-78234d9d8d19"}, "created_date": {"type": "string", "example": "2020-04-10T20:24:32.938Z"}}}}, "400": {"description": "Bad Request", "schema": {"type": "object", "properties": {"message": {"type": "string", "example": "Unable to create plan with invalid input: Expected row_direction parameter lng is required, but none was provided."}}}}, "403": {"description": "Forbidden", "schema": {"type": "object", "properties": {"message": {"type": "string", "example": "User is not authorized to access this resource with an explicit deny."}}}}, "500": {"description": "Internal Server Error", "schema": {"type": "object", "properties": {"message": {"type": "string", "example": "Failed to create item."}}}}}, "security": [{"LambdaTokenAuthorizer": []}], "x-amazon-apigateway-integration": {"uri": "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:878796470432:function:THOR-FLEET-LOGISTICS-API-FleetLogisticsCreatePlan-125M0H87PDNOJ/invocations", "passthroughBehavior": "when_no_match", "httpMethod": "POST", "type": "aws_proxy"}}}, "/plans/{plan_id}": {"get": {"summary": "Retrieve a plan by plan_id", "description": "Returns a plan", "parameters": [{"in": "header", "name": "Authorization", "type": "string", "format": "Bearer", "required": True}, {"in": "path", "name": "plan_id", "type": "string", "required": True, "description": "UUID of the plan"}], "responses": {"200": {"description": "OK", "schema": {"type": "object", "properties": {"kpis": {"type": "array", "items": {"type": "object", "properties": {"name": {"type": "string"}, "result": {"type": "object", "properties": {"value": {"type": "string"}, "unit": {"type": "string"}}}}}, "example": [{"name": "wayline_count", "result": [{"value": "1"}]}, {"name": "headland_area", "result": [{"value": "39538.3054331367", "unit": "SquareMeters"}]}, {"name": "primary_area", "result": [{"value": "187881.14197863924", "unit": "SquareMeters"}]}]}, "plan_id": {"type": "string", "example": "f9c16062-e866-4fb0-a720-78234d9d8d19"}, "field_id": {"type": "string", "example": "67890"}, "created_date": {"type": "string", "example": "2020-04-10T20:24:32.938Z"}, "status": {"type": "object", "properties": {"has_error": {"type": "boolean", "example": False}, "is_complete": {"type": "boolean", "example": False}, "step_name": {"type": "string", "example": "Started"}, "updated_date": {"type": "string", "example": "2020-04-10T20:24:32.938Z"}}}, "updated_date": {"type": "string", "example": "2020-04-10T20:24:32.938Z"}, "s3_presigned_url": {"type": "string", "example": "https://thor-fleet-logistics-partitions-dev.s3.amazonaws.com/persisted-partitions/288b241d-af50-4330-953e-84ea6617fd39-partition.json?AWSAccessKeyId=ASIA4ZHCZ7CQDSFGHEGB&Signature=qwjChWGXYnb4UCgP91VoTV2KHgY%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEDIaCXVzLWVhc3QtMSJGMEQCIChohllkih%2BI%2FN2d9cAag6xIO06m7%2BDcXrnCRG73GO5EAiAjUgy4S0H6TZvK7Zae3HsQDnfa494tSelqDJOKy4X6wSr%2BAQgbEAEaDDg3ODc5NjQ3MDQzMiIMyDSBhtXn5pIiSbH9KtsBrb5w%2BLqWYQxwIHPU%2BmjAw0gc1N3Ir5n%2Fpn1SUYJB9ufZStBYvH6qnsUz7aHICkZGv74L%2BTEYu%2B6pGk5zI5qaPJKa9hg15Ij30pGxFnYUAPXnIspdFKfRT9JyK%2BhA10HoxEU8syNo3Z4i3mJhkxE4Cqa4c5I4y1hMBeyBOCGPA2V%2Bvr2E%2FkSVGS616SJJbORRtFr605el%2BhovpNq84QBVKJxG%2FLkJd0GlufRRworuPndCJg73CTSDBgSHNtYyrtyx9hK6e854igSI7g5Ua1wu6RKlRsrzzl9ye0k6MKql8PkFOuEBhHKoQz6dA6MsN9%2FxNB32tx2HOJwiU9i%2FnPdIgXpj0lwTc3RW418bpGA7zOkYvuHb9RsbI%2FkaCf5cIJLWOJYF7z1KBqXggJj7Iq89%2BtclhkrvD%2Ba3qvWMlJZ1YdPFfwXdY2EEvtiQAB0imZrLK68xdBfSH%2FeQaEAN1x7S9OQ6ZrNuxqQDBOdlbJkDCw1RctKhMXb95e2%2B9tj0BXE4s1rDjeYsJosckU6penCcpWXh4G9hqF6241145g7M3101%2Bwm4mSJ9KdCSIWgyXiUGYLXzxO3uek9MnnyCl1zNXAWmTdnu&Expires=1597773059"}}}}, "400": {"description": "Bad Request"}, "403": {"description": "Forbidden", "schema": {"type": "object", "properties": {"message": {"type": "string", "example": "User is not authorized to access this resource with an explicit deny."}}}}, "404": {"description": "Not Found", "schema": {"type": "object", "properties": {"message": {"type": "string", "example": "Could not find a plan with plan id f9c16062-e866-4fb0-a720-78234d9d8d19."}}}}, "500": {"description": "Internal Server Error", "schema": {"type": "object", "properties": {"message": {"type": "string", "example": "An error occurred while retrieving the plan with plan id f9c16062-e866-4fb0-a720-78234d9d8d195."}}}}, "504": {"description": "Timeout Error", "schema": {"type": "object", "properties": {"plan_id": {"type": "string", "example": "f9c16062-e866-4fb0-a720-78234d9d8d19"}, "field_id": {"type": "string", "example": "67890"}, "created_date": {"type": "string", "example": "2020-04-10T20:24:32.938Z"}, "updated_date": {"type": "string", "example": "2020-04-10T20:24:32.938Z"}, "status": {"type": "object", "properties": {"has_error": {"type": "boolean", "example": True}, "is_complete": {"type": "boolean", "example": True}, "message": {"type": "string", "example": "An error has occurred in the workflow while generating a route for the requested field. The workflow has been updated accordingly and the process terminated"}, "step_name": {"type": "string", "example": "Saved partition to S3"}, "updated_date": {"type": "string", "example": "2020-04-10T20:24:32.938Z"}}}}}}}, "security": [{"LambdaTokenAuthorizer": []}], "x-amazon-apigateway-integration": {"uri": "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:878796470432:function:THOR-FLEET-LOGISTICS-API-FleetLogisticsPlanByPlan-1XYB23PHPE3Q3/invocations", "passthroughBehavior": "when_no_match", "httpMethod": "POST", "type": "aws_proxy"}}}, "/plans/{plan_id}/status": {"get": {"summary": "Retrieve the status of a plan by plan_id", "description": "Returns status", "parameters": [{"in": "header", "name": "Authorization", "type": "string", "format": "Bearer", "required": True}, {"in": "path", "name": "plan_id", "type": "string", "required": True, "description": "UUID of the plan to get the status of."}], "responses": {"200": {"description": "OK", "schema": {"type": "object", "properties": {"has_error": {"type": "boolean", "example": True}, "is_complete": {"type": "boolean", "example": True}, "message": {"type": "string", "example": "An error has occurred in the workflow while generating a route for the requested field. The workflow has been updated accordingly and the process terminated"}, "step_name": {"type": "string", "example": "Saved partition to S3"}, "updated_date": {"type": "string", "example": "2020-04-10T20:24:32.938Z"}}}}, "400": {"description": "Bad Request"}, "403": {"description": "Forbidden", "schema": {"type": "object", "properties": {"message": {"type": "string", "example": "User is not authorized to access this resource with an explicit deny."}}}}, "404": {"description": "Not Found", "schema": {"type": "object", "properties": {"message": {"type": "string", "example": "Could not find a status with the plan id f9c16062-e866-4fb0-a720-78234d9d8d19."}}}}, "500": {"description": "Internal Server Error", "schema": {"type": "object", "properties": {"message": {"type": "string", "example": "An error occurred while retrieving the status with plan id f9c16062-e866-4fb0-a720-78234d9d8d19."}}}}, "504": {"description": "Timeout Error", "schema": {"type": "object", "properties": {"has_error": {"type": "boolean", "example": False}, "is_complete": {"type": "boolean", "example": False}, "message": {"type": "string", "example": "An error has occurred in the workflow while generating a route for the requested field. The workflow has been updated accordingly and the process terminated"}, "step_name": {"type": "string", "example": "Started"}, "updated_date": {"type": "string", "example": "2020-04-10T20:24:32.938Z"}}}}}, "security": [{"LambdaTokenAuthorizer": []}], "x-amazon-apigateway-integration": {"uri": "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:878796470432:function:THOR-FLEET-LOGISTICS-API-FleetLogisticsGetStatusF-1A27AM4FY3XHS/invocations", "passthroughBehavior": "when_no_match", "httpMethod": "POST", "type": "aws_proxy"}}}}, "securityDefinitions": {"LambdaTokenAuthorizer": {"type": "apiKey", "name": "Authorization", "in": "header", "x-amazon-apigateway-authtype": "custom", "x-amazon-apigateway-authorizer": {"authorizerUri": "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:878796470432:function:THOR-FLEET-LOGISTICS-API-V1ALPHA1-AuthFunction-IS6LV9F2G3UR/invocations", "authorizerResultTtlInSeconds": 300, "type": "token"}}}, "definitions": {"thor_fleet_logistics_plans": {"type": "object", "properties": {"plan_id": {"type": "string", "example": "07e2362c-033b-4b4c-8520-900bfdc9a5e7", "description": "The plan id of a plan."}, "field_id": {"type": "string", "example": "657", "description": "The field id of a plan."}, "created_date": {"type": "string", "example": "2020-07-23 19:50:43.289", "description": "The created date of a plan."}, "status": {"type": "object", "properties": {"has_error": {"type": "boolean", "example": False, "description": "Check if the status has an error."}, "is_complete": {"type": "boolean", "example": False, "description": "Check if the status is complete."}, "step_name": {"type": "string", "example": "Generating a partition", "description": "The current step name."}, "updated_date": {"type": "string", "example": "2020-07-23 19:50:43.289", "description": "The updated date of a status."}}, "title": "Status", "description": "The status of a plan."}, "updated_date": {"type": "string", "example": "2020-07-23 19:50:43.289", "description": "The updated date of a plan."}, "kpis": {"description": "The wayline_count, primary_area, and headland_area calculated in the PartitionKpiProducer step.", "type": "array", "items": {"type": "object", "properties": {"name": {"type": "string", "description": "The name of the kpi calculated."}, "result": {"type": "object", "properties": {"value": {"type": "string", "description": "The value of the kpi calculated."}, "unit": {"type": "string", "description": "The unit of the kpi calculated."}}}}}, "example": [{"name": "wayline_count", "result": [{"value": "1"}]}, {"name": "headland_area", "result": [{"value": "39538.3054331367", "unit": "SquareMeters"}]}, {"name": "primary_area", "result": [{"value": "187881.14197863924", "unit": "SquareMeters"}]}]}}, "title": "Plans", "description": "The details for a plan.", "required": ["plan_id", "field_id", "created_date", "status", "updated_date"]}}}

    if env == 'stg':
        golden_v1alpha1_swagger['host'] = golden_v1alpha1_swagger['host'].replace('dev', 'stg', 1)

    elif env == 'prod':
        golden_v1alpha1_swagger['host'] = golden_v1alpha1_swagger['host'].replace('dev.', '', 1)

    response = get_swagger(env, api, auth, level)
    assert response.status_code == 200
    json_response = response.json()

    assert json_response == golden_v1alpha1_swagger
