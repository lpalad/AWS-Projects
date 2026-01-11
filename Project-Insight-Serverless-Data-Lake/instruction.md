# Project Insight - Step-by-Step Lab Instructions

## Overview

Build a production-grade serverless data lake for e-commerce clickstream analytics.

```
Web Servers → Firehose → Lambda → S3 Raw → Crawler → ETL → S3 Curated → Athena
                                                ↑
                                          Step Functions
                                          (Orchestrator)
```

**Estimated Cost:** $0.30 - $1.00 for 48 hours
**Time to Complete:** 2-3 hours

---

# PHASE 1: AWS Account & Security Setup

## Step 1.1: Create IAM User for CLI Access

We need a dedicated IAM user for terminal access. Never use root account.

### 1.1.1 - Login to AWS Console

```
1. Go to: https://console.aws.amazon.com/
2. Login with your root account or existing admin account
3. Make sure you're in your preferred region (e.g., us-east-1)
```

**Your feedback:** Confirm you're logged in and which region you're using.

---

### 1.1.2 - Create IAM User

```
1. Go to: IAM → Users → Create user
2. User name: project-insight-admin
3. Check: "Provide user access to the AWS Management Console" (optional)
4. Select: "I want to create an IAM user"
5. Password: Auto-generate or create your own
6. Click: Next
```

**Your feedback:** Confirm user name created.

---

### 1.1.3 - Attach Permissions

For this lab, we'll use administrator access. In production, you'd use least privilege.

```
1. Select: "Attach policies directly"
2. Search and check: "AdministratorAccess"
3. Click: Next
4. Click: Create user
```

**Your feedback:** Confirm user created with AdministratorAccess.

---

### 1.1.4 - Create Access Keys for CLI

```
1. Click on the user: project-insight-admin
2. Go to: Security credentials tab
3. Scroll to: Access keys
4. Click: Create access key
5. Select: "Command Line Interface (CLI)"
6. Check: "I understand the above recommendation..."
7. Click: Next
8. Description tag: "Project Insight CLI Access"
9. Click: Create access key
```

**IMPORTANT: Save these keys! You won't see them again.**

```
Access Key ID:     [SAVE THIS]
Secret Access Key: [SAVE THIS]
```

**Your feedback:** Confirm you saved both keys securely.

---

## Step 1.2: Install and Configure AWS CLI

### 1.2.1 - Check if AWS CLI is installed

Run this in your terminal:

```bash
aws --version
```

**Expected output:**
```
aws-cli/2.x.x Python/3.x.x Darwin/...
```

If not installed, install it:

**macOS:**
```bash
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
sudo installer -pkg AWSCLIV2.pkg -target /
```

**Your feedback:** Paste the output of `aws --version`

---

### 1.2.2 - Configure AWS CLI with your credentials

Run this:

```bash
aws configure
```

Enter the following when prompted:

```
AWS Access Key ID [None]: <paste your Access Key ID>
AWS Secret Access Key [None]: <paste your Secret Access Key>
Default region name [None]: us-east-1
Default output format [None]: json
```

**Your feedback:** Confirm configuration complete.

---

### 1.2.3 - Test AWS CLI connection

Run this to verify your credentials work:

```bash
aws sts get-caller-identity
```

**Expected output:**
```json
{
    "UserId": "AIDAXXXXXXXXXXXXXXXXX",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/project-insight-admin"
}
```

**Your feedback:** Paste the output (you can hide your account number if you want).

---

## Step 1.3: Set Environment Variables

We'll use variables to avoid typing long bucket names repeatedly.

### 1.3.1 - Get your AWS Account ID

Run this:

```bash
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "Your AWS Account ID: $AWS_ACCOUNT_ID"
```

**Your feedback:** Confirm your account ID is displayed.

---

### 1.3.2 - Set project variables

Run these commands to set up variables for the session:

```bash
export AWS_REGION="us-east-1"
export PROJECT_NAME="project-insight"
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# S3 Bucket names (must be globally unique)
export RAW_BUCKET="${PROJECT_NAME}-raw-${AWS_ACCOUNT_ID}"
export CURATED_BUCKET="${PROJECT_NAME}-curated-${AWS_ACCOUNT_ID}"
export SCRIPTS_BUCKET="${PROJECT_NAME}-scripts-${AWS_ACCOUNT_ID}"
export ATHENA_BUCKET="${PROJECT_NAME}-athena-${AWS_ACCOUNT_ID}"

# Print to verify
echo "Region: $AWS_REGION"
echo "Raw Bucket: $RAW_BUCKET"
echo "Curated Bucket: $CURATED_BUCKET"
echo "Scripts Bucket: $SCRIPTS_BUCKET"
echo "Athena Bucket: $ATHENA_BUCKET"
```

**Your feedback:** Paste the output showing all bucket names.

---

# PHASE 2: Create S3 Buckets

## Step 2.1: Create the Raw Data Bucket (Bronze)

This bucket will store raw JSON files from Kinesis Firehose.

```bash
aws s3api create-bucket \
    --bucket $RAW_BUCKET \
    --region $AWS_REGION
```

**Note:** If you're NOT in us-east-1, add this parameter:
```bash
    --create-bucket-configuration LocationConstraint=$AWS_REGION
```

**Your feedback:** Confirm bucket created or paste any error.

---

## Step 2.2: Create the Curated Data Bucket (Silver)

This bucket will store clean Parquet files.

```bash
aws s3api create-bucket \
    --bucket $CURATED_BUCKET \
    --region $AWS_REGION
```

**Your feedback:** Confirm bucket created.

---

## Step 2.3: Create the Scripts Bucket

This bucket will store Lambda code and Glue ETL scripts.

```bash
aws s3api create-bucket \
    --bucket $SCRIPTS_BUCKET \
    --region $AWS_REGION
```

**Your feedback:** Confirm bucket created.

---

## Step 2.4: Create the Athena Results Bucket

This bucket will store Athena query results.

```bash
aws s3api create-bucket \
    --bucket $ATHENA_BUCKET \
    --region $AWS_REGION
```

**Your feedback:** Confirm bucket created.

---

## Step 2.5: Verify all buckets exist

```bash
aws s3 ls | grep $PROJECT_NAME
```

**Expected output:**
```
2024-01-10 12:00:00 project-insight-raw-123456789012
2024-01-10 12:00:00 project-insight-curated-123456789012
2024-01-10 12:00:00 project-insight-scripts-123456789012
2024-01-10 12:00:00 project-insight-athena-123456789012
```

**Your feedback:** Paste the output showing all 4 buckets.

---

## Step 2.6: Block public access on all buckets

Security best practice - block all public access:

```bash
for bucket in $RAW_BUCKET $CURATED_BUCKET $SCRIPTS_BUCKET $ATHENA_BUCKET; do
    aws s3api put-public-access-block \
        --bucket $bucket \
        --public-access-block-configuration \
        "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
    echo "Blocked public access on: $bucket"
done
```

**Your feedback:** Confirm all 4 buckets have public access blocked.

---

# PHASE 3: Create IAM Roles

## Step 3.1: Create IAM Role for Lambda (Firehose Data Cleansing)

### 3.1.1 - Create the trust policy file

Run this to create the trust policy:

```bash
cat > /tmp/lambda-trust-policy.json << 'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF
```

**Your feedback:** Confirm file created.

---

### 3.1.2 - Create the Lambda role

```bash
aws iam create-role \
    --role-name project-insight-lambda-role \
    --assume-role-policy-document file:///tmp/lambda-trust-policy.json \
    --description "Role for Project Insight Lambda functions"
```

**Your feedback:** Confirm role created (you'll see JSON output with the role ARN).

---

### 3.1.3 - Attach basic Lambda execution policy

```bash
aws iam attach-role-policy \
    --role-name project-insight-lambda-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

**Your feedback:** Confirm policy attached (no output means success).

---

## Step 3.2: Create IAM Role for Kinesis Firehose

### 3.2.1 - Create the trust policy file

```bash
cat > /tmp/firehose-trust-policy.json << 'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "firehose.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF
```

**Your feedback:** Confirm file created.

---

### 3.2.2 - Create the Firehose role

```bash
aws iam create-role \
    --role-name project-insight-firehose-role \
    --assume-role-policy-document file:///tmp/firehose-trust-policy.json \
    --description "Role for Project Insight Kinesis Firehose"
```

**Your feedback:** Confirm role created.

---

### 3.2.3 - Create Firehose permissions policy

```bash
cat > /tmp/firehose-permissions-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::${RAW_BUCKET}",
                "arn:aws:s3:::${RAW_BUCKET}/*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "lambda:InvokeFunction"
            ],
            "Resource": "arn:aws:lambda:${AWS_REGION}:${AWS_ACCOUNT_ID}:function:project-insight-data-cleanse"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
EOF
```

**Your feedback:** Confirm file created.

---

### 3.2.4 - Attach the policy to Firehose role

```bash
aws iam put-role-policy \
    --role-name project-insight-firehose-role \
    --policy-name firehose-s3-lambda-access \
    --policy-document file:///tmp/firehose-permissions-policy.json
```

**Your feedback:** Confirm policy attached.

---

## Step 3.3: Create IAM Role for Glue (Crawler & ETL)

### 3.3.1 - Create the trust policy file

```bash
cat > /tmp/glue-trust-policy.json << 'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "glue.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF
```

**Your feedback:** Confirm file created.

---

### 3.3.2 - Create the Glue role

```bash
aws iam create-role \
    --role-name project-insight-glue-role \
    --assume-role-policy-document file:///tmp/glue-trust-policy.json \
    --description "Role for Project Insight Glue Crawler and ETL"
```

**Your feedback:** Confirm role created.

---

### 3.3.3 - Attach AWS managed Glue policy

```bash
aws iam attach-role-policy \
    --role-name project-insight-glue-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole
```

**Your feedback:** Confirm policy attached.

---

### 3.3.4 - Create S3 access policy for Glue

```bash
cat > /tmp/glue-s3-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::${RAW_BUCKET}",
                "arn:aws:s3:::${RAW_BUCKET}/*",
                "arn:aws:s3:::${CURATED_BUCKET}",
                "arn:aws:s3:::${CURATED_BUCKET}/*",
                "arn:aws:s3:::${SCRIPTS_BUCKET}",
                "arn:aws:s3:::${SCRIPTS_BUCKET}/*"
            ]
        }
    ]
}
EOF
```

**Your feedback:** Confirm file created.

---

### 3.3.5 - Attach S3 policy to Glue role

```bash
aws iam put-role-policy \
    --role-name project-insight-glue-role \
    --policy-name glue-s3-access \
    --policy-document file:///tmp/glue-s3-policy.json
```

**Your feedback:** Confirm policy attached.

---

## Step 3.4: Create IAM Role for Step Functions

### 3.4.1 - Create the trust policy file

```bash
cat > /tmp/stepfunctions-trust-policy.json << 'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "states.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF
```

**Your feedback:** Confirm file created.

---

### 3.4.2 - Create the Step Functions role

```bash
aws iam create-role \
    --role-name project-insight-stepfunctions-role \
    --assume-role-policy-document file:///tmp/stepfunctions-trust-policy.json \
    --description "Role for Project Insight Step Functions"
```

**Your feedback:** Confirm role created.

---

### 3.4.3 - Create Step Functions permissions policy

```bash
cat > /tmp/stepfunctions-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "glue:StartCrawler",
                "glue:GetCrawler",
                "glue:StartJobRun",
                "glue:GetJobRun",
                "glue:GetJobRuns"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "sns:Publish"
            ],
            "Resource": "arn:aws:sns:${AWS_REGION}:${AWS_ACCOUNT_ID}:project-insight-alerts"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}
EOF
```

**Your feedback:** Confirm file created.

---

### 3.4.4 - Attach policy to Step Functions role

```bash
aws iam put-role-policy \
    --role-name project-insight-stepfunctions-role \
    --policy-name stepfunctions-glue-sns-access \
    --policy-document file:///tmp/stepfunctions-policy.json
```

**Your feedback:** Confirm policy attached.

---

## Step 3.5: Verify all roles exist

```bash
aws iam list-roles --query "Roles[?contains(RoleName, 'project-insight')].RoleName" --output table
```

**Expected output:**
```
-----------------------------------------
|              ListRoles                |
+---------------------------------------+
|  project-insight-firehose-role        |
|  project-insight-glue-role            |
|  project-insight-lambda-role          |
|  project-insight-stepfunctions-role   |
+---------------------------------------+
```

**Your feedback:** Paste the output showing all 4 roles.

---

# PHASE 4: Create Lambda Function (Data Cleansing)

## Step 4.1: Create the Lambda function code

### 4.1.1 - Create the Python file

```bash
mkdir -p /tmp/lambda-code

cat > /tmp/lambda-code/lambda_function.py << 'EOF'
import json
import base64
import re
from datetime import datetime

def mask_ip(ip):
    """Mask the last two octets of an IP address."""
    if ip and isinstance(ip, str):
        parts = ip.split('.')
        if len(parts) == 4:
            return f"{parts[0]}.{parts[1]}.xxx.xxx"
    return ip

def clean_string(value):
    """Strip whitespace from string values."""
    if isinstance(value, str):
        return value.strip()
    return value

def lambda_handler(event, context):
    """
    Kinesis Firehose Data Transformation Lambda.
    - Strips whitespace from all string fields
    - Masks IP addresses for privacy
    - Adds processing timestamp
    - Handles malformed records gracefully
    """
    output = []

    for record in event['records']:
        try:
            # Decode the incoming data
            payload = base64.b64decode(record['data']).decode('utf-8')
            json_data = json.loads(payload)

            # Clean: Strip whitespace from all string fields
            for key, value in json_data.items():
                json_data[key] = clean_string(value)

            # Mask IP address for privacy
            if 'user_ip' in json_data:
                json_data['user_ip'] = mask_ip(json_data['user_ip'])

            # Add processing timestamp
            json_data['processed_at'] = datetime.utcnow().isoformat() + 'Z'

            # Encode the transformed data
            transformed_data = json.dumps(json_data) + '\n'
            encoded_data = base64.b64encode(transformed_data.encode('utf-8')).decode('utf-8')

            output_record = {
                'recordId': record['recordId'],
                'result': 'Ok',
                'data': encoded_data
            }

        except Exception as e:
            # If transformation fails, mark as ProcessingFailed
            # Firehose will send these to the error bucket
            print(f"Error processing record: {str(e)}")
            output_record = {
                'recordId': record['recordId'],
                'result': 'ProcessingFailed',
                'data': record['data']
            }

        output.append(output_record)

    print(f"Processed {len(output)} records")
    return {'records': output}
EOF
```

**Your feedback:** Confirm file created.

---

### 4.1.2 - Create the deployment package (ZIP)

```bash
cd /tmp/lambda-code
zip -r lambda-firehose-transform.zip lambda_function.py
ls -la lambda-firehose-transform.zip
```

**Your feedback:** Confirm ZIP file created and show file size.

---

### 4.1.3 - Upload ZIP to S3

```bash
aws s3 cp /tmp/lambda-code/lambda-firehose-transform.zip \
    s3://${SCRIPTS_BUCKET}/lambda/lambda-firehose-transform.zip
```

**Your feedback:** Confirm upload successful.

---

## Step 4.2: Create the Lambda function

### 4.2.1 - Wait for IAM role propagation

IAM roles take a few seconds to propagate. Wait 10 seconds:

```bash
echo "Waiting 10 seconds for IAM role propagation..."
sleep 10
echo "Done waiting."
```

**Your feedback:** Confirm waited.

---

### 4.2.2 - Create the Lambda function

```bash
aws lambda create-function \
    --function-name project-insight-data-cleanse \
    --runtime python3.11 \
    --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/project-insight-lambda-role \
    --handler lambda_function.lambda_handler \
    --code S3Bucket=${SCRIPTS_BUCKET},S3Key=lambda/lambda-firehose-transform.zip \
    --timeout 60 \
    --memory-size 128 \
    --description "Data cleansing Lambda for Firehose transformation"
```

**Your feedback:** Confirm Lambda function created (you'll see JSON output with the function ARN).

---

### 4.2.3 - Test the Lambda function locally

Let's test with sample data:

```bash
cat > /tmp/test-event.json << 'EOF'
{
    "records": [
        {
            "recordId": "record-1",
            "data": "eyJldmVudF9pZCI6ImV2dF8xMjM0NSIsInVzZXJfaWQiOiJ1c3JfNjc4OTAiLCJ1c2VyX2lwIjoiMTkyLjE2OC4xLjEwMCIsInRpbWVzdGFtcCI6IjIwMjQtMDEtMTBUMTQ6MzA6MDBaIiwiZXZlbnRfdHlwZSI6InBhZ2VfdmlldyIsInBhZ2VfdXJsIjoiL3Byb2R1Y3RzL3Nob2VzIiwic2Vzc2lvbl9pZCI6InNlc3NfYWJjZGVmIn0="
        }
    ]
}
EOF

aws lambda invoke \
    --function-name project-insight-data-cleanse \
    --payload file:///tmp/test-event.json \
    --cli-binary-format raw-in-base64-out \
    /tmp/lambda-response.json

echo "Lambda response:"
cat /tmp/lambda-response.json | python3 -m json.tool
```

**Your feedback:** Paste the Lambda response. You should see `"result": "Ok"` in the output.

---

# PHASE 5: Create Kinesis Firehose Delivery Stream

## Step 5.1: Create the Firehose delivery stream

### 5.1.1 - Wait for Lambda to be ready

```bash
echo "Waiting 5 seconds for Lambda to be fully ready..."
sleep 5
echo "Done."
```

**Your feedback:** Confirm waited.

---

### 5.1.2 - Create the Firehose configuration file

```bash
cat > /tmp/firehose-config.json << EOF
{
    "DeliveryStreamName": "project-insight-clickstream",
    "DeliveryStreamType": "DirectPut",
    "ExtendedS3DestinationConfiguration": {
        "RoleARN": "arn:aws:iam::${AWS_ACCOUNT_ID}:role/project-insight-firehose-role",
        "BucketARN": "arn:aws:s3:::${RAW_BUCKET}",
        "Prefix": "clickstream/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/",
        "ErrorOutputPrefix": "errors/!{firehose:error-output-type}/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/",
        "BufferingHints": {
            "SizeInMBs": 5,
            "IntervalInSeconds": 60
        },
        "CompressionFormat": "GZIP",
        "ProcessingConfiguration": {
            "Enabled": true,
            "Processors": [
                {
                    "Type": "Lambda",
                    "Parameters": [
                        {
                            "ParameterName": "LambdaArn",
                            "ParameterValue": "arn:aws:lambda:${AWS_REGION}:${AWS_ACCOUNT_ID}:function:project-insight-data-cleanse"
                        }
                    ]
                }
            ]
        },
        "CloudWatchLoggingOptions": {
            "Enabled": true,
            "LogGroupName": "/aws/kinesisfirehose/project-insight-clickstream",
            "LogStreamName": "DestinationDelivery"
        }
    }
}
EOF
```

**Your feedback:** Confirm file created.

---

### 5.1.3 - Create the Firehose delivery stream

```bash
aws firehose create-delivery-stream \
    --cli-input-json file:///tmp/firehose-config.json
```

**Your feedback:** Confirm Firehose created (you'll see JSON with DeliveryStreamARN).

---

### 5.1.4 - Wait for Firehose to be active

```bash
echo "Waiting for Firehose to become ACTIVE..."
aws firehose describe-delivery-stream \
    --delivery-stream-name project-insight-clickstream \
    --query 'DeliveryStreamDescription.DeliveryStreamStatus' \
    --output text
```

Run this command until it shows `ACTIVE`. It may take 1-2 minutes.

**Your feedback:** Confirm Firehose is ACTIVE.

---

# PHASE 6: Test Data Ingestion

## Step 6.1: Send test data to Firehose

### 6.1.1 - Create a test event generator script

```bash
cat > /tmp/send-test-data.sh << 'EOF'
#!/bin/bash

# Generate and send test clickstream events to Firehose

STREAM_NAME="project-insight-clickstream"
EVENTS=("page_view" "add_to_cart" "purchase" "search" "click")
PAGES=("/home" "/products" "/cart" "/checkout" "/profile" "/search")

for i in {1..10}; do
    EVENT_TYPE=${EVENTS[$RANDOM % ${#EVENTS[@]}]}
    PAGE=${PAGES[$RANDOM % ${#PAGES[@]}]}
    USER_ID="usr_$(printf '%05d' $((RANDOM % 1000)))"
    SESSION_ID="sess_$(openssl rand -hex 4)"
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    IP="192.168.$((RANDOM % 255)).$((RANDOM % 255))"

    DATA=$(cat << ENDJSON
{"event_id":"evt_${i}_$(openssl rand -hex 4)","user_id":"${USER_ID}","user_ip":"${IP}","timestamp":"${TIMESTAMP}","event_type":"${EVENT_TYPE}","page_url":"${PAGE}","session_id":"${SESSION_ID}"}
ENDJSON
)

    echo "Sending event $i: $EVENT_TYPE on $PAGE"

    aws firehose put-record \
        --delivery-stream-name $STREAM_NAME \
        --record "Data=${DATA}" \
        --output text > /dev/null

    sleep 1
done

echo "Done! Sent 10 test events."
EOF

chmod +x /tmp/send-test-data.sh
```

**Your feedback:** Confirm script created.

---

### 6.1.2 - Run the test data generator

```bash
/tmp/send-test-data.sh
```

**Your feedback:** Confirm 10 events were sent.

---

### 6.1.3 - Wait for Firehose buffer to flush

Firehose buffers data for 60 seconds before writing to S3.

```bash
echo "Waiting 90 seconds for Firehose to flush buffer to S3..."
sleep 90
echo "Done waiting. Let's check S3."
```

**Your feedback:** Confirm you waited.

---

### 6.1.4 - Check if data landed in S3

```bash
aws s3 ls s3://${RAW_BUCKET}/clickstream/ --recursive
```

**Expected output:** You should see files with paths like:
```
clickstream/year=2024/month=01/day=10/project-insight-clickstream-1-2024-...
```

**Your feedback:** Paste the output showing files in S3.

---

### 6.1.5 - View the contents of a file

```bash
# Get the first file
FIRST_FILE=$(aws s3 ls s3://${RAW_BUCKET}/clickstream/ --recursive | head -1 | awk '{print $4}')
echo "First file: $FIRST_FILE"

# Download and decompress
aws s3 cp s3://${RAW_BUCKET}/${FIRST_FILE} /tmp/sample-data.gz
gunzip -c /tmp/sample-data.gz | head -5
```

**Your feedback:** Paste the output. You should see cleaned JSON with masked IPs.

---

# PHASE 7: Create Glue Data Catalog and Crawler

## Step 7.1: Create Glue Database

```bash
aws glue create-database \
    --database-input '{
        "Name": "project_insight_raw_db",
        "Description": "Database for raw clickstream data"
    }'
```

**Your feedback:** Confirm database created.

---

## Step 7.2: Create Glue Crawler

### 7.2.1 - Create the crawler

```bash
aws glue create-crawler \
    --name project-insight-raw-crawler \
    --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/project-insight-glue-role \
    --database-name project_insight_raw_db \
    --table-prefix "raw_" \
    --targets '{
        "S3Targets": [
            {
                "Path": "s3://'"${RAW_BUCKET}"'/clickstream/"
            }
        ]
    }' \
    --schema-change-policy '{
        "UpdateBehavior": "UPDATE_IN_DATABASE",
        "DeleteBehavior": "LOG"
    }' \
    --configuration '{
        "Version": 1.0,
        "Grouping": {
            "TableGroupingPolicy": "CombineCompatibleSchemas"
        }
    }'
```

**Your feedback:** Confirm crawler created.

---

### 7.2.2 - Run the crawler

```bash
aws glue start-crawler --name project-insight-raw-crawler
echo "Crawler started. This may take 1-2 minutes..."
```

**Your feedback:** Confirm crawler started.

---

### 7.2.3 - Check crawler status

Run this until status is `READY`:

```bash
aws glue get-crawler --name project-insight-raw-crawler \
    --query 'Crawler.State' --output text
```

**Your feedback:** Confirm crawler is READY.

---

### 7.2.4 - Verify table was created in Data Catalog

```bash
aws glue get-tables --database-name project_insight_raw_db \
    --query 'TableList[*].{Name:Name,Columns:StorageDescriptor.Columns[*].Name}' \
    --output table
```

**Your feedback:** Paste the output showing table name and columns.

---

# PHASE 8: Create Glue ETL Job (JSON to Parquet)

## Step 8.1: Create the ETL script

### 8.1.1 - Create the PySpark ETL script

```bash
cat > /tmp/glue-etl-script.py << 'EOF'
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql.functions import year, month, dayofmonth, col

# Get job parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME', 'RAW_DATABASE', 'RAW_TABLE', 'CURATED_BUCKET'])

# Initialize contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Read from Glue Data Catalog (enables job bookmarks)
print(f"Reading from database: {args['RAW_DATABASE']}, table: {args['RAW_TABLE']}")

datasource = glueContext.create_dynamic_frame.from_catalog(
    database=args['RAW_DATABASE'],
    table_name=args['RAW_TABLE'],
    transformation_ctx="datasource"
)

# Convert to DataFrame for easier manipulation
df = datasource.toDF()
print(f"Record count: {df.count()}")

# Skip if no data
if df.count() == 0:
    print("No new data to process. Exiting.")
    job.commit()
    sys.exit(0)

# Add partition columns from timestamp
df = df.withColumn("year", year(col("timestamp")))
df = df.withColumn("month", month(col("timestamp")))
df = df.withColumn("day", dayofmonth(col("timestamp")))

# Convert back to DynamicFrame
dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dynamic_frame")

# Write to S3 in Parquet format with partitioning
output_path = f"s3://{args['CURATED_BUCKET']}/clickstream/"
print(f"Writing to: {output_path}")

glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame,
    connection_type="s3",
    connection_options={
        "path": output_path,
        "partitionKeys": ["year", "month", "day"]
    },
    format="parquet",
    format_options={"compression": "snappy"},
    transformation_ctx="datasink"
)

print("ETL job completed successfully!")
job.commit()
EOF
```

**Your feedback:** Confirm script created.

---

### 8.1.2 - Upload ETL script to S3

```bash
aws s3 cp /tmp/glue-etl-script.py s3://${SCRIPTS_BUCKET}/glue/glue-etl-script.py
```

**Your feedback:** Confirm upload successful.

---

## Step 8.2: Create the Glue ETL Job

### 8.2.1 - Get the raw table name

```bash
RAW_TABLE=$(aws glue get-tables --database-name project_insight_raw_db \
    --query 'TableList[0].Name' --output text)
echo "Raw table name: $RAW_TABLE"
```

**Your feedback:** Confirm table name displayed.

---

### 8.2.2 - Create the Glue job

```bash
aws glue create-job \
    --name project-insight-json-to-parquet \
    --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/project-insight-glue-role \
    --command '{
        "Name": "glueetl",
        "ScriptLocation": "s3://'"${SCRIPTS_BUCKET}"'/glue/glue-etl-script.py",
        "PythonVersion": "3"
    }' \
    --default-arguments '{
        "--job-bookmark-option": "job-bookmark-enable",
        "--RAW_DATABASE": "project_insight_raw_db",
        "--RAW_TABLE": "'"${RAW_TABLE}"'",
        "--CURATED_BUCKET": "'"${CURATED_BUCKET}"'",
        "--enable-metrics": "true",
        "--enable-continuous-cloudwatch-log": "true"
    }' \
    --glue-version "4.0" \
    --number-of-workers 2 \
    --worker-type "G.1X" \
    --timeout 60 \
    --description "Convert raw JSON clickstream to Parquet"
```

**Your feedback:** Confirm Glue job created.

---

## Step 8.3: Run the Glue ETL Job

### 8.3.1 - Start the job

```bash
aws glue start-job-run --job-name project-insight-json-to-parquet
```

**Your feedback:** Confirm job started (you'll see a JobRunId).

---

### 8.3.2 - Monitor the job status

Run this until status is `SUCCEEDED`:

```bash
aws glue get-job-runs --job-name project-insight-json-to-parquet \
    --query 'JobRuns[0].{Status:JobRunState,Started:StartedOn,Duration:ExecutionTime}' \
    --output table
```

**Note:** The job may take 2-5 minutes to complete.

**Your feedback:** Paste status updates until SUCCEEDED.

---

### 8.3.3 - Check Parquet files in Curated bucket

```bash
aws s3 ls s3://${CURATED_BUCKET}/clickstream/ --recursive
```

**Your feedback:** Paste output showing Parquet files with partition structure.

---

# PHASE 9: Create Curated Database and Crawler

## Step 9.1: Create Curated Database

```bash
aws glue create-database \
    --database-input '{
        "Name": "project_insight_curated_db",
        "Description": "Database for curated Parquet clickstream data"
    }'
```

**Your feedback:** Confirm database created.

---

## Step 9.2: Create Curated Crawler

```bash
aws glue create-crawler \
    --name project-insight-curated-crawler \
    --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/project-insight-glue-role \
    --database-name project_insight_curated_db \
    --table-prefix "curated_" \
    --targets '{
        "S3Targets": [
            {
                "Path": "s3://'"${CURATED_BUCKET}"'/clickstream/"
            }
        ]
    }' \
    --schema-change-policy '{
        "UpdateBehavior": "UPDATE_IN_DATABASE",
        "DeleteBehavior": "LOG"
    }'
```

**Your feedback:** Confirm crawler created.

---

## Step 9.3: Run the Curated Crawler

```bash
aws glue start-crawler --name project-insight-curated-crawler
echo "Curated crawler started..."
```

Wait for it to complete:

```bash
aws glue get-crawler --name project-insight-curated-crawler \
    --query 'Crawler.State' --output text
```

**Your feedback:** Confirm crawler is READY.

---

## Step 9.4: Verify Curated Table

```bash
aws glue get-tables --database-name project_insight_curated_db \
    --query 'TableList[*].{Name:Name,Columns:StorageDescriptor.Columns[*].Name}' \
    --output table
```

**Your feedback:** Paste output showing curated table and columns.

---

# PHASE 10: Query with Athena

## Step 10.1: Configure Athena

### 10.1.1 - Create Athena workgroup

```bash
aws athena create-work-group \
    --name project-insight-workgroup \
    --configuration '{
        "ResultConfiguration": {
            "OutputLocation": "s3://'"${ATHENA_BUCKET}"'/results/"
        },
        "EnforceWorkGroupConfiguration": true,
        "PublishCloudWatchMetricsEnabled": true
    }' \
    --description "Workgroup for Project Insight queries"
```

**Your feedback:** Confirm workgroup created.

---

## Step 10.2: Run Athena Queries

### 10.2.1 - Query 1: Count all records

```bash
aws athena start-query-execution \
    --query-string "SELECT COUNT(*) as total_events FROM project_insight_curated_db.curated_clickstream" \
    --work-group project-insight-workgroup \
    --query-execution-context "Database=project_insight_curated_db"
```

Save the QueryExecutionId, then get results:

```bash
# Replace YOUR_QUERY_ID with the actual ID
QUERY_ID="YOUR_QUERY_ID"

# Wait a few seconds, then get results
sleep 5
aws athena get-query-results --query-execution-id $QUERY_ID
```

**Your feedback:** Paste the query result.

---

### 10.2.2 - Query 2: Count by event type

```bash
QUERY_ID=$(aws athena start-query-execution \
    --query-string "SELECT event_type, COUNT(*) as count FROM project_insight_curated_db.curated_clickstream GROUP BY event_type ORDER BY count DESC" \
    --work-group project-insight-workgroup \
    --query-execution-context "Database=project_insight_curated_db" \
    --query 'QueryExecutionId' --output text)

echo "Query ID: $QUERY_ID"
sleep 10

aws athena get-query-results --query-execution-id $QUERY_ID \
    --query 'ResultSet.Rows[*].Data[*].VarCharValue' --output table
```

**Your feedback:** Paste the query result showing event type counts.

---

### 10.2.3 - Query 3: Verify IP masking

```bash
QUERY_ID=$(aws athena start-query-execution \
    --query-string "SELECT user_ip FROM project_insight_curated_db.curated_clickstream LIMIT 5" \
    --work-group project-insight-workgroup \
    --query-execution-context "Database=project_insight_curated_db" \
    --query 'QueryExecutionId' --output text)

sleep 5

aws athena get-query-results --query-execution-id $QUERY_ID \
    --query 'ResultSet.Rows[*].Data[*].VarCharValue' --output table
```

**Your feedback:** Paste results. IPs should show `xxx.xxx` masking.

---

# PHASE 11: Create Step Functions Orchestration

## Step 11.1: Create SNS Topic for Alerts

```bash
aws sns create-topic --name project-insight-alerts
```

**Your feedback:** Confirm topic created (save the TopicArn).

---

## Step 11.2: Subscribe your email to the topic

```bash
# Replace with your email
YOUR_EMAIL="your-email@example.com"

SNS_TOPIC_ARN="arn:aws:sns:${AWS_REGION}:${AWS_ACCOUNT_ID}:project-insight-alerts"

aws sns subscribe \
    --topic-arn $SNS_TOPIC_ARN \
    --protocol email \
    --notification-endpoint $YOUR_EMAIL
```

**IMPORTANT:** Check your email and confirm the subscription!

**Your feedback:** Confirm you received and confirmed the subscription email.

---

## Step 11.3: Create Step Functions State Machine

### 11.3.1 - Create the state machine definition

```bash
cat > /tmp/stepfunctions-definition.json << EOF
{
    "Comment": "Project Insight Data Pipeline Orchestration",
    "StartAt": "StartRawCrawler",
    "States": {
        "StartRawCrawler": {
            "Type": "Task",
            "Resource": "arn:aws:states:::aws-sdk:glue:startCrawler",
            "Parameters": {
                "Name": "project-insight-raw-crawler"
            },
            "Next": "WaitForRawCrawler",
            "Catch": [
                {
                    "ErrorEquals": ["States.ALL"],
                    "Next": "SendFailureAlert"
                }
            ]
        },
        "WaitForRawCrawler": {
            "Type": "Wait",
            "Seconds": 30,
            "Next": "CheckRawCrawlerStatus"
        },
        "CheckRawCrawlerStatus": {
            "Type": "Task",
            "Resource": "arn:aws:states:::aws-sdk:glue:getCrawler",
            "Parameters": {
                "Name": "project-insight-raw-crawler"
            },
            "Next": "IsRawCrawlerReady"
        },
        "IsRawCrawlerReady": {
            "Type": "Choice",
            "Choices": [
                {
                    "Variable": "$.Crawler.State",
                    "StringEquals": "READY",
                    "Next": "StartETLJob"
                }
            ],
            "Default": "WaitForRawCrawler"
        },
        "StartETLJob": {
            "Type": "Task",
            "Resource": "arn:aws:states:::glue:startJobRun.sync",
            "Parameters": {
                "JobName": "project-insight-json-to-parquet"
            },
            "Next": "StartCuratedCrawler",
            "Catch": [
                {
                    "ErrorEquals": ["States.ALL"],
                    "Next": "SendFailureAlert"
                }
            ]
        },
        "StartCuratedCrawler": {
            "Type": "Task",
            "Resource": "arn:aws:states:::aws-sdk:glue:startCrawler",
            "Parameters": {
                "Name": "project-insight-curated-crawler"
            },
            "Next": "WaitForCuratedCrawler",
            "Catch": [
                {
                    "ErrorEquals": ["States.ALL"],
                    "Next": "SendFailureAlert"
                }
            ]
        },
        "WaitForCuratedCrawler": {
            "Type": "Wait",
            "Seconds": 30,
            "Next": "CheckCuratedCrawlerStatus"
        },
        "CheckCuratedCrawlerStatus": {
            "Type": "Task",
            "Resource": "arn:aws:states:::aws-sdk:glue:getCrawler",
            "Parameters": {
                "Name": "project-insight-curated-crawler"
            },
            "Next": "IsCuratedCrawlerReady"
        },
        "IsCuratedCrawlerReady": {
            "Type": "Choice",
            "Choices": [
                {
                    "Variable": "$.Crawler.State",
                    "StringEquals": "READY",
                    "Next": "PipelineSuccess"
                }
            ],
            "Default": "WaitForCuratedCrawler"
        },
        "PipelineSuccess": {
            "Type": "Succeed"
        },
        "SendFailureAlert": {
            "Type": "Task",
            "Resource": "arn:aws:states:::sns:publish",
            "Parameters": {
                "TopicArn": "arn:aws:sns:${AWS_REGION}:${AWS_ACCOUNT_ID}:project-insight-alerts",
                "Subject": "Project Insight Pipeline FAILED",
                "Message.$": "States.Format('Pipeline failed with error: {}', $.Error)"
            },
            "Next": "PipelineFailed"
        },
        "PipelineFailed": {
            "Type": "Fail",
            "Error": "PipelineError",
            "Cause": "The data pipeline encountered an error"
        }
    }
}
EOF
```

**Your feedback:** Confirm file created.

---

### 11.3.2 - Create the state machine

```bash
aws stepfunctions create-state-machine \
    --name project-insight-pipeline \
    --definition file:///tmp/stepfunctions-definition.json \
    --role-arn arn:aws:iam::${AWS_ACCOUNT_ID}:role/project-insight-stepfunctions-role \
    --type STANDARD
```

**Your feedback:** Confirm state machine created (save the stateMachineArn).

---

## Step 11.4: Test the Full Pipeline

### 11.4.1 - Send more test data

```bash
/tmp/send-test-data.sh
```

**Your feedback:** Confirm 10 more events sent.

---

### 11.4.2 - Wait for Firehose buffer

```bash
echo "Waiting 90 seconds for Firehose to flush..."
sleep 90
```

**Your feedback:** Confirm waited.

---

### 11.4.3 - Run the Step Functions pipeline

```bash
STATE_MACHINE_ARN="arn:aws:states:${AWS_REGION}:${AWS_ACCOUNT_ID}:stateMachine:project-insight-pipeline"

EXECUTION_ARN=$(aws stepfunctions start-execution \
    --state-machine-arn $STATE_MACHINE_ARN \
    --query 'executionArn' --output text)

echo "Execution started: $EXECUTION_ARN"
```

**Your feedback:** Confirm execution started.

---

### 11.4.4 - Monitor execution

Run this until status is `SUCCEEDED`:

```bash
aws stepfunctions describe-execution \
    --execution-arn $EXECUTION_ARN \
    --query '{Status:status,Started:startDate,Stopped:stopDate}' \
    --output table
```

**Your feedback:** Paste status until SUCCEEDED (may take 5-10 minutes).

---

### 11.4.5 - Verify new data in Athena

```bash
QUERY_ID=$(aws athena start-query-execution \
    --query-string "SELECT COUNT(*) as total FROM project_insight_curated_db.curated_clickstream" \
    --work-group project-insight-workgroup \
    --query-execution-context "Database=project_insight_curated_db" \
    --query 'QueryExecutionId' --output text)

sleep 5

aws athena get-query-results --query-execution-id $QUERY_ID
```

**Your feedback:** Confirm count increased from previous query.

---

# PHASE 12: Cleanup (Tear Down)

## Run this when you're done to avoid charges!

### 12.1 - Delete Step Functions

```bash
aws stepfunctions delete-state-machine \
    --state-machine-arn arn:aws:states:${AWS_REGION}:${AWS_ACCOUNT_ID}:stateMachine:project-insight-pipeline
```

### 12.2 - Delete SNS Topic

```bash
aws sns delete-topic \
    --topic-arn arn:aws:sns:${AWS_REGION}:${AWS_ACCOUNT_ID}:project-insight-alerts
```

### 12.3 - Delete Glue Jobs and Crawlers

```bash
aws glue delete-job --job-name project-insight-json-to-parquet
aws glue delete-crawler --name project-insight-raw-crawler
aws glue delete-crawler --name project-insight-curated-crawler
```

### 12.4 - Delete Glue Databases

```bash
aws glue delete-database --name project_insight_raw_db
aws glue delete-database --name project_insight_curated_db
```

### 12.5 - Delete Athena Workgroup

```bash
aws athena delete-work-group --work-group project-insight-workgroup --recursive-delete-option
```

### 12.6 - Delete Lambda Function

```bash
aws lambda delete-function --function-name project-insight-data-cleanse
```

### 12.7 - Delete Firehose

```bash
aws firehose delete-delivery-stream --delivery-stream-name project-insight-clickstream
```

### 12.8 - Empty and Delete S3 Buckets

```bash
for bucket in $RAW_BUCKET $CURATED_BUCKET $SCRIPTS_BUCKET $ATHENA_BUCKET; do
    echo "Emptying bucket: $bucket"
    aws s3 rm s3://$bucket --recursive
    echo "Deleting bucket: $bucket"
    aws s3api delete-bucket --bucket $bucket
done
```

### 12.9 - Delete IAM Roles

```bash
# Detach policies first
aws iam detach-role-policy --role-name project-insight-lambda-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam detach-role-policy --role-name project-insight-glue-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole

# Delete inline policies
aws iam delete-role-policy --role-name project-insight-firehose-role --policy-name firehose-s3-lambda-access
aws iam delete-role-policy --role-name project-insight-glue-role --policy-name glue-s3-access
aws iam delete-role-policy --role-name project-insight-stepfunctions-role --policy-name stepfunctions-glue-sns-access

# Delete roles
aws iam delete-role --role-name project-insight-lambda-role
aws iam delete-role --role-name project-insight-firehose-role
aws iam delete-role --role-name project-insight-glue-role
aws iam delete-role --role-name project-insight-stepfunctions-role
```

### 12.10 - Verify cleanup

```bash
echo "Checking for remaining resources..."
aws s3 ls | grep project-insight
aws iam list-roles --query "Roles[?contains(RoleName, 'project-insight')]" --output table
aws glue get-databases --query "DatabaseList[?contains(Name, 'project')]" --output table
```

**Your feedback:** Confirm all resources deleted.

---

# Summary

## What You Built

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   1. IAM Roles (4 roles with least-privilege policies)          │
│   2. S3 Buckets (4 buckets: raw, curated, scripts, athena)      │
│   3. Lambda Function (data cleansing with IP masking)           │
│   4. Kinesis Firehose (real-time ingestion with Lambda)         │
│   5. Glue Crawlers (2 crawlers: raw and curated)                │
│   6. Glue Data Catalog (2 databases with tables)                │
│   7. Glue ETL Job (JSON to Parquet with job bookmarks)          │
│   8. Step Functions (orchestration with error handling)         │
│   9. SNS Topic (failure alerts)                                 │
│   10. Athena (SQL queries on Parquet data)                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## DEA-C01 Exam Topics Covered

| Domain | Topics Practiced |
|--------|------------------|
| Domain 1: Ingestion | Kinesis Firehose, Lambda transforms, buffering |
| Domain 2: Storage | S3, Parquet, partitioning, compression |
| Domain 3: Operations | Glue, Step Functions, Job Bookmarks |
| Domain 4: Security | IAM roles, least privilege, data masking |

---

## Next Steps

1. **Rebuild** the entire pipeline from memory
2. **Add Lake Formation** for column-level security
3. **Test schema evolution** by adding new fields
4. **Create a Gold layer** with aggregated tables

---

**Congratulations! You've built a production-grade data lake on AWS!**
