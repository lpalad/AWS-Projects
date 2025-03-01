# AWS CloudFront with Nginx Reverse Proxy Setup

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
