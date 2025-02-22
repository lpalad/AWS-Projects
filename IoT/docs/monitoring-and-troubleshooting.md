# Monitoring and Troubleshooting Guide

## CloudWatch Monitoring

### Lambda Function Monitoring
```bash
# Key Metrics to Monitor
- Invocations
- Errors
- Duration
- Throttles
- ConcurrentExecutions

# Log Groups
/aws/lambda/ANZ-PoC
/aws/lambda/mobile-ANZ-poc

### IoT Core Monitoring

#### Connection Metrics
- ConnectedDevices
- PublishIn.Success
- Subscribe.Success
- PublishOut.Success

#### MQTT Topics
- livesense/poc/+/ANZlab

---

### DynamoDB Monitoring

#### Table Metrics
- ConsumedReadCapacityUnits
- ConsumedWriteCapacityUnits
- ThrottledRequests
- SystemErrors

---

### Troubleshooting Flowcharts

#### Device Connection Issues

**Connection Failed**

- **Certificate Issues**
  - Check certificate exists and valid
  - Verify certificate attached to policy
  - Confirm certificate active

- **Policy Issues**
  - Verify policy permissions
  - Check resource ARNs
  - Validate topic patterns

- **Network Issues**
  - Verify endpoint URL
  - Check port 8883 accessible
  - Confirm TLS version

#### Data Flow Issues

**Data Not Reaching DynamoDB**

- **IoT Rule**
  - Rule enabled?
  - SQL query correct?
  - IAM role permissions?

- **Lambda Function**
  - Check CloudWatch logs
  - Verify error handling
  - Test function directly

- **DynamoDB**
  - Table exists?
  - Write capacity?
  - IAM permissions?

---

### Common Issues and Solutions

#### Device Connectivity (YAML)
```yaml
Issue: Device fails to connect
Solutions:
  - Verify endpoint: YOUR_IOT_ENDPOINT.iot.REGION.amazonaws.com
  - Check certificate paths
  - Confirm policy attachment
  - Test with MQTT test client


Lambda Function Errors (YAML)
Issue: Lambda execution failures
Solutions:
  - Check CloudWatch logs for specific errors
  - Verify DynamoDB table name
  - Confirm IAM role permissions
  - Test with sample event


API Gateway Issues (YAML)
Issue: API returns 5xx errors
Solutions:
  - Verify Lambda integration
  - Check CORS settings
  - Test Lambda directly
  - Review CloudWatch logs



Monitoring Dashboard
CloudWatch Dashboard Template (JSON)
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["AWS/IoT", "ConnectedDevices"]
        ],
        "period": 300,
        "stat": "Average",
        "region": "REGION",
        "title": "Connected Devices"
      }
    }
  ]
}



Alert Setup
Lambda Error Alert (Bash)
bash
Copy
aws cloudwatch put-metric-alarm \
    --alarm-name "ANZ-Lambda-Error-Alert" \
    --alarm-description "Alert on Lambda errors" \
    --metric-name Errors \
    --namespace AWS/Lambda \
    --statistic Sum \
    --period 300 \
    --threshold 1 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 1 \
    --alarm-actions "YOUR_SNS_TOPIC_ARN"


Health Check Script (Python)


import boto3
import json

def check_health():
    # Check IoT Core
    iot = boto3.client('iot')
    try:
        endpoint = iot.describe_endpoint()
        print("IoT Core Endpoint: Available")
    except Exception as e:
        print(f"IoT Core Issue: {str(e)}")

    # Check DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ANZpoclab_data')
    try:
        response = table.scan(Limit=1)
        print("DynamoDB: Accessible")
    except Exception as e:
        print(f"DynamoDB Issue: {str(e)}")

    # Additional health checks...


**Recovery Procedures**
Certificate Recovery
Generate new certificate
Update device configuration
Revoke old certificate
Verify connection


**Data Recovery**
Check DynamoDB backups
Verify data integrity
Restore if necessary
Validate recovered data


**Maintenance Tasks**
Regular Checks
Certificate expiration
Policy permissions
Lambda function logs
DynamoDB capacity
API Gateway metrics

**Monthly Tasks**
Review CloudWatch logs
Check error rates
Update monitoring thresholds
Verify backup integrity

