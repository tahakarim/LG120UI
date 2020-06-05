import logging
import requests
from get_url import get_url
from oauth import oauth


def plans_post(env, api, auth, level):
    """
    Function to run the post plans endpoint

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
    :rtype: object
    """

    logger = logging.getLogger('api_testing')
    logger.setLevel(level)

    res_token = oauth(env, auth)
    logger.debug("Response_Token: {0}".format(res_token))
    access_token = res_token['access_token']

    url = get_url(env, api) + 'plans'

    if env != 'dev':
        payload = 'ctf=true&field_id=1&operation_type=%22Hello%20World%22&' \
                'vehicle_configuration=false&partition_configuration=true&' \
                'route_configuration=%22straight%22&soil_mositure=%22wet%22'
    else:
        payload = "{" \
                    "\"ctf\": true," \
                    "\"field_id\": 1," \
                    "\"operation_type\": \"test\"," \
                    "\"vehicle_configurations\": true," \
                    "\"partition_configuration\": true," \
                    "\"route_configuration\": \"yep\"," \
                    "\"soil_moisture\": \"wet\" " \
                  "}"
    headers = {'Content_Type': 'application/json',
               'Authorization': access_token
               }

    response = requests.post(url, headers=headers, data=payload)

    return response


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

    res_token = oauth(env, auth)
    logger.debug("Response_Token: {0}".format(res_token))
    access_token = res_token['access_token']

    url = get_url(env, api) + 'plans'

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
    headers = {'Content_Type': 'application/json',
               'Authorization': access_token
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

    return response



if __name__ == "__main__":
    plans_post()
    plans_get()