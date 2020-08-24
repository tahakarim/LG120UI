import logging
import requests
from get_url import get_url
from oauth import oauth
from requests_toolbelt.utils import dump


def plans_get(env, api, auth, level, page_num=None, page_size=None):
    """
    Function to run the get plans endpoint

    :param env: The environment to run in development 'dev', staging \
    'stg', or production 'prod' (default: 'dev')
    :type env: str

    :param api: The api version to run (default: 'v1alpha1')
    :type api: str

    :param auth: Which oauth type to run (default: 'aaa')
    :type auth: str

    :param level:
    :type level: str

    :param page_num:
    :type page_num: int

    :param page_size:
    :type page_size: int

    :return: the requests object
    :rtype: list
    """

    logger = logging.getLogger('api_testing')
    logger.setLevel(level)

    access_token = oauth(env, auth)
    logger.debug("Response_Token: {0}".format(access_token))

    url = get_url(env, api) + 'plans'
    logger.debug(url)

    #if env != 'dev':
    #    payload = 'ctf=true&field_id=1&operation_type=%22Hello%20World%22&' \
    #            'vehicle_configuration=false&partition_configuration=true&' \
    #            'route_configuration=%22straight%22&soil_mositure=%22wet%22'
    #else:
    #    payload = "{" \
    #                "\"ctf\": true," \
    #                "\"field_id\": 1," \
    #                "\"operation_type\": \"test\"," \
    #                "\"vehicle_configurations\": true," \
    #                "\"partition_configuration\": true," \
    #                "\"route_configuration\": \"yep\"," \
    #                "\"soil_moisture\": \"wet\" " \
    #              "}"
    headers = {'Authorization': 'Bearer ' + access_token
              }

    if page_num != None and page_size != None:
        params = {'page': page_num,
                  'size': page_size
                 }
    elif page_num != None:
        params = {'page': page_num}
    elif page_size != None:
        params = {'size': page_size}
    else:
        params = {}

    response = requests.get(url, headers=headers, params=params)
    data = dump.dump_all(response)
    logger.debug(data.decode('utf-8'))

    return response


def plans_post_payload(env, api, auth, level, payload):
    """
    Function to run the post plans endpoint with custom payloads

    :param env: The environment to run in development 'dev', staging \
    'stg', or production 'prod' (default: 'dev')
    :type env: str

    :param api: The api version to run (default: 'v1alpha1')
    :type api: str

    :param auth: Which oauth type to run (default: 'aaa')
    :type auth: str

    :param level:
    :type level: str

    :param payload:
    :type level: dictionary

    :return: the requests object
    :rtype: object
    """

    logger = logging.getLogger('api_testing')
    logger.setLevel(level)

    access_token = oauth(env, auth)
    logger.debug("Response_Token: {0}".format(access_token))

    url = get_url(env, api) + 'plans'

    headers = {'Authorization': 'Bearer ' + access_token}

    response = requests.post(url, headers=headers, data=payload)
    data = dump.dump_all(response)
    logger.debug(data.decode('utf-8'))

    return response


def plans_get_by_id(env, api, auth, level, id, page_num=None, page_size=None):
    """
    Function to run the get plans with an ID endpoint

    :param env: The environment to run in development 'dev', staging \
    'stg', or production 'prod' (default: 'dev')
    :type env: str

    :param api: The api version to run (default: 'v1alpha1')
    :type api: str

    :param auth: Which oauth type to run (default: 'aaa')
    :type auth: str

    :param level:
    :type level: str

    :param id: The plan ID that should be returned.
    :type level: str

    :param page_num:
    :type page_num: int

    :param page_size:
    :type page_size: int

    :return: the requests object
    :rtype: list
    """

    logger = logging.getLogger('api_testing')
    logger.setLevel(level)

    access_token = oauth(env, auth)
    logger.debug("Response_Token: {0}".format(access_token))

    url = get_url(env, api) + 'plans/' + id
    logger.debug(url)
    headers = {'Authorization': 'Bearer ' + access_token}

    if page_num != None and page_size != None:
        params = {'page': page_num,
                  'size': page_size
                 }
    elif page_num != None:
        params = {'page': page_num}
    elif page_size != None:
        params = {'size': page_size}
    else:
        params = {}

    response = requests.get(url, headers=headers, params=params)
    data = dump.dump_all(response)
    logger.debug(data.decode('utf-8'))

    return response


def plans_get_status(env, api, auth, level, id, page_num=None, page_size=None):
    """
    Function to run the get plans status endpoint

    :param env: The environment to run in development 'dev', staging \
    'stg', or production 'prod' (default: 'dev')
    :type env: str

    :param api: The api version to run (default: 'v1alpha1')
    :type api: str

    :param auth: Which oauth type to run (default: 'aaa')
    :type auth: str

    :param level:
    :type level: str

    :param id: The plan ID that should be returned.
    :type level: str

    :param page_num:
    :type page_num: int

    :param page_size:
    :type page_size: int

    :return: the requests object
    :rtype: list
    """

    logger = logging.getLogger('api_testing')
    logger.setLevel(level)

    access_token = oauth(env, auth)
    logger.debug("Response_Token: {0}".format(access_token))

    url = get_url(env, api) + 'plans/' + id + '/status'
    logger.debug(url)

    headers = {'Authorization': 'Bearer ' + access_token}

    if page_num != None and page_size != None:
        params = {'page': page_num,
                  'size': page_size
                 }
    elif page_num != None:
        params = {'page': page_num}
    elif page_size != None:
        params = {'size': page_size}
    else:
        params = {}

    response = requests.get(url, headers=headers, params=params)
    data = dump.dump_all(response)
    logger.debug(data.decode('utf-8'))

    return response


def get_swagger(env, api, auth, level):
    """
        Function to get the swagger JSON

        :param env: The environment to run in development 'dev', staging \
        'stg', or production 'prod' (default: 'dev')
        :type env: str

        :param api: The api version to run (default: 'v1alpha1')
        :type api: str

        :param auth: Which oauth type to run (default: 'aaa')
        :type auth: str

        :param level:
        :type level: str

        :return: the requests object
        :rtype: list
        """
    logger = logging.getLogger('api_testing')
    logger.setLevel(level)

    access_token = oauth(env, auth)
    logger.debug("Response_Token: {0}".format(access_token))

    url = get_url(env, api)
    logger.debug(url)
    headers = {'Authorization': 'Bearer ' + access_token}

    response = requests.get(url, headers=headers)
    data = dump.dump_all(response)
    logger.debug(data.decode('utf-8'))

    return response


if __name__ == "__main__":
    #plans_post()
    plans_get("dev", "v1alpha1", "aaat", "INFO")