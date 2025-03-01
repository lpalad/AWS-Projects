AWS CloudFront with Nginx Reverse Proxy Setup

Overview
Implementation of global content delivery using AWS CloudFront with Nginx reverse proxy and S3 bucket origin. This lab demonstrates setting up a complete content delivery network with enhanced security and performance optimization.

Implementation Phases

PHASE 1: Infrastructure Verification
PHASE 2: S3 Bucket Configuration
PHASE 3: CloudFront Distribution Setup
PHASE 4: DNS and SSL Configuration
PHASE 5: Security Implementation
PHASE 6: Testing and Validation
EC2 Instance Verification
aws ec2 describe-instances --instance-id [INSTANCE-ID]

Security Group Verification
aws ec2 describe-security-groups --filters Name=vpc-id,Values=[VPC-ID]

VPC Verification
aws ec2 describe-vpcs --vpc-ids [VPC-ID]

Subnet Verification
aws ec2 describe-subnets --subnet-ids [SUBNET-ID]

Nginx Configuration
location = / {
proxy_pass http://[S3-BUCKET-ENDPOINT]/high-availability.html;
proxy_set_header Host [S3-BUCKET-ENDPOINT];
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_buffering off;
proxy_redirect off;
}

location / {
proxy_pass http://[S3-BUCKET-ENDPOINT]/;
proxy_set_header Host [S3-BUCKET-ENDPOINT];
proxy_set_header X-Real-IP $remote_addr;
proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
proxy_set_header X-Forwarded-Proto $scheme;
proxy_buffering off;
proxy_redirect off;
}

Monitoring Scripts
Page Testing Script
CLOUDFRONT_DOMAIN="[YOUR-DISTRIBUTION-DOMAIN]"
PAGES=(
"high-availability.html"
"aws-outages.html"
"disclaimer.html"
)

echo "Testing CloudFront Distribution..."
for page in "${PAGES[@]}"; do
echo -n "Testing $page: "
status=$(curl -s -o /dev/null -w "%{http_code}" https://$CLOUDFRONT_DOMAIN/$page)
if [ "$status" == "200" ]; then
echo "✅ OK ($status)"
else
echo "❌ Failed ($status)"
fi
done
