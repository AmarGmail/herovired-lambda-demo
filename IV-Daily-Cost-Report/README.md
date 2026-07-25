#Objective: Build an automated alert when AWS spend exceeds a threshold.


##Step 1: Create SNS Topic
Create a standard SNS Topic and subscribe to an email.

##Step 2: Create IAM Role with Inline policy and attach AWSLambdaBasicExecutionRole.

##Step 3: Create a lambda function and attach the execution policy above.
There are two functions get_month_to_date_cost and publish_alert(cost)
which are called from lambda_handler to get the cost of the month and trigger alert to SNS queue which in turn send an email to the subscriber.

##Step 4: Verified lambda test function

##step 5: verified cloudTril and CloudWatch for email event

###Discussion Point:
Managed Alternative: AWS Budgets can automatically monitor AWS spending and send notifications when predefined thresholds are exceeded, requiring little to no custom code.
Why use Lambda instead? Lambda provides greater flexibility for implementing custom business logic, such as sending alerts based on specific AWS services, applying anomaly detection, integrating with Slack or Microsoft Teams, or triggering automated remediation workflows in response to spending patterns.


