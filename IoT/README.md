# AWS IoT Core - Air Quality Monitoring System

## Overview
This project implements an automated air quality monitoring system using AWS IoT Core and serverless services. The system collects and processes real-time sensor data from multiple devices measuring various air quality parameters including particulate matter (PM) and total suspended particles (TSP).

## Architecture
[Architecture Diagram - Coming Soon]

### AWS Services Used
- AWS IoT Core (MQTT Broker)
- AWS Lambda
- Amazon DynamoDB
- Amazon API Gateway

## Components

### 1. IoT Core Setup
- Topic Structure: 'livesense/poc/*/airmetlab'
- No ClientID validation required
- Certificate-based authentication
- Policy Name: airmetpoclab

### 2. Data Structure
Sensor data format:

{
    "devid": 987562,
    "mt": 0,
    "sc": 26,
    "sv": [
        {"oc": 0, "sri": 1, "v": 2.5},    // Flow Rate
        {"oc": 0, "sri": 2, "v": 15.3}    // PM1
    ],
    "ts": 1740189740
}


Sensor Mapping
Name	RelativeID
Flow (L/min)	1
PM1 (µg/m3)	2
PM1 15-Minute Average	3
PM1 1-Hour Average	4
[Complete mapping table in implementation details]

**4. Lambda Functions**
Air-met-PoC: Processes incoming IoT data
mobile-airmet-poc: Serves API requests
5. API Gateway
Endpoint for web/mobile access
Supports CORS
Public GET endpoint
Implementation Steps
IoT Core Setup
bash

# Create IoT Policy
aws iot create-policy \
--policy-name "airmetpoclab" \
--policy-document file://airmetpoclab-policy.json


Lambda Setup

# Create Lambda function
aws lambda create-function \
--function-name "ANZ-PoC" \
--runtime python3.9 \
    [Additional parameters in implementation details]


**API Gateway Setup**

# Create REST API

aws apigateway create-rest-api \
--name "ANZ-api" \
--description "API for ANZ PoC mobile access"



Testing
MQTT Test Client
MQTTX Application
API Endpoint Testing
Python Simulator Scripts



Security Considerations
Certificate-based device authentication
Public API endpoint considerations
DynamoDB access controls
AWS IAM roles and policies




Future Enhancements
API authentication
Enhanced data visualization
Additional sensor support
Historical data analysis




Requirements
AWS Account
AWS CLI configured
Python 3.9+
Required Python packages:
awsiotsdk
boto3





Directory Structure

project/
├── scripts/
│   ├── python/
│   └── cli/
├── certificates/
└── docs/




Author
Leonard Palad

Blog: https://www.cloudhermit.com.au/
LinkedIn: https://www.linkedin.com/in/leonardspalad/


License
This project is licensed under the MIT License - see the LICENSE file for details
