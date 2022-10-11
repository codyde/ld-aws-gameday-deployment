# Copyright 2022 Amazon.com and its affiliates; all rights reserved. 
# This file is Amazon Web Services Content and may not be duplicated or distributed without permission.
import json
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError


# Retrieve's team template output parameter from DynamoDB gdQuestsApi-QuestStates table
def retrieve_team_template_output_value(quests_api_client, quest_id, team_data, parameter_name):
    quest_status = quests_api_client.get_quest_for_team(team_data['team-id'], quest_id)
    print(f"get_quest_for_team: {quest_status}")
    stack_outputs = json.loads(quest_status['quest-team-enable-stack-outputs'])
    for output in stack_outputs:
        if output['OutputKey'] == parameter_name:
            parameter_value = output['OutputValue']
            print(f"Found parameter value {parameter_value}")
            return parameter_value
    # if we got here, there was a problem with the stack or the code or the output
    # Return an error value and we'll throw an exception later in the process for
    # better event operator experience
    return "ERROR"