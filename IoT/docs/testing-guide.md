# Testing Guide

## MQTT Test Client Testing

### AWS IoT Core Test Client
1. Navigate to AWS IoT Core Console
2. Access "MQTT test client"
3. Configure test settings:
```bash
Topic: livesense/poc/ER1024007/ANZlab
QoS: 0
Sample Payload:
{
    "cri": "DEVICE_ID",
    "mt": 0,
    "sc": 26,
    "sv": [
        {"oc": 0, "sri": 1, "v": 2.5},
        {"oc": 0, "sri": 2, "v": 15.3}
    ],
    "ts": TIMESTAMP
}

MQTTX Application Testing
Connection Settings
yaml
Host: YOUR_IOT_ENDPOINT.iot.REGION.amazonaws.com
Port: 8883
Client ID: Any unique identifier
Protocol: MQTT v3.1.1
SSL/TLS: Enabled

Certificate Paths
Certificates Directory: YOUR_CERTIFICATES_PATH
├── ANZpoc-cert.pem
├── ANZpoc-private.key
└── AmazonRootCA1.pem

Python Simulator Script
Basic Test Script
import json
import time
import random
from awscrt import io, mqtt
from awsiot import mqtt_connection_builder

# Configuration
ENDPOINT = "YOUR_IOT_ENDPOINT"
CERT_PATH = "PATH_TO_CERTIFICATE"
PRI_KEY_PATH = "PATH_TO_PRIVATE_KEY"
CA_PATH = "PATH_TO_ROOT_CA"

# Device configurations
DEVICES = [
    {"id": "1024008", "topic": "livesense/poc/ER1024008/ANZlab"},
    {"id": "1024009", "topic": "livesense/poc/ER1024009/ANZlab"}
]

MESSAGE_INTERVAL = 15  # seconds


API Endpoint Testing
Using cURL
bash
curl https://YOUR_API_ENDPOINT/prod/readings


Using Web Browser
javascript
fetch('https://YOUR_API_ENDPOINT/prod/readings')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));


![image](https://github.com/user-attachments/assets/233fa1dc-9835-45d9-aa4a-bf2013430863)

