# Copyright 2022 Amazon.com and its affiliates; all rights reserved. 
# This file is Amazon Web Services Content and may not be duplicated or distributed without permission.
import json
import os
from platform import release
from tabnanny import check
import boto3
from datetime import datetime
import dynamodb_utils
import quest_const
import input_const
import output_const
import scoring_const
import hint_const
import http.client
import requests
import ui_utils
from aws_gameday_quests.gdQuestsApi import GameDayQuestsApiClient

# Standard AWS GameDay Quests Environment Variables
QUEST_ID = os.environ['QUEST_ID']
QUEST_API_BASE = os.environ['QUEST_API_BASE']
QUEST_API_TOKEN = os.environ['QUEST_API_TOKEN']
GAMEDAY_REGION = os.environ['GAMEDAY_REGION']
# ASSETS_BUCKET = os.environ['ASSETS_BUCKET']
# ASSETS_BUCKET_PREFIX = os.environ['ASSETS_BUCKET_PREFIX']

# Quest Environment Variables
QUEST_TEAM_STATUS_TABLE = os.environ['QUEST_TEAM_STATUS_TABLE']

# Dynamo DB resource
dynamodb = boto3.resource('dynamodb')
quest_team_status_table = dynamodb.Table(QUEST_TEAM_STATUS_TABLE)

def check_webapp(apprunnerurl):
    try:
        print(f"Testing web app status using URL {apprunnerurl}")
        conn = http.client.HTTPSConnection(apprunnerurl.strip('https://'), timeout=5)
        conn.request("GET", "/")
        res = conn.getresponse()
        status = res.status
        print(f"The status code returned it {status}")
        if status != 200:
            raise Exception(f"Web app down: {status}")
        return True
    except Exception as e:
        print(f"Web app not available: {e}")
        return False

def check_apprunner(apprunnername):
    try:
        client = boto3.client('apprunner')
        arsvc=client.list_services()
        print(arsvc)
        for i in arsvc['ServiceSummaryList']:
            if i['ServiceName'] == apprunnername:
                return True
    except Exception as e:
        print(f"Unable to connect: {e}")
        return False
        
def get_apprunner_url(apprunnername):
    try:
        client = boto3.client('apprunner')
        arsvc=client.list_services()
        print(arsvc)
        for i in arsvc['ServiceSummaryList']:
            if i['ServiceName'] == apprunnername:
                svcarn = i['ServiceArn']
        svcurl = 'https://' + client.describe_service(ServiceArn=svcarn)['Service']['ServiceUrl']
        return svcurl 
    except Exception as e:
        print(f"Unable to connect: {e}")

def check_apikey(apikey):
    try:
        url = "https://app.launchdarkly.com/api/v2/projects"
        headers = {"Authorization": apikey}
        r = requests.get(url, headers=headers)
        print(r.json())
        return True
    except Exception as e:
        print(f"Unable to connect: {e}")
        return False

def get_ld_project(apikey):
    try:
        url = "https://app.launchdarkly.com/api/v2/projects"
        headers = {"Authorization": apikey}
        r = requests.get(url, headers=headers)
        projkey = r.json()['items'][0]['key']
        print("The LaunchDarkly project is "+projkey)
        return projkey
    except Exception as e:
        print(f"Unable to connect: {e}")
        return e

def getlogModeTargeting(team_data):
    try:
        url = f"https://app.launchdarkly.com/api/v2/flags/{team_data['ld-project-key']}/logMode"
        headers = {"Authorization": team_data['ld-api-key']}
        response = requests.get(url, headers=headers)
        data = response.json()
        targetedUser = data['environments']['test']['targets'][0]['values'][0]
        if targetedUser == 'debuguser':
            return True
        else:
            raise Exception(f"The debuguser is not targeted")
    except Exception as e:
        print(f"There was an error on executing this api call: {e}")
        return False

def getAppRelease(team_data):
    try:
        print(f"Getting current version via API")
        conn = http.client.HTTPSConnection(team_data['app-runner-url'].strip('https://'), timeout=5)
        conn.request("GET", "/status")
        res = conn.getresponse()
        string = res.read().decode('utf-8')
        dataResp = json.loads(string)
        print(dataResp['app-version'])
        if dataResp['app-version'] == team_data['app-version']:
            return True
        else:
            raise Exception(f"The version does not match")
    except Exception as e:
        print(f"The version does not match")
        return False

def getDebugValue(team_data):
    try:
        print(f"Getting debug value via the /teamdebug API")
        conn = http.client.HTTPSConnection(team_data['app-runner-url'].strip('https://'), timeout=5)
        conn.request("GET", "/teamdebug")
        res = conn.getresponse()
        string = res.read().decode('utf-8')
        dataResp = json.loads(string)
        print(dataResp['debugcode'])
        if dataResp['debugcode'] == team_data['debugcode']:
            return True
        else:
            raise Exception(f"The debug code is invalid")
    except Exception as e:
        print(f"The version does not match")
        return False

def getMigrationValue(team_data):
    try:
        print(f"Getting debug value via the /teamdebug API")
        conn = http.client.HTTPSConnection(team_data['app-runner-url'].strip('https://'), timeout=5)
        conn.request("GET", "/health")
        res = conn.getresponse()
        string = res.read().decode('utf-8')
        dataResp = json.loads(string)
        print(dataResp['location'])
        if dataResp['location'] == team_data['migration-location']:
            return True
        else:
            raise Exception(f"The migration location is invalid")
    except Exception as e:
        print(f"You haven't migrated")
        return False

def calculate_bonus_points(quests_api_client, quest_id, team_data):
    quest = quests_api_client.get_quest_for_team(team_data['team-id'], QUEST_ID)

    # Get quest start time
    start_time = datetime.fromtimestamp(quest['quest-start-time'])

    # Get quest end time, that is, current time
    end_time = datetime.now()

    # Calculate elapsed time
    time_diff = end_time - start_time
    minutes = int(time_diff.total_seconds() / 60)

    # Calculate bonus points based on elapsed time
    bonus_points = int(scoring_const.QUEST_COMPLETE_POINTS / minutes * scoring_const.QUEST_COMPLETE_MULTIPLIER)
    print(f"Bonus points on {scoring_const.QUEST_COMPLETE_POINTS} done in {minutes} minutes: {bonus_points}")

    return bonus_points

# This function is triggered by sns_lambda.py whenever the team has provided input via the event UI. It validates
# the input and performs related operations, such as updating the team's DynamoDB table record or posting a feedback message.
# Expected event parameters: {'team_id': team_id,'key': key, 'value': value}
def lambda_handler(event, context):
    print(f"update_lambda invocation, event:{json.dumps(event, default=str)}, context: {str(context)}")

    # Instantiate the Quest API Client.
    quests_api_client = GameDayQuestsApiClient(QUEST_API_BASE, QUEST_API_TOKEN)

    # Check if event is running
    event_status = quests_api_client.get_event_status()
    if event_status['status'] != quest_const.EVENT_IN_PROGRESS:
        print(f"Event Status: {event_status['status']}, aborting UPDATE_LAMBDA")
        return

    # Check if quest is active for the team
    quest_status = quests_api_client.get_quest_for_team(team_id=event['team_id'], quest_id=QUEST_ID)
    if quest_status['quest-state'] != quest_const.TEAM_QUEST_IN_PROGRESS:
        print(f"Quest Status: {quest_status['quest-state']}, aborting UPDATE_LAMBDA")

    dynamodb_response = quest_team_status_table.get_item(Key={'team-id': event['team_id']})
    print(f"Retrieved team state for team {event['team_id']}: {json.dumps(dynamodb_response, default=str)}")
    team_data = dynamodb_response['Item']

    # Task 1 evaluation
    if (event['key'] == input_const.TASK1_ENDPOINT_KEY
        and not team_data['is-webapp-up'] and not team_data['ld-api-key-completed']): # This second check is needed to avoid multiple submissions since points are being given here
        try:
            print("prior apprunner url value is "+team_data['app-runner-url'])
            input_value = event['value'] 
            print("event value is "+event['value'])
            team_data['monitoring-chaos-timer'] = int(datetime.now().timestamp())
            print("setting task1-attempted to True")
            team_data['task1-attempted'] = True
            # print("Setting App Runner URL value")
            # team_data['app-runner-url'] = str(event['value'])

            # Update DynamoDB to avoid race conditions, then do the rest on success

            # Delete input since cannot be updated as task can be started only once
            # quests_api_client.delete_input(
            #     team_id=team_data["team-id"],
            #     quest_id=QUEST_ID, 
            #     key=input_const.TASK1_ENDPOINT_KEY
            # )

            apphealth = check_apprunner(input_value)

            if apphealth == True:
                print(f"Setting team_data is-webapp-up True, url, and updating Dynamo")
                team_data['is-webapp-up'] = True
                team_data['app-runner-url'] = get_apprunner_url(input_value)
                dynamodb_utils.save_team_data(team_data, quest_team_status_table)

                quests_api_client.delete_input(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID, 
                    key=input_const.TASK1_ENDPOINT_KEY
                )
                              
                # Delete app down message if present
                quests_api_client.delete_output(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID, 
                    key=output_const.TASK1_APPRUNNER_WRONG_KEY
                )

                quests_api_client.delete_hint(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID, 
                    hint_key=hint_const.TASK1_HINT1_KEY,
                    detail=True
                )

                quests_api_client.post_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=output_const.TASK1_APPRUNNER_COMPLETE_KEY,
                    label=output_const.TASK1_APPRUNNER_COMPLETE_LABEL,
                    value=output_const.TASK1_APPRUNNER_COMPLETE_VALUE,
                    dashboard_index=output_const.TASK1_APPRUNNER_COMPLETE_INDEX,
                    markdown=output_const.TASK1_APPRUNNER_COMPLETE_MARKDOWN,
                )

                quests_api_client.post_input(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=input_const.TASK1_API_KEY,
                    label=input_const.TASK1_API_LABEL,
                    description=input_const.TASK1_API_DESCRIPTION,
                )

                quests_api_client.post_score_event(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID,
                    description=scoring_const.CORRECT_APPRUNNER_DESC,
                    points=scoring_const.CORRECT_APPRUNNER_POINTS
                )

            else: 
                if team_data['task1-attempted']:
                    print(f"The web application for team {team_data['team-id']} is DOWN")
                    print(f"Resetting app-runner-url to try again and updating Dynamo")
                    team_data['app-runner-url'] = 'unknown'
                    # team_data['is-apprunner-done']: False
                    print(f"Setting app-runner-url to unknown Dynamo")
                    dynamodb_utils.save_team_data(team_data, quest_team_status_table)

                    quests_api_client.post_input(
                        team_id=team_data['team-id'],
                        quest_id=QUEST_ID,
                        key=input_const.TASK1_ENDPOINT_KEY,
                        label=input_const.TASK1_ENDPOINT_LABEL,
                        description=input_const.TASK1_ENDPOINT_DESCRIPTION,
                        dashboard_index=input_const.TASK1_ENDPOINT_INDEX
                    )
                
                    quests_api_client.post_output(
                        team_id=team_data['team-id'],
                        quest_id=QUEST_ID,
                        key=output_const.TASK1_APPRUNNER_WRONG_KEY,
                        label=output_const.TASK1_APPRUNNER_WRONG_LABEL,
                        value=output_const.TASK1_APPRUNNER_WRONG_VALUE,
                        dashboard_index=output_const.TASK1_APPRUNNER_WRONG_INDEX,
                        markdown=output_const.TASK1_APPRUNNER_WRONG_MARKDOWN,
                    )

                    # Post task 1 hint
                    quests_api_client.post_hint(
                        team_id=team_data['team-id'],
                        quest_id=QUEST_ID,
                        hint_key=hint_const.TASK1_HINT1_KEY,
                        label=hint_const.TASK1_HINT1_LABEL,
                        description=hint_const.TASK1_HINT1_DESCRIPTION,
                        value=hint_const.TASK1_HINT1_VALUE,
                        dashboard_index=hint_const.TASK1_HINT1_INDEX,
                        cost=hint_const.TASK1_HINT1_COST,
                        status=hint_const.STATUS_OFFERED
                    )

                    quests_api_client.delete_output(
                        team_id=team_data["team-id"],
                        quest_id=QUEST_ID,
                        key="TASK1_APPRUNNER_DOWN_KEY"
                    )

                    quests_api_client.post_score_event(
                        team_id=team_data["team-id"],
                        quest_id=QUEST_ID,
                        description=scoring_const.WRONG_APPRUNNER_DESC,
                        points=scoring_const.WRONG_APPRUNNER_POINTS
                    )

                # Assuming they havent yet 
                else: 
                    print("Not attempted yet; doing nothing")

        except Exception as err:
            print(f"Error while handling team update request: {err}")

    if (event['key'] == input_const.TASK1_API_KEY and not team_data['ld-api-key-completed']):
        try:
            print("Adding api key "+event['value']+" to quest")
            team_data['ld-api-key'] = event['value']

            if check_apikey(team_data['ld-api-key']) == True:
                team_data['ld-api-key-completed'] = True

                team_data['ld-project-key'] = get_ld_project(team_data['ld-api-key'])
                dynamodb_utils.save_team_data(team_data, quest_team_status_table)

                quests_api_client.delete_input(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID, 
                    key=input_const.TASK1_API_KEY
                )

                quests_api_client.post_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=output_const.TASK1_COMPLETE_KEY,
                    label=output_const.TASK1_COMPLETE_LABEL,
                    value=output_const.TASK1_COMPLETE_VALUE,
                    dashboard_index=output_const.TASK1_COMPLETE_INDEX,
                    markdown=output_const.TASK1_COMPLETE_MARKDOWN,
                )

                # Stage Task 2 Things

                quests_api_client.post_input(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=input_const.TASK2_LAUNCH_KEY,
                    label=input_const.TASK2_LAUNCH_LABEL,
                    description=input_const.TASK2_LAUNCH_DESCRIPTION,
                    dashboard_index=input_const.TASK2_LAUNCH_INDEX,
                )

                # image_url = ui_utils.generate_signed_or_open_url(ASSETS_BUCKET, f"{ASSETS_BUCKET_PREFIX}curl.jpeg",signed_duration=86400)

                quests_api_client.post_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=output_const.TASK2_KEY,
                    label=output_const.TASK2_LABEL,
                    value=output_const.TASK2_VALUE,
                    dashboard_index=output_const.TASK2_INDEX,
                    markdown=output_const.TASK2_MARKDOWN,
                )

                quests_api_client.post_input(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=input_const.TASK2_LAUNCH_KEY,
                    label=input_const.TASK2_LAUNCH_LABEL,
                    description=input_const.TASK2_LAUNCH_DESCRIPTION,
                    dashboard_index=input_const.TASK2_LAUNCH_INDEX
                )

                quests_api_client.post_hint(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    hint_key=hint_const.TASK2_HINT1_KEY,
                    label=hint_const.TASK2_HINT1_LABEL,
                    description=hint_const.TASK2_HINT1_DESCRIPTION,
                    value=hint_const.TASK1_HINT2_VALUE,
                    dashboard_index=hint_const.TASK2_HINT1_INDEX,
                    cost=hint_const.TASK1_HINT2_COST,
                    status=hint_const.STATUS_OFFERED
                )

                quests_api_client.post_score_event(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID,
                    description=scoring_const.CORRECT_API_DESC,
                    points=scoring_const.CORRECT_API_POINTS
                )

                dynamodb_utils.save_team_data(team_data, quest_team_status_table)

            else:

                quests_api_client.post_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=output_const.TASK1_API_WRONG_KEY,
                    label=output_const.TASK1_API_WRONG_LABEL,
                    value=output_const.TASK1_API_WRONG_VALUE,
                    dashboard_index=output_const.TASK1_API_WRONG_INDEX,
                    markdown=output_const.TASK1_API_WRONG_INDEX,
                )

                quests_api_client.post_score_event(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID,
                    description=scoring_const.WRONG_API_DESC,
                    points=scoring_const.WRONG_API_POINTS
                )

        except Exception as err:
            print(f"Error while handling team update request: {err}")

    # Task 2 Website Release 
    if (event['key'] == input_const.TASK2_LAUNCH_KEY and not team_data['is-website-released'] and team_data['is-api-key-completed'] == True):
        print("Evaluating Task 2")

        task2_Score_Lock = team_data['task2-score-locked']
        if not task2_Score_Lock:
            team_data['task2-score-locked'] = True
            input_value = event['value']
            print("The input value is "+input_value)
            team_data['task2-attempted'] = True
            team_data['app-version'] = input_value
            released_version = getAppRelease(team_data)
            print("The value is the app status is "+str(released_version))
            dynamodb_utils.save_team_data(team_data, quest_team_status_table)
            if released_version:
                team_data['is-website-released'] = True
                team_data['start-task-3'] = True
                print("writing updated task2 value")
                dynamodb_utils.save_team_data(team_data, quest_team_status_table)
                
                print("Task 2 - Checking for errors and deleting if there is")
                
                print("unlocking task2 score lock")
                team_data['task2-score-locked'] = False

                print("Removing input and locking the scoring")
                quests_api_client.delete_input(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID, 
                    key=input_const.TASK2_LAUNCH_KEY
                )
                
                print("Trying to delete unlreased error")
                quests_api_client.delete_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=output_const.TASK2_UNRELEASED_KEY,
                )
                
                print("Deleting hint")
                quests_api_client.delete_hint(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID, 
                    hint_key=hint_const.TASK2_HINT1_KEY,
                    detail=True
                )

                print("Posting complete output")
                quests_api_client.post_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=output_const.TASK2_COMPLETE_KEY,
                    label=output_const.TASK2_COMPLETE_LABEL,
                    value=output_const.TASK2_COMPLETE_VALUE,
                    dashboard_index=output_const.TASK2_COMPLETE_INDEX,
                    markdown=output_const.TASK2_COMPLETE_MARKDOWN,
                )


                print("Scoring task 2")

                quests_api_client.post_input(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=input_const.TASK3_DEBUG_KEY,
                    label=input_const.TASK3_DEBUG_LABEL,
                    description=input_const.TASK3_DEBUG_DESCRIPTION,
                    dashboard_index=input_const.TASK3_DEBUG_INDEX
                )

                quests_api_client.post_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=output_const.TASK3_KEY,
                    label=output_const.TASK3_LABEL,
                    value=output_const.TASK3_VALUE,
                    dashboard_index=output_const.TASK3_INDEX,
                    markdown=output_const.TASK3_COMPLETE_MARKDOWN,
                )

                quests_api_client.delete_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key="task2_score_lock",
                )

                quests_api_client.post_score_event(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID,
                    description=scoring_const.COMPLETE_DESC,
                    points=scoring_const.COMPLETE_POINTS
                )

            else: 
                print("resetting app-version")
                team_data['app-version'] = 'unknown'
                print("writing values to Dynamo")
                dynamodb_utils.save_team_data(team_data, quest_team_status_table)
                
                quests_api_client.post_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key="task2_app_unreleased",
                    label="Still unreleased!",
                    value="The preview version of the page is still running",
                    dashboard_index=21,
                    markdown=True,
                )

                team_data['task2-score-locked'] = False
                
                print("Deleting task lock message")
                quests_api_client.delete_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key="task2_score_lock",
                )

                quests_api_client.post_input(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=input_const.TASK2_LAUNCH_KEY,
                    label=input_const.TASK2_LAUNCH_LABEL,
                    description=input_const.TASK2_LAUNCH_DESCRIPTION,
                    dashboard_index=input_const.TASK2_LAUNCH_INDEX
                )

                quests_api_client.post_score_event(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID,
                    description=scoring_const.UNRELEASED_DESC,
                    points=scoring_const.UNRELEASED_POINTS
                )

                dynamodb_utils.save_team_data(team_data, quest_team_status_table)
        else:
            quests_api_client.post_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key="task2_score_lock",
                    label="Input Locked",
                    value="It looks like a value has already been submitted - scoring is locked. Patience is a virtue",
                    dashboard_index=14,
                    markdown=True,
                )

    # Task 3 Debug Mode Enablement
    elif event['key'] == input_const.TASK3_DEBUG_KEY and not team_data['is-debug-mode'] and not team_data['task3-score-locked']: # run if debug mode is false and task lock is off
        try:
            print("Evaluating task 3")
            team_data['task3-score-locked'] = True
            dynamodb_utils.save_team_data(team_data, quest_team_status_table)
            team_data['task3-attempted'] = True
            input_value = event['value']
            team_data['debugcode'] = input_value
            debugstatus = getDebugValue(team_data)
            targetingOn = getlogModeTargeting(team_data)
            if debugstatus == True and targetingOn == True:

                quests_api_client.delete_input(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID, 
                    key=input_const.TASK3_DEBUG_KEY
                )

                quests_api_client.delete_output(
                        team_id=team_data['team-id'],
                        quest_id=QUEST_ID,
                        key=output_const.TASK3_INCORRECT_KEY,
                    )

                quests_api_client.post_output(
                        team_id=team_data['team-id'],
                        quest_id=QUEST_ID,
                        key=output_const.TASK3_COMPLETE_KEY,
                        label=output_const.TASK3_COMPLETE_LABEL,
                        value=output_const.TASK3_COMPLETE_VALUE,
                        dashboard_index=output_const.TASK3_COMPLETE_INDEX,
                        markdown=output_const.TASK3_COMPLETE_MARKDOWN,
                    )

                
                team_data['is-debug-mode'] = True

                # Post Task 4 info

                quests_api_client.post_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=output_const.TASK4_KEY,
                    label=output_const.TASK4_LABEL,
                    value=output_const.TASK4_VALUE,
                    dashboard_index=output_const.TASK4_INDEX,
                    markdown=output_const.TASK4_MARKDOWN,
                )

                quests_api_client.post_input(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=input_const.TASK4_MIGRATION_KEY,
                    label=input_const.TASK4_MIGRATION_LABEL,
                    description=input_const.TASK4_MIGRATION_DESCRIPTION,
                    dashboard_index=input_const.TASK4_MIGRATION_INDEX
                )

                quests_api_client.post_score_event(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID,
                    description=scoring_const.DEBUG_RIGHT_DESC,
                    points=scoring_const.DEBUG_RIGHT_POINTS
                )


                dynamodb_utils.save_team_data(team_data, quest_team_status_table)
            else:
                print("Value was wrong - setting reset sequence") 
                print("Removing score lock for Task 3")
                team_data['task3-score-locked'] = False
                team_data['debugCode'] = 'unknown'
                
                quests_api_client.post_output(
                        team_id=team_data['team-id'],
                        quest_id=QUEST_ID,
                        key=output_const.TASK3_INCORRECT_KEY,
                        label=output_const.TASK3_INCORRECT_LABEL,
                        value=output_const.TASK3_INCORRECT_VALUE,
                        dashboard_index=output_const.TASK3_INCORRECT_INDEX,
                        markdown=output_const.TASK3_INCORRECT_MARKDOWN,
                    )

                quests_api_client.post_input(
                        team_id=team_data['team-id'],
                        quest_id=QUEST_ID,
                        key=input_const.TASK3_DEBUG_KEY,
                        label=input_const.TASK3_DEBUG_LABEL,
                        description=input_const.TASK3_DEBUG_DESCRIPTION,
                        dashboard_index=input_const.TASK3_DEBUG_INDEX
                    )  

                quests_api_client.post_score_event(
                        team_id=team_data["team-id"],
                        quest_id=QUEST_ID,
                        description=scoring_const.DEBUG_WRONG_DESC,
                        points=scoring_const.DEBUG_WRONG_POINTS
                    )

                dynamodb_utils.save_team_data(team_data, quest_team_status_table)

        except Exception as err:
            print(f"Error while handling team update request: {err}")


    # Task 4 - DB Migration
    elif event['key'] == input_const.TASK4_MIGRATION_KEY and not team_data['is-db-migrated'] and not team_data['task4-score-locked']:
        try:
            print("Evaluating task 4")
            # Check team's input value
            team_data['task4-score-locked'] = True
            quests_api_client.delete_input(
                team_id=team_data["team-id"],
                quest_id=QUEST_ID, 
                key=input_const.TASK4_MIGRATION_KEY
            )
            value = event['value']
            team_data['migration-location'] = value
            migrated = getMigrationValue(team_data)
            if migrated == True:

                quests_api_client.delete_input(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID, 
                    key=input_const.TASK4_MIGRATION_KEY
                )

                # Delete error if it exists 
                team_data['is-db-migrated'] = True

                quests_api_client.delete_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=output_const.TASK4_WRONG_KEY,
                )

                quests_api_client.post_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=output_const.TASK4_CORRECT_KEY,
                    label=output_const.TASK4_CORRECT_LABEL,
                    value=output_const.TASK4_CORRECT_VALUE,
                    dashboard_index=output_const.TASK4_CORRECT_INDEX,
                    markdown=output_const.TASK4_CORRECT_MARKDOWN,
                )

                team_data['task4-score-locked'] = False
                dynamodb_utils.save_team_data(team_data, quest_team_status_table)

                quests_api_client.post_score_event(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID,
                    description=scoring_const.QUEST_COMPLETE_DESC,
                    points=scoring_const.QUEST_COMPLETE_POINTS
                )

                # Award quest complete bonus points
                bonus_points = calculate_bonus_points(quests_api_client, QUEST_ID, team_data)

                # Post quest complete message
                quests_api_client.post_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=output_const.QUEST_COMPLETE_KEY,
                    label=output_const.QUEST_COMPLETE_LABEL,
                    value=output_const.QUEST_COMPLETE_VALUE,
                    dashboard_index=output_const.QUEST_COMPLETE_INDEX,
                    markdown=output_const.QUEST_COMPLETE_MARKDOWN,
                )

                quests_api_client.post_score_event(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID,
                    description=scoring_const.MIGRATION_SUCCESS_DESC,
                    points=scoring_const.MIGRATION_SUCCESS_POINTS
                )

                quests_api_client.post_score_event(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID,
                    description=scoring_const.QUEST_COMPLETE_BONUS_DESC,
                    points=bonus_points
                )

                # Complete quest
                quests_api_client.post_quest_complete(team_id=team_data['team-id'], quest_id=QUEST_ID)

            else:

                quests_api_client.post_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=output_const.TASK4_WRONG_KEY,
                    label=output_const.TASK4_WRONG_LABEL,
                    value=output_const.TASK4_WRONG_VALUE,
                    dashboard_index=output_const.TASK4_WRONG_INDEX,
                    markdown=output_const.TASK4_WRONG_MARKDOWN,
                )
                
                team_data['migration-location'] = 'unknown'
                team_data['task4-score-locked'] = False

                quests_api_client.post_input(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=input_const.TASK4_MIGRATION_KEY,
                    label=input_const.TASK4_MIGRATION_LABEL,
                    description=input_const.TASK4_MIGRATION_DESCRIPTION,
                    dashboard_index=input_const.TASK4_MIGRATION_INDEX
                )

                quests_api_client.post_score_event(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID,
                    description=scoring_const.MIGRATION_FAILED_DESC,
                    points=scoring_const.MIGRATION_FAILED_POINTS
                )
                    
                dynamodb_utils.save_team_data(team_data, quest_team_status_table)

        except Exception as err:
            print(f"Error while handling team update request: {err}")

    else:
        print(f"Unknown input key {event['key']} encountered, ignoring.")
