# Security Design

## Overview
This document outlines the security measures implemented across our multi-region AWS infrastructure, focusing on access control, data protection, and network security.

## Network Security
### Security Groups
#### Web Tier (Sydney)
- Inbound Rules:
  - HTTP (80) from ALB only
  - SSH (22) from bastion host
- Outbound Rules:
  - All traffic allowed

#### API Tier (Oregon)
- Inbound Rules:
  - Port 3000 from authorized IPs
  - SSH (22) from bastion host
- Outbound Rules:
  - MySQL (3306) to Aurora
  - HTTPS (443) for external services

### Network ACLs
- Stateless packet filtering
- Default deny all
- Explicit allow rules for required traffic

## Data Security
### Aurora Database
- Encryption at rest using AWS KMS
- Encryption in transit using SSL/TLS
- IAM authentication enabled
- Automated backups enabled

### API Authentication
- JWT-based token authentication
- Token payload includes:
  - Company identifier
  - Timestamp
  - Access scope
- No expiring tokens for service accounts

## Identity and Access Management
### IAM Roles
- EC2 instance roles
- RDS service roles
- Custom application roles

### Least Privilege Access
- Minimal required permissions
- Regular access review
- Resource-level permissions

## Monitoring and Logging
### CloudWatch
- API access logs
- Aurora database logs
- Instance metrics
- Custom alarms

### AWS CloudTrail
- API activity logging
- Resource change tracking
- Multi-region logging enabled

## Compliance Controls
- Data residency maintained
- Audit logging enabled
- Backup retention policies
- Access control documentation

Author  
Created: February 2025  
Author: Leonard Palad  
Blog site: https://aws.leonardspalad.com/  
LinkedIn: https://www.linkedin.com/in/leonardspalad/
