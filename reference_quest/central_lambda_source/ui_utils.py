# Copyright 2022 Amazon.com and its affiliates; all rights reserved. 
# This file is Amazon Web Services Content and may not be duplicated or distributed without permission.
import boto3
from datetime import datetime 
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

# In a development environment, we are likely dealing with a situation where SCPs or other organizational
# mechanisms block public buckets/objects, so signed URL must be used.
# :param bucket_name: Name of the bucket to the the URL for
# :param object_key: full key with prefix of the object to get the URL for
# :param signed_duration: if signing, how long should the signed URL be valid
# :returns: a URL compatible with unauthenticated requests.get()
def generate_signed_or_open_url(bucket_name: str, object_key: str, signed_duration=60):
    try:
        if "ee-assets-prod" in bucket_name:
            print("Detected Event Engine bucket. Inferring the quest is running in EE")
            public_url = f"https://s3.amazonaws.com/{bucket_name}/{object_key}"
            result = public_url
        else:
            signed_url = boto3.client("s3").generate_presigned_url('get_object',
                                            Params={
                                                'Bucket': bucket_name,
                                                'Key': object_key
                                            },
                                            ExpiresIn=signed_duration)
            result = signed_url
    except Exception as e:
        print(f"Unable to sign content: {e}")

    return result