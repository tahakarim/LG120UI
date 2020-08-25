import json
import logging
import pytest
import random
import params
import helpers
import requests
from datetime import datetime
from plans_endpoint import plans_get, plans_get_by_id, plans_get_status, plans_post_payload
from statistics import median, stdev
from slack import post_message_to_slack
from copy import deepcopy
from time import sleep


@pytest.mark.performance
def test_plans_get_response_performance(env, api, auth, level):
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


@pytest.mark.performance
def test_plans_get_by_id_response_performance(env, api, auth, level):
    """
    Test to validate the response time of GET /plans by id over multiple iterations.

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
    Test to validate the response time of GET /plans by status over multiple iterations.

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


@pytest.mark.performance
def test_plans_post_performance(env, api, auth, level):
    """
      Test to validate if field creation slows under stress

      return: None
    """
    setup_plan_id = []
    for i in range(5):
        payload = deepcopy(params.payload)
        payload['field']['boundary']['boundary'] = params.three_hundred_acre_field
        payload['field']['gates'][0]['point'] = helpers.helper_random_gate(payload['field']['boundary']['boundary'][0],
                                                                           payload['field']['boundary']['boundary'][2])
        payload['row_direction'][0] = helpers.helper_random_fieldpoint(payload['field']['boundary']['boundary'][0],
                                                                       payload['field']['boundary']['boundary'][2])
        payload['row_direction'][1] = helpers.helper_random_fieldpoint(payload['field']['boundary']['boundary'][1],
                                                                       payload['field']['boundary']['boundary'][3])

        payload = json.dumps(payload)
        response = plans_post_payload(env, api, auth, level, payload)
        assert response.status_code == 200
        json_response = response.json()

        plan_id = json_response['plan_id']
        setup_plan_id.append(plan_id)
        sleep(30)

    for plan_id in setup_plan_id:

        # Check to see if finished
        response = plans_get_by_id(env, api, auth, level, plan_id)
        assert response.status_code == 200
        json_response = response.json()
        print("Processing Setup ID: {0}".format(plan_id))

        while json_response['status']['is_complete'] is False:
            sleep(1)
            response = plans_get_by_id(env, api, auth, level, plan_id)
            assert response.status_code == 200
            json_response = response.json()

    print("Starting Test")

    payload = deepcopy(params.payload)
    payload['field']['boundary']['boundary'] = params.three_hundred_acre_field
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
    list_missed_compare_id = []
    output_data = []

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
            list_of_failed_id.append((plan_id, json_response['status']['step_name']))
            continue

        # Check to see body matches baseline
        s3_url_data = requests.get(json_response['s3_presigned_url'])
        assert s3_url_data.status_code == 200
        s3_url_data = s3_url_data.json()

        if s3_body_baseline != s3_url_data['body']['partition']:
            list_missed_compare_id.append(plan_id)

        # Store off time delta
        milli_created = datetime.strptime(json_response['created_date'], delta_time_format).timestamp() * 1
        milli_updated = datetime.strptime(json_response['updated_date'], delta_time_format).timestamp() * 1
        delta_milliseconds = milli_updated - milli_created

        list_of_time_delta.append(delta_milliseconds)

        output_data.append((plan_id, json_response['created_date'], json_response['updated_date'], delta_milliseconds))
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
    for i in output_data:
        print("{0}, {1}, {2}, {3}".format(i[0], i[1], i[2], i[3]))

    if len(list_of_failed_id) > 0:
        print("Number of Failed ID's: {0}".format(len(list_of_failed_id)))
        print("Failed ID's: {0}".format(list_of_failed_id))

    if len(list_missed_compare_id) > 0:
        print("Number of missed compare partitions: {0}".format(len(list_missed_compare_id)))
        print("Missed compare partitions: {0}".format(list_missed_compare_id))
