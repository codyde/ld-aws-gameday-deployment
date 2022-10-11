# Copyright 2022 Amazon.com and its affiliates; all rights reserved. 
# This file is Amazon Web Services Content and may not be duplicated or distributed without permission.

#!/bin/bash

# set trace flag so that all commands output to CodeBuild Log
set -x
QUEST_ROOT_DIR=${PWD}

# The following vars are set by the Pipeline in real-time
echo -e "PIPELINE_BUCKET=" ${PIPELINE_BUCKET}
echo -e "PIPELINE_BUCKET_PREFIX=" ${PIPELINE_BUCKET_PREFIX}
#echo -e "\n Working from " ${QUEST_ROOT_DIR}

# Create the build directory if it doesn't exist
mkdir -p build || exit 1


############################
## Central Account Assets ##
############################
echo -e "\nZipping up the Quest Central Lambda source..."
cd ${QUEST_ROOT_DIR}/central_lambda_source || exit 1

if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv || exit 1
fi
source .venv/bin/activate || exit 1
pip install -r requirements.txt || exit 1
deactivate || exit 1
cd ${QUEST_ROOT_DIR}/central_lambda_source/.venv/lib/python3*/site-packages || exit 1
zip -qr9 - . > ${QUEST_ROOT_DIR}/build/gdQuests-lambda-source.zip --exclude "boto*" "s3transfer*" "pip*" "jmespath*" || exit 1

cd ${QUEST_ROOT_DIR}/central_lambda_source || exit 1
zip -g ${QUEST_ROOT_DIR}/build/gdQuests-lambda-source.zip *.py || exit 1


############################
## Team Account Assets    ##
############################
echo -e "\nZipping up the Quest Team Lambda source..."
cd ${QUEST_ROOT_DIR}/team_lambda_source  ||  exit 1
if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv  ||  exit 1
fi
source .venv/bin/activate  || exit 1
pip install -r requirements.txt || exit 1
deactivate
cd ${QUEST_ROOT_DIR}/team_lambda_source/.venv/lib/python3*/site-packages || exit 1
zip -qr9 - . > ${QUEST_ROOT_DIR}/build/gdQuests-team-lambda-source.zip . --exclude "boto*" "s3transfer*" "pip*" "jmespath*" || exit 1
cd ${QUEST_ROOT_DIR}/team_lambda_source || exit 1
zip -g ${QUEST_ROOT_DIR}/build/gdQuests-team-lambda-source.zip *.py  || exit 1


############################
## Upload to S3           ##
############################
echo -e "\nUploading Quest artifacts to S3"
cd ${QUEST_ROOT_DIR}/build
aws s3 cp gdQuests-lambda-source.zip s3://${PIPELINE_BUCKET}/${PIPELINE_BUCKET_PREFIX}/gdQuests-lambda-source.zip --sse aws:kms --sse-kms-key-id ${KMS_KEY} || exit 1
aws s3 cp gdQuests-team-lambda-source.zip s3://${PIPELINE_BUCKET}/${PIPELINE_BUCKET_PREFIX}/gdQuests-team-lambda-source.zip --sse aws:kms --sse-kms-key-id ${KMS_KEY} || exit 1

echo Complete: $(date)
