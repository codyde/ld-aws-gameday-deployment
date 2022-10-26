# Copyright 2022 Amazon.com and its affiliates; all rights reserved. 
# This file is Amazon Web Services Content and may not be duplicated or distributed without permission.
import os
from datetime import datetime
import boto3
import json
import dynamodb_utils
import quest_const
import output_const
import input_const
import hint_const
import scoring_const
import http.client
import requests
import time
import ui_utils
from aws_gameday_quests.gdQuestsApi import GameDayQuestsApiClient

# Standard AWS GameDay Quests Environment Variables
QUEST_ID = os.environ['QUEST_ID']
QUEST_API_BASE = os.environ['QUEST_API_BASE']
QUEST_API_TOKEN = os.environ['QUEST_API_TOKEN']
GAMEDAY_REGION = os.environ['GAMEDAY_REGION']
ASSETS_BUCKET = os.environ['ASSETS_BUCKET']
ASSETS_BUCKET_PREFIX = os.environ['ASSETS_BUCKET_PREFIX']

# Quest Environment Variables
QUEST_TEAM_STATUS_TABLE = os.environ['QUEST_TEAM_STATUS_TABLE']
CHAOS_TIMER_MINUTES = os.environ['CHAOS_TIMER_MINUTES']

# Dynamo DB setup
dynamodb = boto3.resource('dynamodb')
quest_team_status_table = dynamodb.Table(QUEST_TEAM_STATUS_TABLE)

# This function is triggered by cron_lambda.py. It performs validation of team actions, such as assuming a role in their
# AWS account to check resources or trigger chaos events, as well as updating progress, or posting a message to the team’s event UI.
# Expected event payload is the QuestsAPI entry for this team
def lambda_handler(event, context):
    print(f"check_team_lambda invocation, event:{json.dumps(event, default=str)}, context: {str(context)}")

    # Instantiate the Quest API Client.
    quests_api_client = GameDayQuestsApiClient(QUEST_API_BASE, QUEST_API_TOKEN)

    # Check if event is running
    event_status = quests_api_client.get_event_status()
    if event_status['status'] != quest_const.EVENT_IN_PROGRESS:
        print(f"Event Status: {event_status}, aborting CHECK_TEAM_LAMBDA")
        return

    dynamodb_response = quest_team_status_table.get_item(Key={'team-id': event['team-id']})
    print(f"Retrieved quest team state for team {event['team-id']}: {json.dumps(dynamodb_response, default=str)}")

    # Make a copy of the original array to be able later on to do a comparison and validate whether a DynamoDB update is needed    
    team_data = dynamodb_response['Item'].copy() # Check init_lambda for the format

    # Task 1 evaluation
    team_data = evaluate_apprunner(quests_api_client, team_data)
    
    # Task 2 evaluation
    team_data = evaluate_release(quests_api_client, team_data)

    # Task 3 evaluation
    team_data = evaluate_debug_mode(quests_api_client, team_data)

    # Task 4 evaluation
    team_data = evaluate_db_migration(quests_api_client, team_data)

    # Complete quest if everything is done
    check_and_complete_quest(quests_api_client, QUEST_ID, team_data)

    # Compare initial DynamoDB item with its copy to check whether changes were made. 
    if dynamodb_response['Item']==team_data:
        print("No changes throughout this run - no need to update the DynamoDB item")
    else:
        dynamodb_utils.save_team_data(team_data, quest_team_status_table)


# Task 1 evaluation - Monitoring
def evaluate_apprunner(quests_api_client, team_data):
    print(f"Evaluating app runn deployment task for team {team_data['team-id']}")

    # Check whether task was completed already
    if not team_data['is-webapp-up']:

        if team_data['task1-attempted'] == False:
            if team_data['app-runner-url'] == 'unknown':
                print("No app url - doing nothing")
                quests_api_client.post_input(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=input_const.TASK1_ENDPOINT_KEY,
                    label=input_const.TASK1_ENDPOINT_LABEL,
                    description=input_const.TASK1_ENDPOINT_DESCRIPTION,
                    dashboard_index=input_const.TASK1_ENDPOINT_INDEX
                )
            else:
                ready_check_webapp = check_webapp(team_data['app-runner-url'])
                # If the app is up and returns 200 ok 
                if ready_check_webapp == True:
                    print(f"The web application for team {team_data['team-id']} is UP")
                # If its any other code it = down 
                else:
                    print(f"The web application is DOWN")     
        else:
            ready_check_webapp = check_webapp(team_data['app-runner-url'])
            if not ready_check_webapp:
                print("Resetting app-runner-url to unknown")
                team_data['app-runner-url'] = 'unknown'
                dynamodb_utils.save_team_data(team_data, quest_team_status_table)
            else: 
                print(f"The web application for team {team_data['team-id']} is UP")
                
            # Award points if web app is up else detract points if down
            # Complete task if chaos event had started and web app is up
                if team_data['is-webapp-up'] and not team_data['start-task-2'] and not team_data['is-apprunner-done']:
                    print("Setting is-apprunner-done to True")
                    team_data['is-apprunner-done'] = True
                    print("Setting start-task-2 to True")
                    team_data['start-task-2'] = True
                    dynamodb_utils.save_team_data(team_data, quest_team_status_table)

                    response = quests_api_client.delete_hint(
                        team_id=team_data['team-id'],
                        quest_id=QUEST_ID,
                        hint_key=hint_const.TASK1_HINT1_KEY,
                        detail=True
                    )   
                    
                    # Handling a response status code other than 200. In this case, we are just logging
                    if response['statusCode'] != 200:
                        print(response)

                    # Prepare for Task 2 Post task 2 instructions
                    print("Starting Task 2")
    else: 
        if not team_data['start-task-2'] and not team_data['is-apprunner-done']:
            print("Setting is-apprunner-done to True")
            team_data['is-apprunner-done'] = True
            print("Setting start-task-2 to True")
            team_data['start-task-2'] = True
            dynamodb_utils.save_team_data(team_data, quest_team_status_table)

            quests_api_client.delete_output(
                    team_id=team_data["team-id"],
                    quest_id=QUEST_ID, 
                    key=output_const.TASK1_APPRUNNER_DOWN_KEY
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
                markdown=True
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

            response = quests_api_client.delete_hint(
                team_id=team_data['team-id'],
                quest_id=QUEST_ID,
                hint_key=hint_const.TASK1_HINT1_KEY,
                detail=True
            )   
            
            # Handling a response status code other than 200. In this case, we are just logging
            if response['statusCode'] != 200:
                print(response)

            print(team_data)

            # Post task final message
            print("posting final message")

    return team_data


# Checks whether the monitoring web app is up or done and returns True or False respectively
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


# Task 2 evaluation - website release
def evaluate_release(quests_api_client, team_data):
    print(f"Evaluating released features with LaunchDarkly task for team {team_data['team-id']}")

    image_url = ui_utils.generate_signed_or_open_url(ASSETS_BUCKET, f"{ASSETS_BUCKET_PREFIX}curl.jpeg",signed_duration=86400)

    if not team_data['is-website-released']:
        print("is-website-released is False")

        if team_data['start-task-2'] == True:
            print("start-task-2 is True")

            if team_data['app-version'] == 'unknown': # True
                release_version = getAppRelease(team_data)

                if release_version: # False
                    print(f"The web application for team {team_data['team-id']} is UP")

                    team_data['is-website-released'] = True
                    dynamodb_utils.save_team_data(team_data, quest_team_status_table)

                    # TODO BUILD A HINT HERE FOR THE DEBUG CODE SECTION - SOLVE THE
                    
                else:
                    print(f"The preview site is still displaying")

        else:
            print("Task not started yet - doing nothing")
    else:

        print("Website is released")


    return team_data

def getAppRelease(team_data):
    try:
        print(f"Getting current version via API")
        conn = http.client.HTTPSConnection(team_data['app-runner-url'].strip('https://'), timeout=5)
        conn.request("GET", "/status")
        res = conn.getresponse()
        dataResp = json.loads(res)
        if dataResp['app-version'] == team_data['app-version']:
            return True
        else:
            raise Exception(f"The version does not match")
    except Exception as e:
        print(f"The version does not match")
        return False


# Task 3 - Debug 
def evaluate_debug_mode(quests_api_client, team_data):
    if team_data['start-task-3'] == True and not team_data['is-debug-mode'] and not team_data['task3-score-locked']:
        print("Task 3 - Executing the start of debug mode module")

        if team_data['debugcode'] == 'unknown':

            quests_api_client.post_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=output_const.TASK3_KEY,
                    label=output_const.TASK3_LABEL,
                    value=output_const.TASK3_VALUE,
                    dashboard_index=output_const.TASK3_INDEX,
                    markdown=output_const.TASK3_MARKDOWN,
                )

            quests_api_client.post_input(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=input_const.TASK3_DEBUG_KEY,
                    label=input_const.TASK3_DEBUG_LABEL,
                    description=input_const.TASK3_DEBUG_DESCRIPTION,
                    dashboard_index=input_const.TASK3_DEBUG_INDEX
                )
        else:
            print("Task 3 - Conditions for execution not met")

    else:
        print("Task 3 not ready to be evaluated yet")

    return team_data


# Task 4 - The ultimate answer
# The actual evaluation happens in Update Lambda. Here is the logic to enable the task
def evaluate_db_migration(quests_api_client, team_data):
    print(f"Evaluating Task 4 for {team_data['team-id']}")

    if team_data['start-task-4'] == True and not team_data['is-db-migrated'] and not team_data['task4-score-locked']:
        print(f"Task 4 logic starts for {team_data['team-id']}")

        if team_data['migration-location'] == 'unknown':

    # Enable this task as soon as the team completed all the other tasks
            if (team_data['is-apprunner-done']           # Task 1
                and team_data['is-website-released']         # Task 2
                and team_data['is-debug-mode']           # Task 3
                and not team_data['is-db-migrated']):    # Task 4 (this task not yet enabled)

                # Switch flag
                team_data['start-task-4'] = True

                # Post Task 4 instructions
                quests_api_client.post_output(
                    team_id=team_data['team-id'],
                    quest_id=QUEST_ID,
                    key=output_const.TASK4_KEY,
                    label=output_const.TASK4_LABEL,
                    value=output_const.TASK4_VALUE,
                    dashboard_index=output_const.TASK4_INDEX,
                    markdown=output_const.TASK4_MARKDOWN,
                )
        else:
            print("Task 4 - Conditions for execution not met")

    else:
        print("Task 3 not ready to be evaluated yet")

    return team_data


# Verify that all tasks have been successfully done and complete the quest if so
def check_and_complete_quest(quests_api_client, quest_id, team_data):

    # Check if everything is done
    if (team_data['is-webapp-up']           # Task 1
        and team_data['is-website-released']         # Task 2
        and team_data['is-debug-mode']           # Task 3
        and team_data['is-db-migrated']):    # Task 4

        # Award quest complete points
        print(f"Team {team_data['team-id']} has completed this quest, posting output and awarding points")
        # quests_api_client.post_score_event(
        #     team_id=team_data["team-id"],
        #     quest_id=quest_id,
        #     description=scoring_const.QUEST_COMPLETE_DESC,
        #     points=scoring_const.QUEST_COMPLETE_POINTS
        # )

        # # Award quest complete bonus points
        # bonus_points = calculate_bonus_points(quests_api_client, quest_id, team_data)
        # quests_api_client.post_score_event(
        #     team_id=team_data["team-id"],
        #     quest_id=quest_id,
        #     description=scoring_const.QUEST_COMPLETE_BONUS_DESC,
        #     points=bonus_points
        # )

        # # Post quest complete message
        # quests_api_client.post_output(
        #     team_id=team_data['team-id'],
        #     quest_id=quest_id,
        #     key=output_const.QUEST_COMPLETE_KEY,
        #     label=output_const.QUEST_COMPLETE_LABEL,
        #     value=output_const.QUEST_COMPLETE_VALUE,
        #     dashboard_index=output_const.QUEST_COMPLETE_INDEX,
        #     markdown=output_const.QUEST_COMPLETE_MARKDOWN,
        # )

        # # Complete quest
        # quests_api_client.post_quest_complete(team_id=team_data['team-id'], quest_id=quest_id)

        return True

    return False


# Checks whether the chaos event timer is up by calculating the difference between the current time and 
# the timer's start time plus the minutes to trigger the chaos event
def is_chaos_timer_up(timer_start_time, timer_minutes):

    # Timer start time
    start_time = datetime.fromtimestamp(timer_start_time)

    # Current time
    current_time = datetime.now()

    # Time difference
    time_diff = current_time - start_time
    
    # Time difference in minutes
    minutes = int(time_diff.total_seconds() / 60)

    if minutes >= timer_minutes:
        print(f"Chaos event timer is up: {minutes} minutes have elapsed")
        return True
    else:
        print(f"No time for chaos event yet: {timer_minutes - minutes} minutes left")

    return False


# Calculate quest completion bonus points
# This is to reward teams that complete the quest faster
def calculate_bonus_points(quests_api_client, quest_id, team_data):
    quest = quests_api_client.get_quest_for_team(team_data['team-id'], quest_id)

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