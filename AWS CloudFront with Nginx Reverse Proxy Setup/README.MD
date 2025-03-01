# AWS CloudFront with Nginx Reverse Proxy Lab

## Overview

This GitHub repository provides a fully tested and sanitized lab setup for deploying AWS CloudFront with an Nginx reverse proxy. The goal is to enable a high-availability, globally distributed content delivery network with enhanced security measures.


![Architecture Diagram](docs/architect.png)

## Implementation Phases

- **Phase 1:** Verify Current Setup
- **Phase 2:** Configure S3 Bucket
- **Phase 3:** Set Up CloudFront Distribution
- **Phase 4:** Configure DNS and SSL
- **Phase 5:** Implement Security (WAF, IAM)
- **Phase 6:** Testing and Validation

## Prerequisites

Before you start, ensure you have:

- An AWS account with necessary permissions
- An EC2 instance with Nginx installed
- An S3 bucket configured for static website hosting
- AWS CLI installed and configured

## Step 1: Verify EC2 Instance and Security Groups

Run the following commands to verify your infrastructure:

```bash
aws ec2 describe-instances --instance-ids <INSTANCE-ID>
aws ec2 describe-security-groups --filters Name=vpc-id,Values=<VPC-ID>
```

## Step 2: Configure Nginx as a Reverse Proxy

Update your Nginx configuration:

```nginx
server {
    listen 80;
    server_name <CLOUDFRONT_DOMAIN>;
    location / {
        proxy_pass http://<S3_BUCKET_WEBSITE_URL>/;
        proxy_set_header Host <S3_BUCKET_WEBSITE_URL>;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_buffering off;
        proxy_redirect off;
    }
}
```

Restart Nginx:

```bash
sudo nginx -t && sudo systemctl reload nginx
```

## Step 3: Create CloudFront Distribution

Run the following command to create a CloudFront distribution:

```bash
aws cloudfront create-distribution \
    --origin-domain-name <S3_BUCKET_WEBSITE_URL> \
    --default-root-object index.html
```

## Step 4: Configure DNS and SSL

Update your DNS records in Route 53:

```bash
aws route53 change-resource-record-sets --hosted-zone-id <ZONE_ID> \
    --change-batch file://dns-config.json
```

Enable SSL using ACM:

```bash
aws acm request-certificate --domain-name <CLOUDFRONT_DOMAIN> --validation-method DNS
```

## Step 5: Implement Security

Enable WAF Protection:

```bash
aws wafv2 create-web-acl --name CloudFront-Protection --scope CLOUDFRONT --region us-east-1
```

Attach WAF to CloudFront:

```bash
aws cloudfront update-distribution --id <DISTRIBUTION_ID> --web-acl-id <WEB_ACL_ARN>
```

## Step 6: Testing and Validation

Run a test script to verify availability:

```bash
#!/bin/bash
CLOUDFRONT_DOMAIN="<CLOUDFRONT_DOMAIN>"
PAGES=("index.html" "about.html" "contact.html")

for page in "${PAGES[@]}"; do
    curl -s -o /dev/null -w "%{http_code}" https://$CLOUDFRONT_DOMAIN/$page
    echo "Tested $page"
done
```

Monitor logs:

```bash
sudo tail -f /var/log/nginx/access.log /var/log/nginx/error.log
```

## Conclusion

This repository provides a step-by-step guide to setting up AWS CloudFront with an Nginx reverse proxy. Feel free to fork and modify it to suit your lab setup!

## License

MIT License

## Author

Leonard S Palad

LinkedIn: https://www.linkedin.com/in/leonardspalad/
Blog: https://www.cloudhermit.com.au/
