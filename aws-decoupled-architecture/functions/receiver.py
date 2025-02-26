import json
import boto3
import uuid
import os

# Initialize SQS client
sqs = boto3.client('sqs')
QUEUE_URL = os.environ['QUEUE_URL']

def lambda_handler(event, context):
    try:
        # Parse request body
        if isinstance(event, dict) and 'body' in event:
            # This is coming from API Gateway
            if isinstance(event['body'], str):
                request_body = json.loads(event['body'])
            else:
                request_body = event['body']
        else:
            # Direct invocation
            request_body = event
        
        # Validate request
        if not request_body or not 'order_id' in request_body:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Missing required fields'})
            }
        
        # Add message ID for tracing
        request_body['message_id'] = str(uuid.uuid4())
        message = json.dumps(request_body)
        
        # Send message to SQS
        response = sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=message
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Request accepted for processing',
                'messageId': request_body['message_id'],
                'orderId': request_body['order_id']
            })
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'})
        }
