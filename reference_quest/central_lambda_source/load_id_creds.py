# Copyright 2022 Amazon.com and its affiliates; all rights reserved.
# This file is Amazon Web Services Content and may not be duplicated or distributed without permission.
import boto3
import os
import requests
from aws_gameday_quests.gdQuestsApi import GameDayQuestsApiClient
import urllib3
import json
import traceback

SUCCESS = "SUCCESS"
FAILED = "FAILED"

# Standard AWS GameDay Quests Environment Variables
QUEST_ID = os.environ['QUEST_ID']
QUEST_API_BASE = os.environ['QUEST_API_BASE']
QUEST_API_TOKEN = os.environ['QUEST_API_TOKEN']
GAMEDAY_REGION = os.environ['GAMEDAY_REGION']
ASSETS_BUCKET = os.environ['ASSETS_BUCKET']
ASSETS_BUCKET_PREFIX = os.environ['ASSETS_BUCKET_PREFIX']

http = urllib3.PoolManager()

def lambda_handler(event, context):
    try:
        print(f"event: {json.dumps(event)}")
        print(f"context: {str(context)}")

        response_data = {}

        if event['RequestType'] == 'Delete':
            try:
                send(event, context, SUCCESS, response_data)
                return
            except Exception as e:
                send(event, context, SUCCESS, response_data)    #TODO: SWITCH TO FAILED
                print(f"Custom resource lambda execution for delete has failed: {e}")
                traceback.print_exc()
                return
        else:  # request type is create or update
            try:
                ssm_client = boto3.client('ssm')  # get team's SSM client
                acct_vending_url = ssm_client.get_parameter(Name='AcctVending-LaunchDarklyUrl', WithDecryption=True)['Parameter']['Value']
                if acct_vending_url == 'DEV':
                    print("Acct Vending aborted since in DEV mode")
                    send(event, context, SUCCESS, response_data)

                acct_vending_key = ssm_client.get_parameter(Name='AcctVending-LaunchDarklyKey', WithDecryption=True)['Parameter']['Value']

                # Instantiate the Quest API Client.
                quests_api_client = GameDayQuestsApiClient(QUEST_API_BASE, QUEST_API_TOKEN)
                teams = quests_api_client.get_all_teams(QUEST_ID)

                # download all creds and distribute them across all teams
                acct_vending_headers = {
                    'Content-type': 'application/json',
                    'x-api-key': acct_vending_key
                }
                for team in teams['data']:
                    #team_data = quests_api_client.get_team(team_id=team['team-id'])
                    print(f"{team}")
                    team_table = team['table-number']

                    url = f"{acct_vending_url}/{team_table}"
                    print(f"Querying URL {url}")
                    acct_vending_resp = requests.get(url, headers=acct_vending_headers, timeout=60)
                    print("Response from assets vending endpoint: {}".format(str(acct_vending_resp)))
                    print("Response data from assets vending endpoint: {}".format(json.dumps(acct_vending_resp.text)))
                    launchdarkly_credentials = json.loads(acct_vending_resp.text)
                    print(f"Parsed response data: {json.dumps(launchdarkly_credentials)} ")

                    # upload team's LD credentials to their team account's SSM Parameter Store
                    xa_session = quests_api_client.assume_team_ops_role(team['team-id'])
                    xa_ssm_client = xa_session.client('ssm')  # get team's SSM client

                    try:
                        xa_ssm_client.get_parameter(Name='LD-ServerKey', WithDecryption=True)['Parameter']['Value']
                        xa_ssm_client.get_parameter(Name='LD-ClientKey', WithDecryption=True)['Parameter']['Value']
                        xa_ssm_client.get_parameter(Name='LD-SignInUrl', WithDecryption=True)['Parameter']['Value']
                        xa_ssm_client.get_parameter(Name='TableNumber', WithDecryption=True)['Parameter']['Value']
                        print(f"Acct Vending Credentials already loaded for team {team['team-id']}, ignoring...")
                    except Exception as e:
                        # only add if not already present
                        print(f"Acct Vending Credentials not found for team {team['team-id']}, loading them onto team acct SSM params...")
                        xa_ssm_client.put_parameter(Name='LD-ServerKey',
                                                    Description="LaunchDarkly Server key",
                                                    Value=launchdarkly_credentials['serverkey'],
                                                    Overwrite=True,
                                                    Tier="Standard",
                                                    Type="String",
                                                    DataType="text")
                        xa_ssm_client.put_parameter(Name='LD-ClientKey',
                                                    Description="LaunchDarkly Client key",
                                                    Value=launchdarkly_credentials['clientkey'],
                                                    Overwrite=True,
                                                    Tier="Standard",
                                                    Type="String",
                                                    DataType="text")
                        xa_ssm_client.put_parameter(Name='LD-SignOnUrl',
                                                    Description="LaunchDarkly SignOn URL",
                                                    Value=launchdarkly_credentials['signonurl'],
                                                    Overwrite=True,
                                                    Tier="Standard",
                                                    Type="String",
                                                    DataType="text")
                        xa_ssm_client.put_parameter(Name='TableNumber',
                                                    Description="Table Number of the Team",
                                                    Value=launchdarkly_credentials['table'],
                                                    Overwrite=True,
                                                    Tier="Standard",
                                                    Type="String",
                                                    DataType="text")


                print("Account Vending successful")

                send(event, context, SUCCESS, response_data)
                return
            except Exception as e:
                send(event, context, SUCCESS, response_data)        #TODO: SWITCH TO FAILED
                print(f"Lambda execution has failed! : {e}")
                traceback.print_exc()
                return

    except Exception as e:
        send(event, context, SUCCESS, {}, None)         #TODO: SWITCH TO FAILED
        print(f"Lambda execution has failed unexpectedly, unknown request type (probably a debugging code issue): {e}")
        traceback.print_exc()
        return


def send(event, context, responseStatus, responseData, physicalResourceId=None, noEcho=False, reason=None):
    responseUrl = event['ResponseURL']

    print(responseUrl)

    responseBody = {
        'Status': responseStatus,
        'Reason': reason or "See the details in CloudWatch Log Stream: {}".format(context.log_stream_name),
        'PhysicalResourceId': physicalResourceId or context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
        'NoEcho': noEcho,
        'Data': responseData
    }

    json_responseBody = json.dumps(responseBody)

    print("Response body:")
    print(json_responseBody)

    headers = {
        'content-type': '',
        'content-length': str(len(json_responseBody))
    }

    try:
        response = http.request('PUT', responseUrl, headers=headers, body=json_responseBody)
        print("Status code:", response.status)

    except Exception as e:
        print("send(..) failed executing http.request(..):", e)

