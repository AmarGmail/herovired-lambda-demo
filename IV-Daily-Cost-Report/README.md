# IV - Daily AWS Cost Report Using Cost Explorer API and SNS

## Objective

Automate daily AWS cost monitoring using **AWS Lambda**, **AWS Cost Explorer**, **Amazon SNS**, and **Amazon EventBridge**.

The Lambda function retrieves the current month's AWS **Unblended Cost**, compares it against a configurable threshold, and sends an email notification through Amazon SNS when the threshold is exceeded.

---

# AWS Services Used

- AWS Lambda
- AWS Cost Explorer API
- Amazon SNS
- Amazon EventBridge Scheduler
- Amazon CloudWatch Logs
- IAM

---

# Features

- Retrieves Month-to-Date AWS Cost
- Uses Cost Explorer API
- Configurable cost threshold
- Sends SNS email notification
- Daily scheduled execution using EventBridge
- Detailed CloudWatch logging
- Uses Lambda Environment Variables

---

# IAM Permissions

The Lambda execution role requires:

```
ce:GetCostAndUsage
sns:Publish
logs:CreateLogGroup
logs:CreateLogStream
logs:PutLogEvents
```

The SNS Publish permission should be scoped to the SNS Topic ARN.

---

# Environment Variables

| Variable | Description |
|-----------|-------------|
| SNS_TOPIC_ARN | SNS Topic ARN |
| THRESHOLD | Cost threshold in USD |

Example

```
SNS_TOPIC_ARN=arn:aws:sns:us-east-1:123456789012:DailyCostAlerts
THRESHOLD=0.01
```

---

# Lambda Workflow

1. Triggered manually or by EventBridge.
2. Query AWS Cost Explorer.
3. Retrieve Month-to-Date Unblended Cost.
4. Compare cost against threshold.
5. If threshold exceeded:
   - Publish message to SNS.
   - Email notification sent.
6. Log execution details to CloudWatch.

---

# EventBridge Schedule

Example schedule:

```
Rate: 1 day
```

or

```
Cron: Every day at 09:00 UTC
```

---

# Testing

## Manual Test

Set a very low threshold.

Example:

```
THRESHOLD=0.0000001
```

Invoke the Lambda manually.

Expected output:

```
Month-to-date UnblendedCost: $0.0000004
Configured threshold: $0.0000001
ALERT: Spend exceeds threshold.
SNS alert published.
```

---

# CloudWatch Logs

CloudWatch captures:

- Cost Explorer response
- Current month cost
- Configured threshold
- SNS publish status
- SNS MessageId
- Exceptions

---

# Screenshots

- IAM Role Permissions
- SNS Topic and Email Subscription
- Lambda Test Execution
- CloudWatch Logs
- Email Notification

All screenshots are available under:

```
Screenshots/
```

---

# Project Structure

```
IV-Daily-Cost-Report/
│
├── lambda_function.py
├── README.md
└── Screenshots/
    ├── DailyCostReport-IAMRole-AWSLambdaBasicExecutionRole-InlinePolicy.jpg
    ├── DailyCostReport-SNS-Topic-SubscriptionConfirmation.jpg
    ├── DailyCostReport-Lambda_test_run.jpg
    └── DailyCostReport-CloudTraillSNSTpoic_EmailLogs.jpg
```

---

# Discussion

AWS provides **AWS Budgets** as a managed service for cost monitoring and alerts.

Managed Alternative: AWS Budgets can automatically monitor AWS spending and send notifications when predefined thresholds are exceeded, requiring little to no custom code.

Why use Lambda instead? Lambda provides greater flexibility for implementing custom business logic, such as sending alerts based on specific AWS services, applying anomaly detection, integrating with Slack or Microsoft Teams, or triggering automated remediation workflows in response to spending patterns.

---

# Notes

While testing on a Free Tier account with promotional credits, the AWS Billing dashboard displayed approximately **$10.16** in estimated usage, whereas the Cost Explorer API returned an **UnblendedCost** close to **$0.00** because promotional credits offset the actual billable amount. This behavior is expected and demonstrates the difference between usage costs and billable charges.

---
