# Deployment Guide

## Prerequisites
- AWS CLI configured with appropriate permissions
- Python 3.9+ installed
- Required Python packages: awsiotsdk, boto3
- Access to AWS Console (for verification)

## 1. Environment Setup

### Directory Structure
```bash
/ANZ_Project/
├── certificates/
├── policies/
├── lambda/
├── scripts/
└── tests/

Required Files
# Create project directories
mkdir -p ANZ_Project/{certificates,policies,lambda,scripts,tests}
cd ANZ_Project

2. IoT Core Configuration
Create Policy
# Create policy file
cat << 'EOF' > policies/ANZpoclab-policy.json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iot:Connect",
                "iot:Publish",
                "iot:Subscribe",
                "iot:Receive"
            ],
            "Resource": [
                "arn:aws:iot:REGION:ACCOUNT:client/*",
                "arn:aws:iot:REGION:ACCOUNT:topic/livesense/poc/*/ANZlab",
                "arn:aws:iot:REGION:ACCOUNT:topicfilter/livesense/poc/*/ANZlab"
            ]
        }
    ]
}
EOF

# Deploy policy
aws iot create-policy \
    --policy-name "ANZpoclab" \
    --policy-document file://policies/ANZpoclab-policy.json

Create Certificates
# Generate certificates
aws iot create-keys-and-certificate \
    --set-as-active \
    --certificate-pem-outfile "certificates/ANZpoc-cert.pem" \
    --public-key-outfile "certificates/ANZpoc-public.key" \
    --private-key-outfile "certificates/ANZpoc-private.key"

# Download Root CA
curl https://www.amazontrust.com/repository/AmazonRootCA1.pem \
    -o certificates/AmazonRootCA1.pem

3. Lambda Functions Deployment
Main Processing Lambda
# Create Lambda function file
cat << 'EOF' > lambda/ANZ-PoC.py
[Lambda function code here - sanitized]
EOF

# Package and deploy
cd lambda
zip ANZ-PoC.zip ANZ-PoC.py
aws lambda create-function \
    --function-name "ANZ-PoC" \
    --runtime python3.9 \
    --handler ANZ-PoC.lambda_handler \
    --role "YOUR_LAMBDA_ROLE_ARN" \
    --zip-file fileb://ANZ-PoC.zip

API Lambda
# Create API Lambda function
cd lambda
zip mobile-ANZ-poc.zip mobile-ANZ-poc.py
aws lambda create-function \
    --function-name "mobile-ANZ-poc" \
    --runtime python3.9 \
    --handler mobile-ANZ-poc.lambda_handler \
    --role "YOUR_LAMBDA_ROLE_ARN" \
    --zip-file fileb://mobile-ANZ-poc.zip

4. DynamoDB Setup
# Create table
aws dynamodb create-table \
    --table-name ANZpoclab_data \
    --attribute-definitions AttributeName=id,AttributeType=S \
    --key-schema AttributeName=id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST

5. API Gateway Configuration
# Create API
aws apigateway create-rest-api \
    --name "ANZ-poc-api" \
    --description "API for ANZ PoC mobile access"

# Configure endpoints [Details in API documentation]

6. Testing Deployment
# Sample simulator code
[Python simulator code here - sanitized]

Verification Steps
IoT Core Connection Test
Lambda Function Test
DynamoDB Data Verification
API Endpoint Test


7. Monitoring Setup
CloudWatch Alarms
# Create basic monitoring alarm
aws cloudwatch put-metric-alarm \
    --alarm-name "ANZ-Lambda-Errors" \
    --metric-name Errors \
    --namespace AWS/Lambda \
    --statistic Sum \
    --period 300 \
    --threshold 1 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 1 \
    --alarm-actions "YOUR_SNS_TOPIC_ARN"

8. Cleanup Instructions
**# Remove resources if needed
aws lambda delete-function --function-name "ANZ-PoC"
aws lambda delete-function --function-name "mobile-ANZ-poc"
aws dynamodb delete-table --table-name ANZpoclab_data
aws iot delete-policy --policy-name "ANZpoclab"

# Deployment Checklist

## Pre-deployment
- **AWS CLI configured**
- **Required permissions verified**
- **Directories created**
- **Certificates ready**

## Deployment
- **IoT Core policy created**
- **Certificates generated and stored**
- **Lambda functions deployed**
- **DynamoDB table created**
- **API Gateway configured**

## Post-deployment
- **All components tested**
- **Monitoring configured**
- **Documentation updated**
- **Access verified**


