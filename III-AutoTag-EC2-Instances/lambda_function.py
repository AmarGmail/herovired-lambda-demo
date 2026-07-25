import json
import os
from datetime import datetime, timezone
import boto3
from botocore.exceptions import ClientError


OWNER = os.environ.get("OWNER", "admin")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "dev")

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    print(json.dumps(event, indent=2))

    instance_id = event.get('detail', {}).get('instance-id')
    print(f'Extracted Instance ID: {instance_id}')

    if not instance_id:
        print('No instance ID found in event')
        return {
            'statusCode': 400
        }

    tags = [
        {'Key': 'Owner','Value': OWNER},
        {'Key': 'Environment','Value': ENVIRONMENT},
        {'Key': 'LaunchDate','Value': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}
    ]
    
    #Check Instance state
    response = ec2.describe_instances(InstanceIds=[instance_id])
    state = response["Reservations"][0]["Instances"][0]["State"]["Name"]
    if state != "running":
        print("Instance is not yet running.")
        return {
            "statusCode": 400,
            "message": f"Instance state is {state}; skipping tagging."
        }
    print(f"Instance {instance_id} State: {state}")

    # Tag the instance
    try:
        print(f'Attempting to tag instance {instance_id} with {tags}')
        ec2.create_tags(Resources=[instance_id], Tags=tags)
        print(f'Tags added to instance {instance_id}: {tags}')
    except ClientError as e:
        print(f"ERROR: {e}")
        raise
    
    return {
        'statusCode': 200,
        "instance_id": instance_id,
        "tags": tags,
        "state": state
    }