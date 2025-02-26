import json
import boto3
import uuid
import os

# Initialize SQS client
sqs = boto3.client('sqs')
QUEUE_URL = os.environ['QUEUE_URL']

def lambda_handler(event, context):
    """
    Lambda function that receives API Gateway requests and sends them to SQS.
    
    This function:
    1. Validates incoming requests
    2. Adds a unique message ID for tracing
    3. Sends the request to an SQS queue
    4. Returns a confirmation to the client
    
    Environment variables:
    - QUEUE_URL: The URL of the SQS queue
    """
    try:
        # Parse request body from API Gateway event
        if isinstance(event, dict) and 'body' in event:
            # Format from API Gateway
            request_body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
        else:
            # Direct invocation format
            request_body = event
        
        # Validate required fields
        if not request_body or 'order_id' not in request_body:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Missing required fields'})
            }
        
        # Add message ID for tracing
        request_body['message_id'] = str(uuid.uuid4())
        message = json.dumps(request_body)
        
        # Send message to SQS
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=message
        )
        
        # Return success response
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
