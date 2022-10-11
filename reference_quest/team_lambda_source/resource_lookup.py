# Copyright 2022 Amazon.com and its affiliates; all rights reserved. 
# This file is Amazon Web Services Content and may not be duplicated or distributed without permission.
import boto3
import urllib3
import cfn_response
import json

http = urllib3.PoolManager()

# This function is triggered by a CloudFormation custom resource. It looks up default resources in an AWS account, such as
# default VPC, subnets, CIDR, and return them to the CFN template to be referenced in other blocks. The main purpose is
# reuse of existing resources instead of creating new ones and possibly exceeding cloud quotas.
def lambda_handler(event, context):
    try:
        print(f"event: {json.dumps(event)}")
        print(f"context: {str(context)}")

        response_data = {}

        ec2_client = boto3.client('ec2')

        if event['RequestType'] == 'Delete':
            try:
                cfn_response.send(event, context, cfn_response.SUCCESS, response_data)
                return
            except Exception as e:
                cfn_response.send(event, context, cfn_response.FAILED, response_data)
                print(f"Custom resource lambda execution for delete has failed: {e}")
                return
        else:  # request type is create or update
            try:
                vpcs = ec2_client.describe_vpcs(Filters=[{
                    'Name': 'is-default',
                    'Values': ['true']
                }])
                print(f"Custom resource lambda execution for vpcs: {vpcs}")
                vpc = vpcs["Vpcs"][0]["VpcId"]
                cidr = vpcs["Vpcs"][0]["CidrBlock"]

                response_data["VpcId"] = vpc
                response_data["CidrBlock"] = cidr


                print(f"Custom resource lambda execution for vpc: {vpc}")
                subnets = ec2_client.describe_subnets(Filters=[{
                    'Name': 'vpc-id',
                    'Values': [vpc]
                }, {
                    'Name': 'default-for-az',
                    'Values': ["true"]
                },
                ])

                print(f"Custom resource lambda execution for subnets: {subnets}")

                subnets = get_three_subnets(subnets)

                response_data["SubnetId1"] = subnets[0]
                response_data["SubnetId2"] = subnets[1]
                response_data["SubnetId3"] = subnets[2]

                default_security_group = ec2_client.describe_security_groups(GroupNames=['default'])
                response_data["SecurityGroupIds"] = default_security_group["SecurityGroups"][0]["GroupId"]

                route_tables = ec2_client.describe_route_tables(Filters=[{
                    'Name': 'vpc-id',
                    'Values': [vpc]
                }, {
                    'Name': 'association.main',
                    'Values': ["true"]
                },
                ])
                response_data["RouteTableId"] = route_tables["RouteTables"][0]["RouteTableId"]

                print(f"Custom resource lambda execution for response_data: {response_data}")

                cfn_response.send(event, context, cfn_response.SUCCESS, response_data)
                return
            except Exception as e:
                cfn_response.send(event, context, cfn_response.FAILED, response_data)
                print(f"Lambda execution has failed! : {e}")
                return

    except Exception as e:
        cfn_response.send(event, context, cfn_response.FAILED, {}, None)
        print(f"Lambda execution has failed unexpectedly, unknown request type (probably a debugging code issue): {e}")
        return


def get_three_subnets(subnets):

    res = []

    for subnet in subnets["Subnets"]:
        if len(res) == 3:
            break
        availability_zone_id = subnet["AvailabilityZoneId"]
        #remove problematic AZ
        if availability_zone_id == "use1-az3":
            continue

        subnetId = subnet["SubnetId"]
        res.append(subnetId)

    # Fill out with blanks if less than 3 subnets
    for x in range(3):
        if x+1 > len(res):
            res.append("")

    return res


