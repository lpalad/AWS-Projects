# Sydney Region Setup (Primary)

## Overview
This document provides step-by-step instructions for setting up the primary infrastructure in the Sydney (ap-southeast-2) region.

## VPC Setup
### Create VPC
- Region: ap-southeast-2
- CIDR: 10.1.0.0/16
- Enable DNS hostnames
- Enable DNS resolution

### Create Subnets
#### Public Subnets
- AZ-a: 10.1.1.0/24
- AZ-b: 10.1.2.0/24
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
#### ALB Security Group
- Inbound:
  - Port 80 from 0.0.0.0/0
- Outbound:
  - All traffic

#### Web Server Security Group
- Inbound:
  - Port 80 from ALB Security Group
  - Port 3306 for Aurora
- Outbound:
  - All traffic

## Load Balancer Setup
### Application Load Balancer
- Internet-facing
- Multiple AZ
- Security group: ALB Security Group
- Target group:
  - Protocol: HTTP
  - Port: 80
  - Health check: /index.php
  - Interval: 30 seconds

## EC2 Instances
### Web Server Configuration
- Update system commands:
  - sudo yum update -y
  - sudo yum install -y httpd php php-mysqlnd
  - sudo systemctl start httpd
  - sudo systemctl enable httpd

### Deploy Web Servers
- Instance type: t3.micro
- AMI: Amazon Linux 2
- Subnet: Public subnets
- Security group: Web Server Security Group
- User data: Installation script

## Aurora Database Setup
### Subnet Group
- Create db subnet group
- Add all public subnets

### Aurora Global Database
- Engine: Aurora MySQL 8.0
- Instance class: db.r5.large
- Multi-AZ: Yes
- Database name: registration
- Master username: admin
- Master password: [Secure password]

### Database Configuration
- Create database: registration
- Use database: registration
- Create table users:
  - id INT AUTO_INCREMENT PRIMARY KEY
  - name VARCHAR(100)
  - email VARCHAR(100)
  - company VARCHAR(100)
  - created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

## Route 53 Configuration
### DNS Setup
- Create hosted zone
- Add A record:
  - Type: A
  - Alias: Yes
  - Target: ALB DNS name

## Verification Steps
1. Check VPC and subnet configuration
2. Verify security group rules
3. Test ALB health checks
4. Validate EC2 instances
5. Confirm Aurora connectivity
6. Test DNS resolution

Author  
Created: February 2025  
Author: Leonard Palad  
Blog site: https://aws.leonardspalad.com/  
LinkedIn: https://www.linkedin.com/in/leonardspalad/
