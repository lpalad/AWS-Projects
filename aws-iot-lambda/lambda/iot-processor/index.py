# Lambda IoT Processor Function
## File: lambda/iot-processor/index.py
```python
import json
import boto3
from decimal import Decimal
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('district_data')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    try:
        # Convert the event to use Decimal instead of float
        json_str = json.dumps(event)
        data = json.loads(json_str, parse_float=Decimal)
        
        timestamp = str(datetime.utcnow().isoformat())
        
        item = {
            'id': timestamp,
            'deviceId': f"ER{event['cri']}",
            'timestamp': event['ts'],
            'raw_data': data
        }
        
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
