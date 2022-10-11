# Copyright 2022 Amazon.com and its affiliates; all rights reserved. 
# This file is Amazon Web Services Content and may not be duplicated or distributed without permission.
import json
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError


def save_team_data(team_data, quest_status_table):

    # Get the item's current version
    current_version = team_data["version"]

    # Increase the version number
    team_data["version"] += 1

    # Try updating the item, but only if it hasn't been updated by another function. Some possible scenarios:
    # 1. Race condition between CHECK_TEAM_LAMBDA and UPDATE_LAMBDA with the former going first
    # 2. Race condition between CHECK_TEAM_LAMBDA and UPDATE_LAMBDA with the latter going first
    # 3. Race condition between two executions of UPDATE_LAMBDA due to rapid button clicks
    try:
        print(f"Storing team data back to DynamoDb: {json.dumps(team_data, default=str)}")
        dynamodb_response = quest_status_table.put_item(
            Item=team_data,
            ConditionExpression=Attr("version").eq(current_version)
        )
    except ClientError as err:
        if err.response["Error"]["Code"] == 'ConditionalCheckFailedException':
            raise ValueError("The item was updated by another function since this function started. Check with the developer whether it is safe to ignore this error (the quest is not left in an inconsistent state for the team)") from err
        else:
            raise err
    print(f"Persisted team data back to the quest team status table: {json.dumps(dynamodb_response)}")