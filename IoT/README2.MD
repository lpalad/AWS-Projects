### AWS IoT Core - ANZ Air Quality Monitoring System

#### Overview
This project implements an automated air quality monitoring system using AWS IoT Core and serverless services. The system collects and processes real-time sensor data from multiple devices measuring various air quality parameters including particulate matter (PM) and total suspended particles (TSP).

#### Architecture
[Architecture Diagram - Coming Soon]

#### AWS Services Used
- **AWS IoT Core (MQTT Broker)**
- **AWS Lambda**
- **Amazon DynamoDB**
- **Amazon API Gateway**

---

### Components

#### 1. IoT Core Setup
- **Topic Structure**: `livesense/poc/*/ANZlab`
- **ClientID Validation**: Not required
- **Authentication**: Certificate-based
- **Policy Name**: `ANZpoclab`

#### 2. Data Structure
Sensor data format:
```json
{
    "cri": 60448,
    "mt": 0,
    "sc": 26,
    "sv": [
        {"oc": 0, "sri": 1, "v": 2.5},    // Flow Rate
        {"oc": 0, "sri": 2, "v": 15.3}     // PM1
    ],
    "ts": 1738022940000
}



Sensor Mapping
Name	RelativeID
Flow (L/min)	1
PM1 (µg/m3)	2
PM1 15-Minute Average	3
PM1 1-Hour Average	4
Complete mapping table in implementation details	

Lambda Functions
ANZ-PoC
Processes incoming IoT data
mobile-ANZ-poc
Serves API requests
