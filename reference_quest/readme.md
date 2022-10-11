# AWS GameDay Quest - Reference Quest
Owners and Maintainers: Lorenzo Ciaravola (lciaravo@)

## Documentation
[Quest Wiki](https://w.amazon.com/bin/view/AWS_GameDay/Quests/reference_quest)

## TODO
Below is a list of action items for developers to do, who are using this reference quest as a baseline. Delete the entries as you resolve them.

- Modify package_quest_init.sh as follow:
	BUILD_QUEST_ID=<replace with your quest id>
	BUILD_QUEST_BUCKET_NAME=<replace with your unique bucket name for local development>
	BUILD_QUEST_BUCKET_PREFIX=<optional bucket prefix for local development>
	Do not modify the commented out BUILD_QUEST_BUCKET_NAME and BUILD_QUEST_BUCKET_PREFIX pointing to production values
	Remove the S3 upload of curl.jpeg, as it's an example, and replace with upload of your artifacts if needed
- Replace QuestId parameter in central_cfn.yaml and team_enable_cfn.yaml with your quest Id
- If your quest does not use a team_enable_cfn.yaml template, delete the file, empty the quest-team-cfn-enable property in dev-quests-data.json, and modify the packaging scripts accordingly
- Make appropriate changes to the dev-quests-data.json in your quest folder
- Remove all mappings and resources from team_enable_cfn.yaml if not needed for your quest
- Remove Outputs from team_enable_cfn.yaml if not needed for your quest or add new ones. Note you will also need to modify the retrieve_team_template_output_value call in init_lambda.py appropriately.
- Modify iam.txt to include the permissions required by your quest. These will later on be copied over to production artifacts by the system administrator. Make sure to abide by the principle of least privilege
- Fill in operator_guide.md with any information the event operator needs to know and actions that need to be performed to properly set up the quest
- Fill in supporter_guide.md with detailed instructions on how to solve all the quest challenges



