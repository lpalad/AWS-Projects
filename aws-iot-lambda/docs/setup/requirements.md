# Requirements Setup
## AWS Requirements
- AWS Account
- Region: ap-southeast-2 (Sydney)
## IAM Permissions
- IoT Core full access
- Lambda execution permissions
- DynamoDB full access
## Required Policies
### IoT Policy
- Allow MQTT connections
- Topic pattern: liveaide/poc/*/district
- Allow publish and subscribe
### Lambda Role
- Basic Lambda execution
- DynamoDB write permissions
## Software Requirements
- Python 3.9
- AWS CLI configured
## Table Requirements
DynamoDB table configuration:
- Table name: district_data
- Partition key: id (String)
- Billing mode: PAY_PER_REQUEST
## Message Requirements

Message format must follow:
{
    "cri": [NUMBER],
    "mt": 0,
    "sc": 26,
    "sv": [
        {"oc": 0, "sri": [NUMBER], "v": [VALUE]}
    ],
    "ts": [TIMESTAMP]
}
