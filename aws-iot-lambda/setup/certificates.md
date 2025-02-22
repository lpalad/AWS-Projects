# 1. Moving certificates.md to /docs/setup/certificates.md


Content remains the same:
# IoT Device Certificates Setup


## Certificate Generation
Using AWS CLI to create device certificate:
aws iot create-keys-and-certificate \
    --set-as-active \
    --certificate-pem-outfile "district-cert.pem" \
    --public-key-outfile "district-public.key" \
    --private-key-outfile "district-private.key"

    
## Certificate Files
Three files will be generated:
- district-cert.pem (Certificate)
- district-private.key (Private Key)
- district-public.key (Public Key)

- 
## Policy Attachment
Attach IoT policy to certificate:
aws iot attach-policy \
    --policy-name "district" \
    --target "arn:aws:iot:ap-southeast-2:[ACCOUNT]:cert/[CERTIFICATE_ID]"

    
## Connection Details
MQTT Endpoint:
- Protocol: MQTT over TLS
- Port: 8883
- Endpoint Format: [ENDPOINT].iot.ap-southeast-2.amazonaws.com

- 
## Certificate Usage
Required for:
- Device authentication
- MQTT connections
- Message publishing
Certificate allows:
- Connection to IoT Core
- Publishing to topic: liveaide/poc/*/district
- No ClientID validation required

# 2. Create /docs/setup/policy-setup.md
# IoT Policy Setup
## Policy Creation
Creating IoT Core policy using AWS CLI:
aws iot create-policy \
    --policy-name "district" \
    --policy-document file://iam/iot-policy.json



    
## Policy Document
Located in iam/iot-policy.json:
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
                "arn:aws:iot:ap-southeast-2:[ACCOUNT]:client/*",
                "arn:aws:iot:ap-southeast-2:[ACCOUNT]:topic/liveaide/poc/*/district",
                "arn:aws:iot:ap-southeast-2:[ACCOUNT]:topicfilter/liveaide/poc/*/district"
            ]
        }
    ]
}






## Lambda Role
Located in iam/lambda-role.json:
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}




## Role Permissions
Required permissions for Lambda:
- Basic Lambda execution
- DynamoDB write access
