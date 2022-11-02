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
TEAM_SSM_PARAMS_NEEDED=['LD-ServerKey','LD-ClientKey','LD-SignOnUrl','TableNumber']

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
                print(f"Custom resource lambda execution for delete has failed: {e}")
                traceback.print_exc()
                send(event, context, FAILED, response_data)
                return

        else:  # request type is create or update
            acct_vending_creds_found = False
            acct_vending_url = ""
            acct_vending_key = ""

            # CHECK FOR CENTRAL ACCT VENDING PARAMS
            try:
                # check whether the central Acct Vending params exist (needed only for EE events)
                ssm_client = boto3.client('ssm')  # get team's SSM client
                acct_vending_url = ssm_client.get_parameter(Name='AcctVending-LaunchDarklyUrl', WithDecryption=True)['Parameter']['Value']
                acct_vending_key = ssm_client.get_parameter(Name='AcctVending-LaunchDarklyKey', WithDecryption=True)['Parameter']['Value']
                print("Acct Vending params found")
                acct_vending_creds_found = True

            except ssm_client.exceptions.ParameterNotFound as e:
                # Dev environments don't require the central Acct Vending params,
                # so defer to check for local Team credentials SSM Params below
                print("Acct Vending params not present, checking for team credentials next in case this is a Dev environment")
            except Exception as e:
                print(f"Lambda execution has failed unexpectedly, unknown request type (probably a debugging code issue): {e}")
                traceback.print_exc()
                send(event, context, FAILED, {}, None)
                return

            # CHECK FOR TEAM CREDENTIALS
            try:
                # Instantiate the Quest API Client.
                quests_api_client = GameDayQuestsApiClient(QUEST_API_BASE, QUEST_API_TOKEN)
                teams = quests_api_client.get_all_teams(QUEST_ID)

                for team in teams['data']:
                    xa_session = quests_api_client.assume_team_ops_role(team['team-id'])
                    xa_ssm_client = xa_session.client('ssm')  # get team's SSM client

                    if all_team_cred_params_exist(xa_ssm_client):
                        print(f"All Team Acct Vending Credentials already loaded for team {team['team-id']}, skipping...")
                    else:
                        if not acct_vending_creds_found:
                            # No central Acct Vending credentials and this team is missing their Team Credentials!
                            print("****ABORTING PROCESSING****")
                            print("ACCOUNT VENDING/ENVIRONMENT NOT PROPERLY SET UP")
                            print(f"For EE Events: account vending credentials will need to be set up! PLEASE REFER TO THE OPERATOR GUIDE!")
                            print(f"For local development: the following Team Credentials are expected in SSM Parameter Store: {TEAM_SSM_PARAMS_NEEDED}")
                            print("****ABORTING PROCESSING****")
                            send(event, context, FAILED, {}, None, reason="ACCOUNT VENDING/ENVIRONMENT NOT PROPERLY SET UP, SSM Params missing!" )
                            return

                        else:
                            # EE: central acct vending set up but missing Team credentials => fetch team credentials
                            acct_vending_headers = {
                                'Content-type': 'application/json',
                                'x-api-key': acct_vending_key
                            }
                            team_table = team['table-number']
                            url = f"{acct_vending_url}/{team_table}"
                            print(f"Querying URL {url}")
                            acct_vending_resp = requests.get(url, headers=acct_vending_headers, timeout=60)
                            print("Response from assets vending endpoint: {}".format(str(acct_vending_resp)))
                            #print("Response data from assets vending endpoint: {}".format(json.dumps(acct_vending_resp.text)))
                            launchdarkly_credentials = json.loads(acct_vending_resp.text)
                            print(f"Parsed response data: {json.dumps(launchdarkly_credentials)} ")

                            # upload team's LD credentials to their team account's SSM Parameter Store
                            print(f"Loading Team Credentials onto team acct SSM params for  {team['team-id']}")
                            xa_ssm_client.put_parameter(Name='LD-ServerKey',
                                                        Description="LaunchDarkly Server key",
                                                        Value=launchdarkly_credentials['LAUNCHDARKLY_SERVER_KEY'],
                                                        Overwrite=True,
                                                        Tier="Standard",
                                                        Type="String",
                                                        DataType="text")
                            xa_ssm_client.put_parameter(Name='LD-ClientKey',
                                                        Description="LaunchDarkly Client key",
                                                        Value=launchdarkly_credentials['LAUNCHDARKLY_CLIENT_KEY'],
                                                        Overwrite=True,
                                                        Tier="Standard",
                                                        Type="String",
                                                        DataType="text")
                            xa_ssm_client.put_parameter(Name='LD-SignOnUrl',
                                                        Description="LaunchDarkly SignOn URL",
                                                        Value=launchdarkly_credentials['SSO_LINK'],
                                                        Overwrite=True,
                                                        Tier="Standard",
                                                        Type="String",
                                                        DataType="text")
                            xa_ssm_client.put_parameter(Name='TableNumber',
                                                        Description="Table Number of the Team",
                                                        Value=launchdarkly_credentials['TEAM_ID'],
                                                        Overwrite=True,
                                                        Tier="Standard",
                                                        Type="String",
                                                        DataType="text")
                            # xa_ssm_client.put_parameter(Name='LD-TeamEmail',
                            #                             Description="Table Number of the Team",
                            #                             Value=launchdarkly_credentials['TEAM_EMAIL'],
                            #                             Overwrite=True,
                            #                             Tier="Standard",
                            #                             Type="String",
                            #                             DataType="text")
                            # xa_ssm_client.put_parameter(Name='LD-TeamName',
                            #                             Description="Table Number of the Team",
                            #                             Value=launchdarkly_credentials['TEAM_NAME'],
                            #                             Overwrite=True,
                            #                             Tier="Standard",
                            #                             Type="String",
                            #                             DataType="text")
                            # xa_ssm_client.put_parameter(Name='LD-UserEmail',
                            #                             Description="Table Number of the Team",
                            #                             Value=launchdarkly_credentials['USER_EMAIL'],
                            #                             Overwrite=True,
                            #                             Tier="Standard",
                            #                             Type="String",
                            #                             DataType="text")

                print("Account Vending successful")

                send(event, context, SUCCESS, response_data)
                return
            except Exception as e:
                print(f"Lambda execution has failed! : {e}")
                traceback.print_exc()
                send(event, context, FAILED, response_data)
                return

    except Exception as e:
        print(f"Lambda execution has failed unexpectedly, unknown request type (probably a debugging code issue): {e}")
        traceback.print_exc()
        send(event, context, FAILED, {}, None)
        return

# check whether all team credentials are already loaded in SSM Parameter Store
def all_team_cred_params_exist(xa_ssm_client):
    try:
        for param in TEAM_SSM_PARAMS_NEEDED:
            xa_ssm_client.get_parameter(Name=param, WithDecryption=True)['Parameter']['Value']

        return True
    except Exception as e:
        print(e)
        return False

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

