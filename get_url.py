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
        url = "https://logistics.dev.agco-fuse-services.com/" + api + '/'
    elif env == 'stg':
        url = "https://logistics.stg.agco-fuse-services.com/" + api + '/'
    elif env == 'prod':
        url = "https://logistics.agco-fuse-services.com/" + api + '/'
    else:
        logger.error("Should not get here: get_url.py:23")
        exit(22)

    logger.debug(url)

    return url


if __name__ == "__main__":
    get_url("stg", "v1alpha1")
