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
        ##url = "https://api.stg.agco-fuse-services.com/fleet-logistics/"
        url = "https://b9v0lf0vc8.execute-api.eu-west-1.amazonaws.com/Stage/"
    elif env == 'prod':
        ##url = "https://api.agco-fuse-services.com/fleet-logistics/"
        url = "https://z9launlk3h.execute-api.eu-west-1.amazonaws.com/stable/"
    else:
        logger.error("Should not get here: get_url.py:23")
        exit(22)

    logger.debug(url)
    #if env != 'dev':
    #    url = url + api + '/'

    return url


if __name__ == "__main__":
    get_url("stg", "v1alpha1")
