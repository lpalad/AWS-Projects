# Decoupled Architecture with AWS Lambda and SQS

This repository demonstrates a serverless, decoupled architecture pattern using AWS services to build a resilient, scalable application.

## Architecture Overview


![AWS-Decoupling-Services](https://github.com/user-attachments/assets/ca9c61c3-4b9d-4b30-b0bb-03c8ea90d962)

This architecture showcases:
- Frontend/backend decoupling with event-driven design
- Asynchronous processing with message queuing
- Reliable request handling during traffic spikes or backend issues
- Serverless implementation for automatic scaling

## Components

- **Amazon API Gateway**: Receives HTTP requests from clients
- **AWS Lambda (Receiver)**: Validates requests and sends them to SQS
- **Amazon SQS**: Buffers messages, ensuring no data loss during traffic spikes
- **AWS Lambda (Processor)**: Processes messages from the queue at a controlled rate
- **Amazon DynamoDB**: Stores processed data persistently

## Business Use Cases

This pattern is widely used in:
- E-commerce order processing
- Financial transaction handling
- User registration/onboarding workflows
- IoT data ingestion and processing
- Notification delivery systems
- Any scenario requiring reliable handling of unpredictable workloads

## Implementation Files

- `/functions/receiver.py` - Lambda function for validating and enqueuing requests
- `/functions/processor.py` - Lambda function for processing queued messages
- `/scripts/test-orders.sh` - Script for testing the architecture with sample orders
- `/templates/decoupled-architecture.yaml` - CloudFormation template for deploying the solution

## How It Works

1. Clients send HTTP requests to the API Gateway endpoint
2. The Receiver Lambda validates and sends the request to SQS
3. SQS queues the message until the Processor Lambda can handle it
4. The Processor Lambda processes messages from the queue and stores data in DynamoDB
5. Even during massive traffic spikes or backend slowdowns, no data is lost

## License
This project is licensed under the MIT License - see the LICENSE file for details.

Author
Leonard S Palad

LinkedIn: https://www.linkedin.com/in/leonardspalad/
Blog: https://www.cloudhermit.com.au/
