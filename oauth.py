import base64
import boto3
import json
import logging
import requests
import urllib3


def oauth(env, auth):
    """
    Function to get the oauth2 tokens

    :param auth: Which oauth type to run (default: 'aaa')
    :type auth: str

    :return: json object of tokens and other data
    :rtype: JSON
    """

    logger = logging.getLogger('api_testing')

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    session = boto3.Session(profile_name=env)
    client = session.client('ssm')

    if auth == 'aaa':
        uname = 'thor.' + env + '.fleet-logistics.forgerock.username'
        pword = 'thor.' + env + '.fleet-logistics.forgerock.password'
        c_id = 'thor.' + env + '.fleet-logistics.forgerock.clientid'
        c_secret = 'thor.' + env + '.fleet-logistics.forgerock.clientsecret'
        turl = 'thor.' + env + '.fleet-logistics.forgerock.url'
    elif auth == 'aaat':
        uname = 'thor.' + env + '.fleet-logistics.forgerock.aaat.username'
        pword = 'thor.' + env + '.fleet-logistics.forgerock.aaat.password'
        c_id = 'thor.' + env + '.fleet-logistics.forgerock.aaat.clientid'
        c_secret = 'thor.' + env + \
                   '.fleet-logistics.forgerock.aaat.clientsecret'
        turl = 'thor.' + env + '.fleet-logistics.forgerock.aaat.url'
    else:
        logger.error('Should not be here.  oauth.py:31')
        exit(1)

    logger.debug(uname)
    user_name_json = client.get_parameter(Name=uname)
    logger.debug(user_name_json['Parameter']['Value'])

    password_json = client.get_parameter(Name=pword, WithDecryption=True)
    logger.debug(password_json)
    logger.debug(password_json['Parameter']['Value'])

    id_json = client.get_parameter(Name=c_id, WithDecryption=True)
    client_id = id_json['Parameter']['Value']
    logger.debug(id_json['Parameter']['Value'])

    secret_json = client.get_parameter(Name=c_secret, WithDecryption=True)
    client_secret = secret_json['Parameter']['Value']
    logger.debug(secret_json['Parameter']['Value'])

    url_json = client.get_parameter(Name=turl)
    logger.debug(url_json['Parameter']['Value'])

    client_combo = client_id + ":" + client_secret

    encode = base64.b64encode(client_combo.encode("ascii"))
    logging.debug(encode)


    aaat_cookie = 'AWSALB=cEMzoYTtYFhoLsCCNO+oqb0aI7avscnTWjxtgrKgXbm9o9x4X' \
            '2OgYT3pCblachhSaxPsC1dmZaQUFh9jvTslBZV2twcZ4OBwdxXsfoI/wNkS4kF/h' \
            'jLjDK3+SJV2; AWSALBCORS=cEMzoYTtYFhoLsCCNO+oqb0aI7avscnTWjxtgrKg' \
            'Xbm9o9x4X2OgYT3pCblachhSaxPsC1dmZaQUFh9jvTslBZV2twcZ4OBwdxXsfoI/' \
            'wNkS4kF/hjLjDK3+SJV2'
    aaa_cookie = 'AWSALB=VSJ7d3ACoeYV6L4FHoQWkVHzBMfLusd/Qt/EHAGL8P+FyORAZoEm' \
                 'hrQ2v0AuIEz89JPPAoiTt+oXlv2LEnwvZPsPUAVemGFRbj4C7yPLRBYT1+T' \
                 'ByNPscZwpnFzv; AWSALBCORS=VSJ7d3ACoeYV6L4FHoQWkVHzBMfLusd/Q' \
                 't/EHAGL8P+FyORAZoEmhrQ2v0AuIEz89JPPAoiTt+oXlv2LEnwvZPsPUAVe' \
                 'mGFRbj4C7yPLRBYT1+TByNPscZwpnFzv'
    payload = 'username=' + user_name_json['Parameter']['Value'] + '&' \
              'password=' + password_json['Parameter']['Value'] + \
              '&grant_type=password&scope=telemetry.read+equipment.' \
              'read+device.read'
    aaat_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Authorization': 'Basic ' + encode.decode(),
                   'Cache-Control': 'no-cache',
                   'accept': '*/*',
                   'Cookie': aaat_cookie
                   }
    aaa_headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Authorization': 'Basic ' + encode.decode(),
                   'Cookie': aaa_cookie
                   }


    if auth == 'aaat':
        url = "https://aaat.agcocorp.com/auth/oauth2/fuse/access_token"
        headers = aaat_headers
    elif auth == 'aaa':
        url = "https://aaa.agcocorp.com/auth/oauth2/fuse/access_token"
        headers = aaa_headers
    else:
        logger.error("Should not get here: oauth.py:65")
        exit(22)

    response = requests.post(url_json['Parameter']['Value'],
                             headers=headers, data=payload, verify=False)
    json_response = response.json()

    return json_response


if __name__ == "__main__":
    oauth('stg', 'aaa')
