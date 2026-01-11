# Project Insight - CLI Commands Log

All CLI commands used in this lab for easy reference and rebuild.

**Region:** ap-southeast-2 (Sydney)
**Account ID:** YOUR_AWS_ACCOUNT_ID

---

## Progress Tracker

- [x] Phase 1: AWS Account & Security Setup
- [x] Phase 2: Environment Variables
- [x] Phase 3: Create S3 Buckets
- [x] Phase 4: Create IAM Roles
- [x] Phase 5: Create Lambda Function
- [x] Phase 6: Create Kinesis Firehose
- [x] Phase 7: Test Data Ingestion
- [x] Phase 8: Create Glue Resources (COMPLETED)
- [x] Phase 9: Create Glue ETL Job (COMPLETED)
- [x] Phase 10: Curated Database & Crawler (COMPLETED)
- [x] Phase 11: Athena Queries (COMPLETED)
- [x] Phase 12: Step Functions (COMPLETED)
- [x] Phase 12b: EventBridge Automation (COMPLETED)
- [ ] Phase 13: Cleanup

---

## Phase 1: AWS Account & Security Setup (COMPLETED)

### 1.1 Create IAM User

```bash
aws iam create-user --user-name data-engineer-admin
```

**Output:**
```json
{
    "User": {
        "Path": "/",
        "UserName": "data-engineer-admin",
        "UserId": "YOUR_USER_ID",
        "Arn": "arn:aws:iam::YOUR_AWS_ACCOUNT_ID:user/data-engineer-admin",
        "CreateDate": "2026-01-10T09:20:54+00:00"
    }
}
```

### 1.2 Attach Admin Policy

```bash
aws iam attach-user-policy \
    --user-name data-engineer-admin \
    --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

### 1.3 Create Access Keys

```bash
aws iam create-access-key --user-name data-engineer-admin
```

**Output:**
```json
{
    "AccessKey": {
        "UserName": "data-engineer-admin",
        "AccessKeyId": "YOUR_ACCESS_KEY_ID",
        "Status": "Active",
        "SecretAccessKey": "YOUR_SECRET_ACCESS_KEY",
        "CreateDate": "2026-01-10T09:22:08+00:00"
    }
}
```

### 1.4 Configure AWS CLI

```bash
aws configure
```

**Inputs:**
```
AWS Access Key ID: YOUR_ACCESS_KEY_ID
AWS Secret Access Key: YOUR_SECRET_ACCESS_KEY
Default region name: ap-southeast-2
Default output format: json
```

### 1.5 Test AWS CLI Connection

```bash
aws sts get-caller-identity
```

**Output:**
```json
{
    "UserId": "YOUR_USER_ID",
    "Account": "YOUR_AWS_ACCOUNT_ID",
    "Arn": "arn:aws:iam::YOUR_AWS_ACCOUNT_ID:user/data-engineer-admin"
}
```

---

## Phase 2: Environment Variables (COMPLETED)

**IMPORTANT:** Run this at the start of EVERY new terminal session!

### 2.1 Set Project Variables

```bash
export AWS_REGION="ap-southeast-2"
export PROJECT_NAME="project-insight"
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# S3 Bucket names
export RAW_BUCKET="${PROJECT_NAME}-raw-${AWS_ACCOUNT_ID}"
export CURATED_BUCKET="${PROJECT_NAME}-curated-${AWS_ACCOUNT_ID}"
export SCRIPTS_BUCKET="${PROJECT_NAME}-scripts-${AWS_ACCOUNT_ID}"
export ATHENA_BUCKET="${PROJECT_NAME}-athena-${AWS_ACCOUNT_ID}"

# Verify
echo "Region: $AWS_REGION"
echo "Account ID: $AWS_ACCOUNT_ID"
echo "Raw Bucket: $RAW_BUCKET"
echo "Curated Bucket: $CURATED_BUCKET"
echo "Scripts Bucket: $SCRIPTS_BUCKET"
echo "Athena Bucket: $ATHENA_BUCKET"
```

**Output:**
```
Region: ap-southeast-2
Account ID: YOUR_AWS_ACCOUNT_ID
Raw Bucket: project-insight-raw-YOUR_AWS_ACCOUNT_ID
Curated Bucket: project-insight-curated-YOUR_AWS_ACCOUNT_ID
Scripts Bucket: project-insight-scripts-YOUR_AWS_ACCOUNT_ID
Athena Bucket: project-insight-athena-YOUR_AWS_ACCOUNT_ID
```

---

## Phase 3: Create S3 Buckets (COMPLETED)

### 3.1 Create Raw Bucket (Bronze)

```bash
aws s3api create-bucket \
    --bucket $RAW_BUCKET \
    --region $AWS_REGION \
    --create-bucket-configuration LocationConstraint=$AWS_REGION
```

### 3.2 Create Curated Bucket (Silver)

```bash
aws s3api create-bucket \
    --bucket $CURATED_BUCKET \
    --region $AWS_REGION \
    --create-bucket-configuration LocationConstraint=$AWS_REGION
```

### 3.3 Create Scripts Bucket

```bash
aws s3api create-bucket \
    --bucket $SCRIPTS_BUCKET \
    --region $AWS_REGION \
    --create-bucket-configuration LocationConstraint=$AWS_REGION
```

### 3.4 Create Athena Results Bucket

```bash
aws s3api create-bucket \
    --bucket $ATHENA_BUCKET \
    --region $AWS_REGION \
    --create-bucket-configuration LocationConstraint=$AWS_REGION
```

### 3.5 Verify Buckets

```bash
aws s3 ls | grep project-insight
```

**Output:**
```
2026-01-10 20:29:10 project-insight-athena-YOUR_AWS_ACCOUNT_ID
2026-01-10 20:28:23 project-insight-curated-YOUR_AWS_ACCOUNT_ID
2026-01-10 20:27:21 project-insight-raw-YOUR_AWS_ACCOUNT_ID
2026-01-10 20:28:46 project-insight-scripts-YOUR_AWS_ACCOUNT_ID
```

### 3.6 Block Public Access

```bash
for bucket in $RAW_BUCKET $CURATED_BUCKET $SCRIPTS_BUCKET $ATHENA_BUCKET; do
    aws s3api put-public-access-block \
        --bucket $bucket \
        --public-access-block-configuration \
        "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
    echo "Blocked public access on: $bucket"
done
```

**Output:**
```
Blocked public access on: project-insight-raw-YOUR_AWS_ACCOUNT_ID
Blocked public access on: project-insight-curated-YOUR_AWS_ACCOUNT_ID
Blocked public access on: project-insight-scripts-YOUR_AWS_ACCOUNT_ID
Blocked public access on: project-insight-athena-YOUR_AWS_ACCOUNT_ID
```

---

## Phase 4: Create IAM Roles (IN PROGRESS)

### 4.1 Lambda Role (COMPLETED)

#### 4.1.1 Create Lambda Trust Policy
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

#### 4.1.2 Create Lambda Role
```bash
aws iam create-role \
    --role-name project-insight-lambda-role \
    --assume-role-policy-document file:///tmp/lambda-trust-policy.json \
    --description "Role for Project Insight Lambda functions"
```

**Output:**
```json
{
    "Role": {
        "Path": "/",
        "RoleName": "project-insight-lambda-role",
        "RoleId": "YOUR_LAMBDA_ROLE_ID",
        "Arn": "arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/project-insight-lambda-role",
        "CreateDate": "2026-01-10T09:34:00+00:00"
    }
}
```

#### 4.1.3 Attach Lambda Execution Policy
```bash
aws iam attach-role-policy \
    --role-name project-insight-lambda-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

### 4.2 Firehose Role (IN PROGRESS)

#### 4.2.1 Create Firehose Trust Policy
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

#### 4.2.2 Create Firehose Role
```bash
aws iam create-role \
    --role-name project-insight-firehose-role \
    --assume-role-policy-document file:///tmp/firehose-trust-policy.json \
    --description "Role for Project Insight Kinesis Firehose"
```

**Output:**
```json
{
    "Role": {
        "Path": "/",
        "RoleName": "project-insight-firehose-role",
        "RoleId": "YOUR_FIREHOSE_ROLE_ID",
        "Arn": "arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/project-insight-firehose-role",
        "CreateDate": "2026-01-10T09:36:20+00:00"
    }
}
```

#### 4.2.3 Create Firehose Permissions Policy
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

#### 4.2.4 Attach Firehose Permissions Policy
```bash
aws iam put-role-policy \
    --role-name project-insight-firehose-role \
    --policy-name firehose-s3-lambda-access \
    --policy-document file:///tmp/firehose-permissions-policy.json
```

### 4.3 Glue Role (COMPLETED)

#### 4.3.1 Create Glue Trust Policy
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

#### 4.3.2 Create Glue Role
```bash
aws iam create-role \
    --role-name project-insight-glue-role \
    --assume-role-policy-document file:///tmp/glue-trust-policy.json \
    --description "Role for Project Insight Glue Crawler and ETL"
```

**Output:**
```json
{
    "Role": {
        "Path": "/",
        "RoleName": "project-insight-glue-role",
        "RoleId": "YOUR_GLUE_ROLE_ID",
        "Arn": "arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/project-insight-glue-role",
        "CreateDate": "2026-01-10T09:42:04+00:00"
    }
}
```

#### 4.3.3 Attach AWS Managed Glue Policy
```bash
aws iam attach-role-policy \
    --role-name project-insight-glue-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole
```

#### 4.3.4 Create S3 Access Policy
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

#### 4.3.5 Attach S3 Policy to Glue Role
```bash
aws iam put-role-policy \
    --role-name project-insight-glue-role \
    --policy-name glue-s3-access \
    --policy-document file:///tmp/glue-s3-policy.json
```

### 4.4 Step Functions Role (COMPLETED)

#### 4.4.1 Create Step Functions Trust Policy
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

#### 4.4.2 Create Step Functions Role
```bash
aws iam create-role \
    --role-name project-insight-stepfunctions-role \
    --assume-role-policy-document file:///tmp/stepfunctions-trust-policy.json \
    --description "Role for Project Insight Step Functions"
```

**Output:**
```json
{
    "Role": {
        "Path": "/",
        "RoleName": "project-insight-stepfunctions-role",
        "RoleId": "YOUR_STEPFUNCTIONS_ROLE_ID",
        "Arn": "arn:aws:iam::YOUR_AWS_ACCOUNT_ID:role/project-insight-stepfunctions-role",
        "CreateDate": "2026-01-10T09:52:17+00:00"
    }
}
```

#### 4.4.3 Create Permissions Policy
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

#### 4.4.4 Attach Permissions Policy
```bash
aws iam put-role-policy \
    --role-name project-insight-stepfunctions-role \
    --policy-name stepfunctions-glue-sns-access \
    --policy-document file:///tmp/stepfunctions-policy.json
```

### 4.5 Verify All Roles

```bash
aws iam list-roles --query "Roles[?contains(RoleName, 'project-insight')].RoleName" --output table
```

**Output:**
```
----------------------------------------
|               ListRoles              |
+--------------------------------------+
|  project-insight-firehose-role       |
|  project-insight-glue-role           |
|  project-insight-lambda-role         |
|  project-insight-stepfunctions-role  |
+--------------------------------------+
```

---

## Phase 5: Create Lambda Function (COMPLETED)

### 5.1 Create Lambda Code

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
    output = []

    for record in event['records']:
        try:
            payload = base64.b64decode(record['data']).decode('utf-8')
            json_data = json.loads(payload)

            for key, value in json_data.items():
                json_data[key] = clean_string(value)

            if 'user_ip' in json_data:
                json_data['user_ip'] = mask_ip(json_data['user_ip'])

            json_data['processed_at'] = datetime.utcnow().isoformat() + 'Z'

            transformed_data = json.dumps(json_data) + '\n'
            encoded_data = base64.b64encode(transformed_data.encode('utf-8')).decode('utf-8')

            output_record = {
                'recordId': record['recordId'],
                'result': 'Ok',
                'data': encoded_data
            }

        except Exception as e:
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

### 5.2 Create ZIP and Upload

```bash
cd /tmp/lambda-code
zip -r lambda-firehose-transform.zip lambda_function.py

aws s3 cp /tmp/lambda-code/lambda-firehose-transform.zip \
    s3://${SCRIPTS_BUCKET}/lambda/lambda-firehose-transform.zip
```

### 5.3 Create Lambda Function

```bash
# Wait for IAM propagation
sleep 10

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

### 5.4 Test Lambda

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

cat /tmp/lambda-response.json | python3 -m json.tool
```

---

## Phase 6: Create Kinesis Firehose

### 6.1 Create Firehose Configuration

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

### 6.2 Create Firehose Delivery Stream

```bash
aws firehose create-delivery-stream \
    --cli-input-json file:///tmp/firehose-config.json
```

### 6.3 Check Firehose Status

```bash
aws firehose describe-delivery-stream \
    --delivery-stream-name project-insight-clickstream \
    --query 'DeliveryStreamDescription.DeliveryStreamStatus' \
    --output text
```

---

## Phase 7: Test Data Ingestion (COMPLETED)

### 7.1 Create Test Data Generator

```bash
cat > /tmp/send-test-data.sh << 'EOF'
#!/bin/bash

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

### 7.2 Send Test Data

```bash
/tmp/send-test-data.sh
```

### 7.3 Wait and Check S3

```bash
# Wait for Firehose buffer
sleep 90

# Check files
aws s3 ls s3://${RAW_BUCKET}/clickstream/ --recursive
```

### 7.4 View File Contents

```bash
FIRST_FILE=$(aws s3 ls s3://${RAW_BUCKET}/clickstream/ --recursive | head -1 | awk '{print $4}')
aws s3 cp s3://${RAW_BUCKET}/${FIRST_FILE} /tmp/sample-data.gz
gunzip -c /tmp/sample-data.gz | head -5
```

---

## Phase 8: Create Glue Resources

### 8.1 Create Raw Database

```bash
aws glue create-database \
    --database-input '{
        "Name": "project_insight_raw_db",
        "Description": "Database for raw clickstream data"
    }'
```

### 8.2 Create Raw Crawler

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
    }'
```

### 8.3 Run Raw Crawler

```bash
aws glue start-crawler --name project-insight-raw-crawler
```

### 8.4 Check Crawler Status

```bash
aws glue get-crawler --name project-insight-raw-crawler \
    --query 'Crawler.State' --output text
```

### 8.5 View Data Catalog Tables

```bash
aws glue get-tables --database-name project_insight_raw_db --output table
```

**What it shows**: Full metadata including table name, classification, compression, record count, partition keys

### 8.6 View Table Schema (Columns Only)

```bash
aws glue get-table --database-name project_insight_raw_db --name raw_clickstream \
    --query 'Table.StorageDescriptor.Columns[*].{Column:Name,Type:Type}' --output table
```

**Output:**
```
+---------------+----------+
|    Column     |  Type    |
+---------------+----------+
|  event_id     |  string  |
|  user_id      |  string  |
|  user_ip      |  string  |
|  timestamp    |  string  |
|  event_type   |  string  |
|  page_url     |  string  |
|  session_id   |  string  |
|  processed_at |  string  |
+---------------+----------+
```

**Key findings**:
- 8 columns auto-detected
- Partition keys: year, month, day
- Classification: JSON (GZIP compressed)
- 10 records found

---

## Phase 9: Create Glue ETL Job

### 9.1 Create ETL Script

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

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'RAW_DATABASE', 'RAW_TABLE', 'CURATED_BUCKET'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

print(f"Reading from database: {args['RAW_DATABASE']}, table: {args['RAW_TABLE']}")

datasource = glueContext.create_dynamic_frame.from_catalog(
    database=args['RAW_DATABASE'],
    table_name=args['RAW_TABLE'],
    transformation_ctx="datasource"
)

df = datasource.toDF()
print(f"Record count: {df.count()}")

if df.count() == 0:
    print("No new data to process. Exiting.")
    job.commit()
    sys.exit(0)

df = df.withColumn("year", year(col("timestamp")))
df = df.withColumn("month", month(col("timestamp")))
df = df.withColumn("day", dayofmonth(col("timestamp")))

dynamic_frame = DynamicFrame.fromDF(df, glueContext, "dynamic_frame")

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

aws s3 cp /tmp/glue-etl-script.py s3://${SCRIPTS_BUCKET}/glue/glue-etl-script.py
```

**What the ETL script does**:
- Reads JSON from Bronze bucket via Data Catalog
- Extracts year/month/day from timestamp for partitioning
- Converts to Parquet format with Snappy compression
- Writes to Silver bucket partitioned by date
- Job bookmarks track processed files (incremental processing)

### 9.2 Upload Script to S3

```bash
aws s3 cp /tmp/glue-etl-script.py s3://${SCRIPTS_BUCKET}/glue/glue-etl-script.py
```

**Verify upload**:
```bash
aws s3 ls s3://${SCRIPTS_BUCKET}/glue/
```

### 9.3 Get Raw Table Name

```bash
RAW_TABLE=$(aws glue get-tables --database-name project_insight_raw_db \
    --query 'TableList[0].Name' --output text)
echo "Raw table name: $RAW_TABLE"
```

**Expected output**: `raw_clickstream`

### 9.4 Create Glue Job

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
        "--enable-metrics": "true"
    }' \
    --glue-version "4.0" \
    --number-of-workers 2 \
    --worker-type "G.1X" \
    --timeout 60
```

**Key settings**:
- `job-bookmark-enable`: Only processes NEW files (incremental ETL)
- `G.1X`: Smallest worker type (cost optimization)
- `timeout 60`: Auto-kills job after 60 minutes
- `number-of-workers 2`: Minimum workers for Spark

### 9.5 Run ETL Job

```bash
aws glue start-job-run --job-name project-insight-json-to-parquet
```

**Note**: Takes 2-3 minutes (Spark startup time)

### 9.6 Check Job Status

```bash
aws glue get-job-runs --job-name project-insight-json-to-parquet \
    --query 'JobRuns[0].{Status:JobRunState,Duration:ExecutionTime}' --output table
```

**Possible states**: RUNNING, SUCCEEDED, FAILED

### 9.7 If Job Fails - Check Error

```bash
aws glue get-job-runs --job-name project-insight-json-to-parquet \
    --query 'JobRuns[0].ErrorMessage' --output text
```

### 9.8 Check Curated Bucket (Silver Layer)

```bash
aws s3 ls s3://${CURATED_BUCKET}/clickstream/ --recursive
```

**Expected output**: Parquet files partitioned by year/month/day
```
clickstream/year=2026/month=1/day=10/part-00001-xxxxx.snappy.parquet
clickstream/year=2026/month=1/day=10/part-00002-xxxxx.snappy.parquet
...
```

---

## Phase 10: Curated Database & Crawler

**Why this phase?** The Parquet files exist in S3, but Athena queries the Data Catalog, not S3 directly. The curated crawler scans the Parquet files and registers them as a table so Athena can query them.

### 10.1 Create Curated Database

```bash
aws glue create-database \
    --database-input '{
        "Name": "project_insight_curated_db",
        "Description": "Database for curated Parquet data (Silver layer)"
    }'
```

### 10.2 Create Curated Crawler

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
    }'
```

### 10.3 Run Curated Crawler

```bash
aws glue start-crawler --name project-insight-curated-crawler
```

### 10.4 Check Status

```bash
aws glue get-crawler --name project-insight-curated-crawler \
    --query 'Crawler.State' --output text
```

**Wait for**: `READY` (takes ~1 minute)

### 10.5 Verify Curated Table in Data Catalog

```bash
aws glue get-table --database-name project_insight_curated_db --name curated_clickstream \
    --query 'Table.StorageDescriptor.Columns[*].{Column:Name,Type:Type}' --output table
```

**Expected**: Same columns as raw + year/month/day partition columns, but stored as Parquet

---

## Phase 11: Athena Queries

### 11.1 Create Athena Workgroup

```bash
aws athena create-work-group \
    --name project-insight-workgroup \
    --configuration '{
        "ResultConfiguration": {
            "OutputLocation": "s3://'"${ATHENA_BUCKET}"'/results/"
        }
    }'
```

### 11.2 Query: Count All Records

```bash
QUERY_ID=$(aws athena start-query-execution \
    --query-string "SELECT COUNT(*) as total FROM project_insight_curated_db.curated_clickstream" \
    --work-group project-insight-workgroup \
    --query 'QueryExecutionId' --output text)

sleep 5

aws athena get-query-results --query-execution-id $QUERY_ID
```

### 11.3 Query: Count by Event Type

```bash
QUERY_ID=$(aws athena start-query-execution \
    --query-string "SELECT event_type, COUNT(*) as count FROM project_insight_curated_db.curated_clickstream GROUP BY event_type" \
    --work-group project-insight-workgroup \
    --query 'QueryExecutionId' --output text)

sleep 5

aws athena get-query-results --query-execution-id $QUERY_ID \
    --query 'ResultSet.Rows[*].Data[*].VarCharValue' --output table
```

---

## Phase 12: Step Functions

### 12.1 Create SNS Topic

```bash
aws sns create-topic --name project-insight-alerts
```

### 12.2 Subscribe Email

```bash
SNS_TOPIC_ARN="arn:aws:sns:${AWS_REGION}:${AWS_ACCOUNT_ID}:project-insight-alerts"

aws sns subscribe \
    --topic-arn $SNS_TOPIC_ARN \
    --protocol email \
    --notification-endpoint YOUR_EMAIL@example.com
```

### 12.3 Create State Machine Definition

```bash
cat > /tmp/stepfunctions-definition.json << EOF
{
    "Comment": "Project Insight Data Pipeline",
    "StartAt": "StartRawCrawler",
    "States": {
        "StartRawCrawler": {
            "Type": "Task",
            "Resource": "arn:aws:states:::aws-sdk:glue:startCrawler",
            "Parameters": {"Name": "project-insight-raw-crawler"},
            "Next": "WaitForRawCrawler",
            "Catch": [{"ErrorEquals": ["States.ALL"], "Next": "SendFailureAlert"}]
        },
        "WaitForRawCrawler": {
            "Type": "Wait",
            "Seconds": 30,
            "Next": "CheckRawCrawlerStatus"
        },
        "CheckRawCrawlerStatus": {
            "Type": "Task",
            "Resource": "arn:aws:states:::aws-sdk:glue:getCrawler",
            "Parameters": {"Name": "project-insight-raw-crawler"},
            "Next": "IsRawCrawlerReady"
        },
        "IsRawCrawlerReady": {
            "Type": "Choice",
            "Choices": [{"Variable": "$.Crawler.State", "StringEquals": "READY", "Next": "StartETLJob"}],
            "Default": "WaitForRawCrawler"
        },
        "StartETLJob": {
            "Type": "Task",
            "Resource": "arn:aws:states:::glue:startJobRun.sync",
            "Parameters": {"JobName": "project-insight-json-to-parquet"},
            "Next": "StartCuratedCrawler",
            "Catch": [{"ErrorEquals": ["States.ALL"], "Next": "SendFailureAlert"}]
        },
        "StartCuratedCrawler": {
            "Type": "Task",
            "Resource": "arn:aws:states:::aws-sdk:glue:startCrawler",
            "Parameters": {"Name": "project-insight-curated-crawler"},
            "Next": "WaitForCuratedCrawler",
            "Catch": [{"ErrorEquals": ["States.ALL"], "Next": "SendFailureAlert"}]
        },
        "WaitForCuratedCrawler": {
            "Type": "Wait",
            "Seconds": 30,
            "Next": "CheckCuratedCrawlerStatus"
        },
        "CheckCuratedCrawlerStatus": {
            "Type": "Task",
            "Resource": "arn:aws:states:::aws-sdk:glue:getCrawler",
            "Parameters": {"Name": "project-insight-curated-crawler"},
            "Next": "IsCuratedCrawlerReady"
        },
        "IsCuratedCrawlerReady": {
            "Type": "Choice",
            "Choices": [{"Variable": "$.Crawler.State", "StringEquals": "READY", "Next": "PipelineSuccess"}],
            "Default": "WaitForCuratedCrawler"
        },
        "PipelineSuccess": {"Type": "Succeed"},
        "SendFailureAlert": {
            "Type": "Task",
            "Resource": "arn:aws:states:::sns:publish",
            "Parameters": {
                "TopicArn": "arn:aws:sns:${AWS_REGION}:${AWS_ACCOUNT_ID}:project-insight-alerts",
                "Subject": "Pipeline FAILED",
                "Message.$": "States.Format('Error: {}', $.Error)"
            },
            "Next": "PipelineFailed"
        },
        "PipelineFailed": {"Type": "Fail"}
    }
}
EOF
```

### 12.4 Create State Machine

```bash
aws stepfunctions create-state-machine \
    --name project-insight-pipeline \
    --definition file:///tmp/stepfunctions-definition.json \
    --role-arn arn:aws:iam::${AWS_ACCOUNT_ID}:role/project-insight-stepfunctions-role \
    --type STANDARD
```

### 12.5 Run Pipeline

```bash
STATE_MACHINE_ARN="arn:aws:states:${AWS_REGION}:${AWS_ACCOUNT_ID}:stateMachine:project-insight-pipeline"

EXECUTION_ARN=$(aws stepfunctions start-execution \
    --state-machine-arn $STATE_MACHINE_ARN \
    --query 'executionArn' --output text)

echo "Execution: $EXECUTION_ARN"
```

### 12.6 Check Execution Status

```bash
aws stepfunctions describe-execution \
    --execution-arn $EXECUTION_ARN \
    --query '{Status:status}' --output table
```

---

## Phase 12b: EventBridge Automation (COMPLETED)

**Purpose**: Automatically trigger the pipeline when new files arrive in S3 (event-driven architecture)

### 12b.1 Enable S3 Event Notifications to EventBridge

```bash
aws s3api put-bucket-notification-configuration \
    --bucket $RAW_BUCKET \
    --notification-configuration '{
        "EventBridgeConfiguration": {}
    }'
```

### 12b.2 Create EventBridge Rule

```bash
aws events put-rule \
    --name "project-insight-s3-trigger" \
    --event-pattern '{
        "source": ["aws.s3"],
        "detail-type": ["Object Created"],
        "detail": {
            "bucket": {
                "name": ["'"$RAW_BUCKET"'"]
            },
            "object": {
                "key": [{"prefix": "clickstream/"}]
            }
        }
    }' \
    --description "Trigger data pipeline when new files arrive in raw bucket"
```

### 12b.3 Create EventBridge IAM Role

```bash
cat > /tmp/eventbridge-role-trust.json << 'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "events.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF

aws iam create-role \
    --role-name project-insight-eventbridge-role \
    --assume-role-policy-document file:///tmp/eventbridge-role-trust.json \
    --description "Role for EventBridge to invoke Step Functions"
```

### 12b.4 Add Step Functions Permission to EventBridge Role

```bash
cat > /tmp/eventbridge-sfn-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "states:StartExecution",
            "Resource": "arn:aws:states:${AWS_REGION}:${AWS_ACCOUNT_ID}:stateMachine:project-insight-pipeline"
        }
    ]
}
EOF

aws iam put-role-policy \
    --role-name project-insight-eventbridge-role \
    --policy-name invoke-stepfunctions \
    --policy-document file:///tmp/eventbridge-sfn-policy.json
```

### 12b.5 Add Target to EventBridge Rule

```bash
aws events put-targets \
    --rule "project-insight-s3-trigger" \
    --targets '[{
        "Id": "StepFunctionsTarget",
        "Arn": "arn:aws:states:'"$AWS_REGION"':'"$AWS_ACCOUNT_ID"':stateMachine:project-insight-pipeline",
        "RoleArn": "arn:aws:iam::'"$AWS_ACCOUNT_ID"':role/project-insight-eventbridge-role"
    }]'
```

### 12b.6 Test Automation

**Option 1: Send data through Firehose**
```bash
STREAM_NAME="project-insight-clickstream"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

DATA=$(echo -n "{\"event_id\":\"evt_auto_test\",\"user_id\":\"usr_test\",\"user_ip\":\"10.0.1.1\",\"timestamp\":\"${TIMESTAMP}\",\"event_type\":\"purchase\",\"page_url\":\"/test\",\"session_id\":\"sess_test\"}" | base64)

aws firehose put-record \
    --delivery-stream-name $STREAM_NAME \
    --record "{\"Data\":\"${DATA}\"}"
```

**Option 2: Upload JSON file directly to S3**
```bash
aws s3 cp test-clickstream.json \
    s3://${RAW_BUCKET}/clickstream/year=2026/month=01/day=11/test-clickstream.json
```

**Verify automation triggered:**
```bash
aws stepfunctions list-executions \
    --state-machine-arn "arn:aws:states:${AWS_REGION}:${AWS_ACCOUNT_ID}:stateMachine:project-insight-pipeline" \
    --max-results 3 \
    --query 'executions[*].{Name:name,Status:status,StartTime:startDate}' --output table
```

**How it works:**
1. File lands in S3 raw bucket under `clickstream/` prefix
2. S3 sends event to EventBridge
3. EventBridge matches the rule and triggers Step Functions
4. Pipeline runs automatically: Crawler → ETL → Curated Crawler
5. Data available in Athena within ~5-7 minutes

---

## Troubleshooting Notes

### ETL Job Fails with "SystemExit: 0"
**Cause**: Original ETL script used `sys.exit(0)` when no new data to process. Glue treats any `sys.exit()` as failure.
**Fix**: Updated script to just call `job.commit()` without `sys.exit()`.

### EventBridge Not Triggering Step Functions
**Cause**: Wrong IAM role. Step Functions role can't be used by EventBridge.
**Fix**: Create dedicated `project-insight-eventbridge-role` with `states:StartExecution` permission.

**Check if rule is triggering:**
```bash
aws cloudwatch get-metric-statistics \
    --namespace "AWS/Events" \
    --metric-name "TriggeredRules" \
    --dimensions Name=RuleName,Value=project-insight-s3-trigger \
    --start-time "$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ)" \
    --end-time "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    --period 300 \
    --statistics Sum
```

**Check for failed invocations:**
```bash
aws cloudwatch get-metric-statistics \
    --namespace "AWS/Events" \
    --metric-name "FailedInvocations" \
    --dimensions Name=RuleName,Value=project-insight-s3-trigger \
    --start-time "$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ)" \
    --end-time "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    --period 300 \
    --statistics Sum
```

### Pipeline Takes 5-7 Minutes
**This is normal.** Glue Crawlers and ETL jobs have cold start times:
- Crawler: ~2 min (spin up, scan, update catalog)
- ETL Job: ~2-3 min (Spark cluster startup)
- Curated Crawler: ~2 min

For faster processing, consider Lambda + Athena CTAS or Glue Streaming (always-on).

---

## Phase 13: Cleanup (Tear Down)

```bash
# Delete EventBridge Rule and Target
aws events remove-targets --rule project-insight-s3-trigger --ids StepFunctionsTarget
aws events delete-rule --name project-insight-s3-trigger

# Delete EventBridge Role
aws iam delete-role-policy --role-name project-insight-eventbridge-role --policy-name invoke-stepfunctions
aws iam delete-role --role-name project-insight-eventbridge-role

# Delete Step Functions
aws stepfunctions delete-state-machine \
    --state-machine-arn arn:aws:states:${AWS_REGION}:${AWS_ACCOUNT_ID}:stateMachine:project-insight-pipeline

# Delete SNS
aws sns delete-topic \
    --topic-arn arn:aws:sns:${AWS_REGION}:${AWS_ACCOUNT_ID}:project-insight-alerts

# Delete Glue
aws glue delete-job --job-name project-insight-json-to-parquet
aws glue delete-crawler --name project-insight-raw-crawler
aws glue delete-crawler --name project-insight-curated-crawler
aws glue delete-database --name project_insight_raw_db
aws glue delete-database --name project_insight_curated_db

# Delete Athena
aws athena delete-work-group --work-group project-insight-workgroup --recursive-delete-option

# Delete Lambda
aws lambda delete-function --function-name project-insight-data-cleanse

# Delete Firehose
aws firehose delete-delivery-stream --delivery-stream-name project-insight-clickstream

# Empty and Delete S3 Buckets
for bucket in $RAW_BUCKET $CURATED_BUCKET $SCRIPTS_BUCKET $ATHENA_BUCKET; do
    aws s3 rm s3://$bucket --recursive
    aws s3api delete-bucket --bucket $bucket
done

# Delete IAM Roles
aws iam detach-role-policy --role-name project-insight-lambda-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam detach-role-policy --role-name project-insight-glue-role --policy-arn arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole
aws iam delete-role-policy --role-name project-insight-firehose-role --policy-name firehose-s3-lambda-access
aws iam delete-role-policy --role-name project-insight-glue-role --policy-name glue-s3-access
aws iam delete-role-policy --role-name project-insight-stepfunctions-role --policy-name stepfunctions-glue-sns-access
aws iam delete-role --role-name project-insight-lambda-role
aws iam delete-role --role-name project-insight-firehose-role
aws iam delete-role --role-name project-insight-glue-role
aws iam delete-role --role-name project-insight-stepfunctions-role

# Delete IAM User (optional - if you want to remove the lab user)
aws iam delete-access-key --user-name data-engineer-admin --access-key-id YOUR_ACCESS_KEY_ID
aws iam detach-user-policy --user-name data-engineer-admin --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
aws iam delete-user --user-name data-engineer-admin
```

---

## Quick Reference: Environment Variables

Always set these at the start of a new terminal session:

```bash
export AWS_REGION="ap-southeast-2"
export PROJECT_NAME="project-insight"
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export RAW_BUCKET="${PROJECT_NAME}-raw-${AWS_ACCOUNT_ID}"
export CURATED_BUCKET="${PROJECT_NAME}-curated-${AWS_ACCOUNT_ID}"
export SCRIPTS_BUCKET="${PROJECT_NAME}-scripts-${AWS_ACCOUNT_ID}"
export ATHENA_BUCKET="${PROJECT_NAME}-athena-${AWS_ACCOUNT_ID}"
```
