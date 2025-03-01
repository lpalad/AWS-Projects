# Global Content Delivery with AWS CloudFront

## Overview
Implementation of global content delivery using AWS CloudFront with Nginx reverse proxy and S3 bucket origin. This lab demonstrates setting up a complete content delivery network with enhanced security and performance optimization.

## Implementation Phases
* PHASE 1: Infrastructure Verification
* PHASE 2: S3 Bucket Configuration
* PHASE 3: CloudFront Distribution Setup
* PHASE 4: DNS and SSL Configuration
* PHASE 5: Security Implementation
* PHASE 6: Testing and Validation

## EC2 Instance Verification
```bash
aws ec2 describe-instances --instance-ids [INSTANCE-ID]

Security Group Verification
bash
aws ec2 describe-security-groups --filters Name=vpc-id,Values=[VPC-ID]

VPC Verification
bash
aws ec2 describe-vpcs --vpc-ids [VPC-ID]

Subnet Verification
bash
aws ec2 describe-subnets --subnet-ids [SUBNET-ID]

Nginx Configuration
nginx
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
bash
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

Validation and Troubleshooting
bash
sudo nginx -t
sudo systemctl reload nginx

Log Monitoring
bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
CloudFront Testing
bash
curl -I https://[CLOUDFRONT-DOMAIN]

Expected Response Headers
x-cache: Hit from cloudfront
x-amz-cf-pop: [EDGE-LOCATION]
vary: Accept-Encoding

Cache Management
bash
aws cloudfront create-invalidation \
    --distribution-id [DISTRIBUTION-ID] \
    --paths "/*"

Security Notes
All sensitive information has been replaced with [PLACEHOLDERS]
Replace placeholders with your actual values
Follow AWS security best practices for production deployments

License
MIT

Author
Leonard S Palad

LinkedIn: https://www.linkedin.com/in/leonardspalad/
Blog: https://www.cloudhermit.com.au/

