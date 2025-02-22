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
