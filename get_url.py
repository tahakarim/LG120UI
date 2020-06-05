import logging


def get_url(env, api):
    """
    Function to get the url to use to send api requests

    :param environment: The environment to run in development 'dev', staging \
    'stg', or production 'prod'
    :type environment: str

    :param version: The api version to run
    :type version: str

    :return: The url with the correct environment and versions strings
    :rtype: (str)
    """

    logger = logging.getLogger('api_testing')

    if env == 'dev':
        url = "https://6mtj5tibl2.execute-api.us-east-1.amazonaws.com/prod/"
    elif env == 'stg':
        url = "https://api.stg.agco-fuse-services.com/fleet-logistics/"
    elif env == 'prod':
        url = "https://api.agco-fuse-services.com/fleet-logistics/"
    else:
        logger.error("Should not get here: get_url.py:23")
        exit(22)

    if env != 'dev':
        url = url + api + '/'

    return url


if __name__ == "__main__":
    get_url()
