import json
import boto3
from datetime import timedelta, datetime, timezone
import os

# Initilize Cost Explorer, STS and SNS
ce = boto3.client('ce')
sns = boto3.client("sns")
#sts = boto3.client("sts")

# Get environment variables
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]
THRESHOLD = float(os.environ.get("THRESHOLD", "50"))


# Function to get month to date cost
def get_month_to_date_cost():

    today = datetime.now(timezone.utc).date()
    start_of_month = today.replace(day=1)

    print(f"Querying cost from {start_of_month} to {today + timedelta(days=1)}")
    response = ce.get_cost_and_usage(
        TimePeriod={
            'Start': str(start_of_month),
            'End': str(today + timedelta(days=1))
        },
        Granularity='MONTHLY',
        Metrics=['UnblendedCost']
    )
    print("===== Cost Explorer Response =====")
    print(json.dumps(response, indent=2, default=str))
    print("==================================")   

    amount = response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]    
    return float(amount)

# Function to publish alert
def publish_alert(cost):
    message = (
        f"AWS Cost Alert\n"
        f"Month-to-date spend: ${cost:.7f}\n"
        f"Threshold: ${THRESHOLD:.7f}\n"
        f"Status: EXCEEDED"
    )

    response = sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=f"AWS Cost Alert: ${cost:.7f} exceeds ${THRESHOLD:.7f}",
        Message=message
    )
    print(f"SNS alert published to {SNS_TOPIC_ARN}")
    print(f"SNS MessageId: {response['MessageId']}")

#
# Main Lambda handler
def lambda_handler(event, context):
    # print(json.dumps(event, indent=2))
    
    # identity = sts.get_caller_identity()

    # print("===== STS Identity =====")
    # print(json.dumps(identity, indent=2))
    # print("========================")
    
    try:
        
        cost = get_month_to_date_cost()
        print(f"Month-to-date UnblendedCost: ${cost:.7f}")
        print(f"Configured threshold: ${THRESHOLD:.7f}")
        
        if cost > THRESHOLD:
            print(f"ALERT: Spend ${cost:.7f} exceeds threshold ${THRESHOLD:.7f}")
            publish_alert(cost)
        else:
            print(f"OK: Spend ${cost:.7f} is within threshold.")

    except Exception as e:
        print(f"ERROR: {e}")
        raise

    return {
        'statusCode': 200,
        'this_month_unblended_cost': f'${cost:.7f}',
        'threshold': THRESHOLD,
        'alert_sent': cost > THRESHOLD
    }