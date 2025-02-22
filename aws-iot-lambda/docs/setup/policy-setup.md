Policy Setup
AWS IoT Core policy setup for device authentication and permissions.

Policy Creation
Create IoT Core policy using AWS CLI: aws iot create-policy --policy-name "district" --policy-document file://iam/iot-policy.json

Policy Document
Located in iam/iot-policy.json: { "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Action": [ "iot:Connect", "iot:Publish", "iot:Subscribe", "iot:Receive" ], "Resource": [ "arn:aws:iot:ap-southeast-2:[ACCOUNT]:client/", "arn:aws:iot:ap-southeast-2:[ACCOUNT]:topic/liveaide/poc//district", "arn:aws:iot:ap-southeast-2:[ACCOUNT]:topicfilter/liveaide/poc/*/district" ] } ] }

Lambda Role
Located in iam/lambda-role.json: { "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Principal": { "Service": "lambda.amazonaws.com" }, "Action": "sts:AssumeRole" } ] }

Policy Attachment
Attach policy to certificate: aws iot attach-policy --policy-name "district" --target "arn:aws:iot:ap-southeast-2:[ACCOUNT]:cert/[CERTIFICATE_ID]"
