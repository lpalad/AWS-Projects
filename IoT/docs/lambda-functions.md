# Lambda Functions Documentation

## 1. ANZ-PoC Lambda Function
Main function for processing IoT data and storing in DynamoDB.

### Function Code
```python
import json
import boto3
from decimal import Decimal
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ANZpoclab_data')

def lambda_handler(event, context):
    try:
        # Convert the event to use Decimal instead of float
        json_str = json.dumps(event)
        data = json.loads(json_str, parse_float=Decimal)
        
        timestamp = str(datetime.utcnow().isoformat())
        
        # Process sensor values
        item = {
            'id': timestamp,
            'deviceId': f"ER{event['cri']}",
            'timestamp': event['ts']
        }
        
        # Map RelativeID to field names
        field_map = {
            1: 'flow_rate',
            2: 'pm1',
            3: 'pm1_15min_avg',
            4: 'pm1_1hour_avg',
            5: 'pm1_8hour_avg',
            6: 'pm1_24hour_avg',
            7: 'pm2_5',
            8: 'pm2_5_15min_avg',
            9: 'pm2_5_1hour_avg',
            10: 'pm2_5_8hour_avg',
            11: 'pm2_5_24hour_avg',
            12: 'pm4_25',
            13: 'pm4_25_15min_avg',
            14: 'pm4_25_1hour_avg',
            15: 'pm4_25_8hour_avg',
            16: 'pm4_25_24hour_avg',
            17: 'pm10',
            18: 'pm10_15min_avg',
            19: 'pm10_1hour_avg',
            20: 'pm10_8hour_avg',
            21: 'pm10_24hour_avg',
            22: 'tsp',
            23: 'tsp_15min_avg',
            24: 'tsp_1hour_avg',
            25: 'tsp_8hour_avg',
            26: 'tsp_24hour_avg'
        }
        
        # Process sensor values
        for sensor in event['sv']:
            field_name = field_map.get(sensor['sri'])
            if field_name:
                item[field_name] = Decimal(str(sensor['v']))
        
        response = table.put_item(Item=item)
        return {
            'statusCode': 200,
            'body': json.dumps('Data stored successfully')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }



**Deployment Commands**
# Create zip package
zip ANZ-PoC.zip ANZ-PoC.py

# Create Lambda function
aws lambda create-function \
    --function-name "ANZ-PoC" \
    --runtime python3.9 \
    --handler ANZ-PoC.lambda_handler \
    --role arn:aws:iam::XXXXXXXXXXX:role/ANZpoclab-lambda-role \
    --zip-file fileb://ANZ-PoC.zip



**mobile-ANZ-poc Lambda Function**
**Function Code**

import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ANZpoclab_data')

def lambda_handler(event, context):
    try:
        # Get latest readings
        response = table.scan(
            Limit=10  # Adjust number of records
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',  # For CORS
                'Content-Type': 'application/json'
            },
            'body': json.dumps(response['Items'], default=str)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }



Deployment Commands
# Create zip package
zip mobile-ANZ-poc.zip mobile-ANZ-poc.py

# Create Lambda function
aws lambda create-function \
    --function-name "mobile-ANZ-poc" \
    --runtime python3.9 \
    --handler mobile-ANZ-poc.lambda_handler \
    --role arn:aws:iam::XXXXXXXXXXXX:role/ANZpoclab-lambda-role \
    --zip-file fileb://mobile-ANZ-poc.zip


IAM Role Setup
Both Lambda functions use the same IAM role with permissions for:

CloudWatch Logs
DynamoDB access
IoT Core integration


Role Creation Commands
# Create role and attach policies [Details in IAM documentation]
aws iam create-role \
    --role-name ANZpoclab-lambda-role \
    --assume-role-policy-document file://trust-policy.json




