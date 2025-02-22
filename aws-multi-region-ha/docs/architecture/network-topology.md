# Network Topology

## Overview
This document details the network architecture implemented across two AWS regions (ap-southeast-2 and us-west-2) to support a highly available application infrastructure.

## Global Infrastructure
- Primary Region: Sydney (ap-southeast-2)
- Secondary Region: Oregon (us-west-2)
- Route 53 for DNS management and traffic routing

## Sydney Region (Primary)
### VPC Configuration
- VPC CIDR: 10.1.0.0/16
- Internet Gateway: Attached
- Region: ap-southeast-2

### Subnet Layout
#### Public Subnets
- AZ-a: 10.1.1.0/24
- AZ-b: 10.1.2.0/24
- Purpose: Web servers and Application Load Balancer

### Routing Configuration
- Public Route Tables
  - Default route (0.0.0.0/0) → Internet Gateway
  - Local route (10.1.0.0/16) → Local

## Oregon Region (Secondary)
### VPC Configuration
- VPC CIDR: 10.1.0.0/16
- Internet Gateway: Attached
- Region: us-west-2

### Subnet Layout
#### Public Subnets
- AZ-a: 10.1.3.0/24
- AZ-b: 10.1.4.0/24
- Purpose: API servers and read replicas

### Routing Configuration
- Public Route Tables
  - Default route (0.0.0.0/0) → Internet Gateway
  - Local route (10.1.0.0/16) → Local

## Network Security
### Security Groups
- ALB Security Group
  - Inbound: Port 80 from 0.0.0.0/0
  - Outbound: All traffic

- Web Server Security Group
  - Inbound: Port 80 from ALB Security Group
  - Inbound: Port 3306 for database connectivity
  - Outbound: All traffic

- API Server Security Group
  - Inbound: Port 3000 from specified IPs
  - Inbound: Port 3306 for database connectivity
  - Outbound: All traffic

### Network ACLs
- Default NACLs with standard allow rules
- Customized rules based on security requirements

## Load Balancer Configuration
### Application Load Balancer
- Internet-facing
- Cross-zone load balancing enabled
- HTTP listener on port 80
- Health checks configured for target groups

## Cross-Region Connectivity
- Aurora Global Database replication
- Automated failover capability
- Near real-time data synchronization

Author  
Created: February 2025  
Author: Leonard Palad  
Blog site: https://aws.leonardspalad.com/  
LinkedIn: https://www.linkedin.com/in/leonardspalad/
