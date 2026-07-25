# AWS Lambda Automation with Python (Boto3)

This repository contains hands-on AWS automation assignments implemented using **AWS Lambda**, **Python 3.12**, **Boto3**, **IAM**, **EventBridge**, **SNS**, **S3**, **EC2**, **EBS**, and **Cost Explorer**.

Each assignment is implemented as an independent project with its own source code, screenshots, and detailed documentation.

---

## Repository Structure

```
aws-lambda-function/
├── I-Automated-S3-Cleanup/
│   ├── lambda_function.py
│   ├── README.md
│   └── Screenshots/
│
├── II-EBSSnapshot-Create-Cleanup/
│   ├── lambda_function.py
│   ├── README.md
│   └── Snapshots/
│
├── III-AutoTag-EC2-Instances/
│   ├── lambda_function.py
│   ├── README.md
│   └── Screenshots/
│
└── IV-Daily-Cost-Report/
    ├── lambda_function.py
    ├── README.md
    └── Screenshots/
```

---

## Assignments

### I. Automated S3 Bucket Cleanup

Automatically deletes S3 objects older than a configurable number of days.

**AWS Services**

- AWS Lambda
- Amazon S3
- IAM
- EventBridge
- CloudWatch Logs

Documentation:

- [I-Automated-S3-Cleanup/README.md](I-Automated-S3-Cleanup/README.md)

---

### II. Automated EBS Snapshot Create & Cleanup

Creates EBS snapshots automatically and removes snapshots older than the configured retention period.

**AWS Services**

- AWS Lambda
- Amazon EC2
- Amazon EBS
- IAM
- EventBridge
- CloudWatch Logs

Documentation:

- [II-EBSSnapshot-Create-Cleanup/README.md](II-EBSSnapshot-Create-Cleanup/README.md)

---

### III. Auto Tag EC2 Instances

Automatically tags newly launched EC2 instances using EventBridge and Lambda.

Tags added:

- Owner
- Environment
- LaunchDate

**AWS Services**

- AWS Lambda
- Amazon EC2
- IAM
- EventBridge
- CloudWatch Logs

Documentation:

- [III-AutoTag-EC2-Instances/README.md](III-AutoTag-EC2-Instances/README.md)

---

### IV. Daily AWS Cost Alert

Retrieves Month-to-Date AWS costs using the Cost Explorer API and publishes alerts through Amazon SNS when a configurable threshold is exceeded.

**AWS Services**

- AWS Lambda
- AWS Cost Explorer API
- Amazon SNS
- IAM
- EventBridge
- CloudWatch Logs

Documentation:

- [IV-Daily-Cost-Report/README.md](IV-Daily-Cost-Report/README.md)

---

## Technologies

- Python 3.12
- Boto3
- AWS Lambda
- IAM Roles & Policies
- EventBridge Scheduler
- Amazon SNS
- Amazon S3
- Amazon EC2
- Amazon EBS
- AWS Cost Explorer
- CloudWatch Logs

---

## Notes

- All Lambda functions use **IAM Roles** (no hardcoded AWS credentials).
- Configuration values are externalized using **Lambda Environment Variables**.
- Each assignment contains screenshots demonstrating deployment, testing, and successful execution.
- AI tools are used specially to generate the README files and lambda_function.py.
- The first 4 assignments are listed here.