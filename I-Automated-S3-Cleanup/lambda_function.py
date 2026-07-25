import boto3
import os
from datetime import datetime, timezone, timedelta

# call boto3 client for s3
s3_client = boto3.client("s3")
BUCKET_NAME = os.environ["BUCKET_NAME"]
DELETE_DAYS = int(os.environ["DELETE_DAYS"])
#DELETE_MINS = 60

def lambda_handler(event, context):

    cutoff_time = datetime.now(timezone.utc) - timedelta(days=DELETE_DAYS)
    # cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=DELETE_MINS)

    paginator = s3_client.get_paginator('list_objects_v2')

    deleted = []

    for page in paginator.paginate(Bucket=BUCKET_NAME):

        if "Contents" not in page:
            continue

        for object in page["Contents"]:

            if object["LastModified"] < cutoff_time:
                s3_client.delete_object(
                    Bucket=BUCKET_NAME,
                    Key=object["Key"]
                )

                print(f"Deleted: {object["Key"]} (LastModified: {object["LastModified"]})")
                deleted.append(object["Key"])

    return {
        "DeletedObjects": deleted,
        "Count": len(deleted)
    }    