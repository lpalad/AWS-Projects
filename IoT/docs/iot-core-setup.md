# IoT Core Setup Guide

## Policy Creation
The ANZ IoT policy allows devices to connect and publish data without ClientID validation.

### Policy Document
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iot:Connect",
                "iot:Publish",
                "iot:Subscribe",
                "iot:Receive"
            ],
            "Resource": [
                "arn:aws:iot:ap-southeast-2:881490097605:client/*",
                "arn:aws:iot:ap-southeast-2:881490097605:topic/bestsense/poc/*/ANZlab",
                "arn:aws:iot:ap-southeast-2:881490097605:topicfilter/bestsense/poc/*/ANZlab"
            ]
        }
    ]
}


### CLI Commands
 
# Create policy
aws iot create-policy \
    --policy-name "ANZpoclab" \
    --policy-document file://ANZpoclab-policy.json

# Create certificates
aws iot create-keys-and-certificate \
    --set-as-active \
    --certificate-pem-outfile "ANZpoc-cert.pem" \
    --public-key-outfile "ANZpoc-public.key" \
    --private-key-outfile "ANZpoc-private.key"

# Attach policy to certificate
aws iot attach-policy \
    --policy-name "ANZpoclab" \
    --target "CERTIFICATE_ARN"


Topic Structure
Base Topic: bestense/poc/*/ANZlab
Supports multiple device IDs
Example: best/poc/ER1024007/ANZlab
