 
import boto3
import os
import time
from decimal import Decimal

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

class DecimalEncoder(json.JSONEncoder):
    """JSON encoder that handles Decimal types for DynamoDB values"""
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    """
    Lambda function triggered by SQS events to process messages.
    
    This function:
    1. Receives messages from SQS
    2. Processes each message (simulated with a delay)
    3. Converts numeric values to Decimal for DynamoDB compatibility
    4. Saves the processed data to DynamoDB
    
    Environment variables:
    - TABLE_NAME: The name of the DynamoDB table
    """
    processed_count = 0
    
    # Process each message from the SQS batch
    for record in event['Records']:
        # Extract message data
        message_body = json.loads(record['body'])
        message_id = message_body.get('message_id', 'unknown')
        order_id = message_body.get('order_id', 'unknown')
        
        try:
            # Add processing timestamp
            message_body['processed_at'] = int(time.time())
            
            # Convert numeric values to Decimal for DynamoDB compatibility
            for key, value in message_body.items():
                if isinstance(value, (int, float)):
                    message_body[key] = Decimal(str(value))
            
            # Write to DynamoDB
            table.put_item(Item=message_body)
            
            processed_count += 1
            
        except Exception as e:
            print(f"Error processing message {message_id}: {str(e)}")
            # In a production environment, implement appropriate error handling
            # such as sending to a Dead Letter Queue
            raise
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': f'Successfully processed {processed_count} messages'
        })
    }

