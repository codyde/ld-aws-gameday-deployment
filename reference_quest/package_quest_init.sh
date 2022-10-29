# Copyright 2022 Amazon.com and its affiliates; all rights reserved. 
# This file is Amazon Web Services Content and may not be duplicated or distributed without permission.

#!/bin/bash

QUEST_ROOT_DIR=${PWD}
BUILD_QUEST_NAME="LaunchDarkly Feature Flags"
BUILD_QUEST_ID=7bb514a9-a6dc-4fc0-a797-3f4a7bbd17bb
BUILD_QUEST_BUCKET_NAME=${QDK_ASSETS_BUCKET}                              # when deploying locally
#BUILD_QUEST_BUCKET_NAME=ee-assets-prod-us-east-1                         # when deploying to production
# Include trailing / if a value is defined!
BUILD_QUEST_BUCKET_PREFIX=                                              # when deploying locally
#BUILD_QUEST_BUCKET_PREFIX=modules/9c0e89820b864addaed45ec2f5440379/v5/   # when deploying to production
QUEST_ARTIFACTS_ZIP=gdQuests-${BUILD_QUEST_ID}-quest-artifacts.zip        # don't change
APP_ARTIFACTS_ZIP=Archive.zip

if [[ -z "${AWS_GAMEDAY_PROFILE}" ]]; then
  PROFILE_ARGUMENT=""
  echo Not using AWS_GAMEDAY_PROFILE
else
  PROFILE_ARGUMENT="--profile $AWS_GAMEDAY_PROFILE"
fi


echo -e "BUILD_QUEST_BUCKET_NAME="${BUILD_QUEST_BUCKET_NAME}
echo -e "BUILD_QUEST_BUCKET_PREFIX="${BUILD_QUEST_BUCKET_PREFIX}
echo -e "\n Working from "${QUEST_ROOT_DIR}

# Create the build directory if it doesn't exist
mkdir -p build

########################################################
## Pipeline Assets                                    ##
## Zip up all quest assets (with no dependencies)     ##
## and upload to S3. The quest artifacts zip will     ##
## be used to seed CodeCommit upon it creation        ##
## Note: the zip cannot exceed 6MB!                   ##
########################################################
echo -e "\nZipping up the quest artifacts......"
cd ${QUEST_ROOT_DIR}
zip -q9r - . > ${QUEST_ROOT_DIR}/build/${QUEST_ARTIFACTS_ZIP} . -x \*artifacts\* \*build\* central_lambda_source/.venv/**\* team_lambda_source/.venv/**\*


############################
## Upload to S3           ##
############################
echo -e "\nUploading Quest artifacts to S3 for seeding CodeCommit"
cd ${QUEST_ROOT_DIR}/build
aws s3 cp ${QUEST_ARTIFACTS_ZIP} s3://${BUILD_QUEST_BUCKET_NAME}/${BUILD_QUEST_BUCKET_PREFIX}${BUILD_QUEST_ID}/${QUEST_ARTIFACTS_ZIP} ${PROFILE_ARGUMENT}

echo -e "\nCopying application assets to S3 to seed in CodeCommit"
cd ..
aws s3 cp ${APP_ARTIFACTS_ZIP} s3://${BUILD_QUEST_BUCKET_NAME}/${APP_ARTIFACTS_ZIP}

echo -e "\nCopying team lambda source to S3"
aws s3 cp team_lambda_source.zip s3://${BUILD_QUEST_BUCKET_NAME}/${BUILD_QUEST_BUCKET_PREFIX}${BUILD_QUEST_ID}/gdQuests-team-lambda-source.zip



echo Complete: $(date)
