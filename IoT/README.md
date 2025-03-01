# AWS IoT Core - Air Quality Monitoring System

## Overview

This GitHub repository provides a fully tested and sanitized lab setup for an automated air quality monitoring system using AWS IoT Core and serverless services. The system collects and processes real-time sensor data from multiple devices measuring various air quality parameters, including particulate matter (PM) and total suspended particles (TSP).

## Architecture

[Architecture Diagram - Coming Soon]

### AWS Services Used

- AWS IoT Core (MQTT Broker)
- AWS Lambda
- Amazon DynamoDB
- Amazon API Gateway

## Components

### 1. IoT Core Setup

- Topic Structure: `livesense/poc/*/airmetlab`
- No ClientID validation required
- Certificate-based authentication
- Policy Name: `airmetpoclab`

### 2. Data Structure

Sensor data format:

```json
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
```

#### Sensor Mapping

| Name                     | Relative ID |
|--------------------------|-------------|
| Flow (L/min)            | 1           |
| PM1 (µg/m3)             | 2           |
| PM1 15-Minute Average   | 3           |
| PM1 1-Hour Average      | 4           |

[Complete mapping table in implementation details]

## Step 3: Lambda Functions

### Air-Met PoC Lambda

Processes incoming IoT data:

```bash
aws lambda create-function \
    --function-name "ANZ-PoC" \
    --runtime python3.9 \
    --handler lambda_function.lambda_handler \
    --role <IAM_ROLE_ARN>
```

### API Gateway Setup

Creates a REST API:

```bash
aws apigateway create-rest-api \
    --name "ANZ-api" \
    --description "API for ANZ PoC mobile access"
```

## Testing

### MQTT Test Client
- Use **MQTTX** application for testing MQTT messages.

### API Endpoint Testing
- Use **Python Simulator Scripts** for API testing.

## Security Considerations

- **Certificate-based device authentication**
- **Public API endpoint considerations**
- **DynamoDB access controls**
- **AWS IAM roles and policies**

## Future Enhancements

- API authentication
- Enhanced data visualization
- Additional sensor support
- Historical data analysis

## Requirements

- **AWS Account**
- **AWS CLI configured**
- **Python 3.9+**
- Required Python packages:
  ```bash
  pip install awsiotsdk boto3
  ```

## Directory Structure

```
project/
├── scripts/
│   ├── python/
│   └── cli/
├── certificates/
└── docs/
```

## License

MIT License

## Author

[Leonard Palad](https://www.linkedin.com/in/leonardspalad/)  
[Blog](https://www.cloudhermit.com.au/)
