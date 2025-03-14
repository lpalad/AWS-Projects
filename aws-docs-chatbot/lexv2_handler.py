import json
import boto3

TABLE_NAME = "AWSDocumentation"
AWS_REGION = "us-east-1"

def lambda_handler(event, context):
    search_term = event.get('inputTranscript', "").strip()
    if not search_term:
        return format_response(event, "Which AWS service or topic do you need help with?")
    
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    
    matching_items = [item for item in response.get('Items', []) if search_term.lower() in item['content'].lower()]
    
    if matching_items:
        item = matching_items[0]
        message = f"Here's what I found about '{search_term}':\n\n{item['content'][:150]}...\n\nRead more at: {item['url']}"
        return format_response(event, message)
    else:
        return format_response(event, f"I couldn't find info about '{search_term}'. Try another query.")

def format_response(event, message):
    return {
        "sessionState": {"dialogAction": {"type": "Close"}},
        "messages": [{"contentType": "PlainText", "content": message}]
    }
