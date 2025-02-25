# Multi-Region High-Availability AWS Infrastructure

## Overview
This repository documents the implementation of a highly available, multi-region AWS infrastructure with global database replication and secure API access. 

## Architecture Highlights
- Multi-region deployment (ap-southeast-2 and us-west-2)
- Aurora Global Database for data replication
- Load-balanced web servers
- Secure API service with token authentication
- Route 53 for DNS management

## Key Components
- Application Load Balancer
- EC2 instances in multiple Availability Zones 
- Aurora Global Database
- Node.js API Service
- Security Groups and Network ACLs

## Prerequisites
- AWS Account
- Basic understanding of:
  - AWS Services
  - Networking concepts
  - Database management
  - API development

## Documentation Structure
- `/docs/architecture/` - Detailed design documentation
- `/docs/setup/` - Implementation guides
- `/docs/operations/` - Operational procedures
- `/diagrams/` - Infrastructure diagrams

## Security Considerations
- Token-based API authentication
- Network security best practices
- Data encryption in transit and at rest
- Least privilege access principles

## License
[License type to be determined]

Author  
Created: February 2025  
Author: Leonard Palad  
Blog site: https://www.cloudhermit.com.au/
LinkedIn: https://www.linkedin.com/in/leonardspalad/
