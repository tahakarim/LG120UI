import base64
import boto3
import params
import logging
import requests
import urllib3
import random
from datetime import datetime, timedelta


def oauth(env, auth):
    """
    Function to get the oauth2 tokens

    :param env: Which environment type to run (default: 'stg')
    :type auth: str

    :param auth: Which oauth type to run (default: 'aaa')
    :type auth: str

    :return: access token
    :rtype: str
    """

    logger = logging.getLogger('api_testing')
    myvar = auth
    if myvar == 'aaat' or myvar == 'aaa':

        if params.token is None or datetime.now() > params.expire_time:
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

            aaat_cookie = 'AWSALB=cEMzoYTtYFhoLsCCNO+oqb0aI7avscnTWjxtgrKgXbm9o9x' \
                '4X2OgYT3pCblachhSaxPsC1dmZaQUFh9jvTslBZV2twcZ4OBwdxXsfoI/wNkS4kF' \
                '/hjLjDK3+SJV2; AWSALBCORS=cEMzoYTtYFhoLsCCNO+oqb0aI7avscnTWjxtgr' \
                'KgXbm9o9x4X2OgYT3pCblachhSaxPsC1dmZaQUFh9jvTslBZV2twcZ4OBwdxXsfo' \
                'I/wNkS4kF/hjLjDK3+SJV2'
            aaa_cookie = 'AWSALB=VSJ7d3ACoeYV6L4FHoQWkVHzBMfLusd/Qt/EHAGL8P+FyORA' \
                'ZoEmhrQ2v0AuIEz89JPPAoiTt+oXlv2LEnwvZPsPUAVemGFRbj4C7yPLRBYT1+TB' \
                'yNPscZwpnFzv; AWSALBCORS=VSJ7d3ACoeYV6L4FHoQWkVHzBMfLusd/Qt/EHAG' \
                'L8P+FyORAZoEmhrQ2v0AuIEz89JPPAoiTt+oXlv2LEnwvZPsPUAVemGFRbj4C7yP' \
                'LRBYT1+TByNPscZwpnFzv'
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

            token = params.token = json_response['access_token']
            # Set the token expire time to 50 minutes instead of 1 hour to avoid
            # race conditions
            params.expire_time = datetime.now() + timedelta(minutes=50)

            return token

        else:
            token = params.token

            return token
    else:
        # Step 1
        session = boto3.Session(profile_name=env)
        client = session.client('ssm')

        loginid = 'thor.' + env + '.fleet-logistics.gigya.loginId'
        password = 'thor.' + env + '.fleet-logistics.gigya.password'
        api_key = 'thor.' + env + '.fleet-logistics.gigya.apiKey'

        loginid = client.get_parameter(Name=loginid)
        loginid = loginid['Parameter']['Value']

        password = client.get_parameter(Name=password)
        password = password['Parameter']['Value']

        api_key = client.get_parameter(Name=api_key)
        api_key = api_key['Parameter']['Value']

        payload = {'apiKey': api_key, 'loginId': loginid, 'password': password, 'lang': 'en'}

        response = requests.get('https://gigya.agcocorp.com/accounts.login', params=payload)
        assert response.status_code == 200
        json_response = response.json()

        cookieValue = json_response['sessionInfo']['cookieValue']
        # Step 2

        payload = {'apiKey': api_key, 'expiration': '3600', 'login_token': cookieValue}
        response = requests.get('https://accounts.eu1.gigya.com/accounts.getJWT', params=payload)

        assert response.status_code == 200
        json_response = response.json()
        id_token = json_response['id_token']
        return id_token


if __name__ == "__main__":
    oauth('stg', 'aaa')
