# IoT Core Architecture and Setup
## Overview
The IoT Core implementation handles MQTT message ingestion from sensor devices, with secure certificate-based authentication and automated message routing to Lambda.
## Architecture Components
### MQTT Broker Setup
- Endpoint: [REGION].iot.[REGION].amazonaws.com
- Protocol: MQTT over TLS
- Port: 8883 (standard MQTT TLS)
### Message Topics
- Base Topic: livesense/poc/[DEVICE_ID]/airmetlab
- Format: Device IDs follow pattern ER[NUMBER]
- Example: livesense/poc/ER1024007/airmetlab
### Device Authentication
- X.509 certificate-based authentication
- Client certificates managed through AWS IoT Core
- No client ID restrictions implemented
### Message Routing
- IoT Rules process incoming MQTT messages
- SQL Query: SELECT * FROM 'livesense/poc/+/airmetlab'
- Direct Lambda integration for processing
## Data Flow
1. Device publishes to MQTT topic
2. IoT Core authenticates via certificate
3. IoT Rule captures message
4. Lambda function triggered
5. Data stored in DynamoDB
## Message Structure
{
    "cri": 1024007,
    "mt": 0,
    "sc": 26,
    "sv": [
        {"oc": 0, "sri": 1, "v": 1.802},
        {"oc": 0, "sri": 2, "v": 5.706}
    ],
    "ts": 1739538240
}
## Security Implementation
- TLS 1.2 required for all connections
- Certificate rotation policy: 365 days
- No shared certificates between devices
- Policy-based access control
## Monitoring
- CloudWatch Logs enabled
- Metrics tracked:
  - Connected devices
  - Messages processed
  - Rule invocations
## Performance Considerations
- Message size limit: 128KB
- QoS Level supported: 0,1
- Maximum concurrent connections: 500k
## Best Practices
- Implement exponential backoff for reconnection
- Use QoS 1 for critical messages
- Monitor certificate expiration
- Implement device shadow for state management
Created: February 2025
Author: Leonard Palad
Blog site: https://aws.leonardspalad.com/
LinkedIn: https://www.linkedin.com/in/leonardspalad/
