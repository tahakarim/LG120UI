import requests
import logging


def post_message_to_slack(text_incoming, level):
    """
    Function to send messages to the aether_test_alerts channel on slack

    :param text_incoming: Message to be printed on slack
    :type text_incoming: str

    :param level: debug level
    :type level: str

    :return: none
    :rtype: none
    """

    logger = logging.getLogger('api_testing')
    logger.setLevel(level)

    url = 'https://hooks.slack.com/services/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'
    headers = {'Content-type': 'application/json'}
    text = '{"text":"' + text_incoming + '"}'

    response = requests.post(url, headers=headers, data=text)
    logger.debug(response.request.body)
