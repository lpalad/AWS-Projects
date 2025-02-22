# Oregon Region Setup (Secondary)

## Overview
This document provides step-by-step instructions for setting up the secondary infrastructure in the Oregon (us-west-2) region, including the API service and Aurora read replica.

## VPC Setup
### Create VPC
- Region: us-west-2
- CIDR: 10.1.0.0/16
- Enable DNS hostnames
- Enable DNS resolution

### Create Subnets
#### Public Subnets
- AZ-a: 10.1.3.0/24
- AZ-b: 10.1.4.0/24
- Auto-assign public IPv4: Yes

### Internet Gateway
- Create and attach to VPC
- Update route tables

### Route Tables
- Create public route table
- Add routes:
  - 0.0.0.0/0 → Internet Gateway
  - 10.1.0.0/16 → Local
- Associate with public subnets

## Security Configuration
### Security Groups
#### API Server Security Group
- Inbound:
  - Port 3000 from 159.196.168.92/32
  - Port 3306 for Aurora access
  - Port 22 for SSH access
- Outbound:
  - All traffic

#### Aurora Security Group
- Inbound:
  - Port 3306 from API Security Group
- Outbound:
  - All traffic

## API Server Setup
### EC2 Instance Configuration
- Instance type: t3.micro
- AMI: Amazon Linux 2
- Subnet: Public subnet (AZ-a)
- Security group: API Server Security Group
- Public IP: Enabled

### Software Installation
- Update system commands:
  - sudo yum update -y
  - sudo yum install -y nodejs npm mysql
  - curl -sL https://rpm.nodesource.com/setup_18.x | sudo bash -
  - sudo yum install -y nodejs
  - sudo npm install -g pm2

### API Application Setup
- Create application directory:
  - mkdir registration-api
  - cd registration-api
  - npm init -y
  - npm install express mysql2 dotenv jsonwebtoken

### Environment Configuration
- Create .env file:
  - DB_HOST=secondary-cluster-demo.cluster-ro-xxx.us-west-2.rds.amazonaws.com
  - DB_USER=admin
  - DB_PASSWORD=[Secure password]
  - DB_NAME=registration
  - PORT=3000

### API Implementation
- Create index.js with:
  - Express server setup
  - Database connection
  - JWT authentication
  - Company-specific data filtering
  - Error handling
  - Security headers

## Aurora Secondary Setup
### Subnet Group
- Create db subnet group
- Add all public subnets

### Aurora Read Replica
- Create from Global Database
- Instance class: db.r5.large
- Multi-AZ: No
- Subnet group: Created above
- Security group: Aurora Security Group

## Monitoring Setup
### CloudWatch
- Enable detailed monitoring
- Create log groups:
  - API application logs
  - Aurora logs
- Set up alarms:
  - API health
  - Database connectivity
  - Error rates

### Performance Monitoring
- Enable Enhanced Monitoring
- Setup Performance Insights
- Configure audit logging

## Verification Steps
1. Check VPC and subnet configuration
2. Verify security group rules
3. Test API server connectivity
4. Validate Aurora read replica
5. Test API endpoints:
   - Authentication
   - Data retrieval
   - Error handling
6. Monitor replication lag

## Failover Testing
### Read Replica Promotion
- Test manual promotion
- Verify automatic failover
- Check application handling
- Validate data consistency

### Application Response
- Monitor error handling
- Check retry logic
- Verify logging
- Test alert systems

Author  
Created: February 2025  
Author: Leonard Palad  
Blog site: https://aws.leonardspalad.com/  
LinkedIn: https://www.linkedin.com/in/leonardspalad/
