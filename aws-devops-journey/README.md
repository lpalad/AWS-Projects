# AWS High-Availability Infrastructure Lab

## The Problem We're Solving
When your entire business runs on a single server, you're one crash away from disaster. This lab implements a fault-tolerant, auto-scaling infrastructure that eliminates single points of failure - the same solution Fortune 500 companies pay consultants $250,000+ to implement.

## Architecture
ascii
                   AWS Cloud
┌──────────────────────────────────────────┐
│  VPC (10.0.0.0/16)                      │
│  ┌────────────────────────────────────┐  │
│  │            Load Balancer           │  │
│  │                 ▼                  │  │
│  │    ┌──────┐    ┌──────┐           │  │
│  │    │EC2 #1│    │EC2 #2│           │  │
│  │    └──────┘    └──────┘           │  │
│  │         ▼         ▼               │  │
│  │          S3 Website               │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘


Project Structure
aws-devops-journey/
├── infrastructure/
│   └── terraform/
│       ├── main.tf         # Main infrastructure code
│       └── s3-policy.tf    # S3 bucket policies
├── applications/
│   └── sample-app/
│       └── index.html      # Static website
└── README.md


Quick Start

# Initialize Terraform
cd infrastructure/terraform


terraform init

# Deploy infrastructure
terraform plan -out=tfplan
terraform apply tfplan


Prerequisites
AWS Account
Terraform installed
AWS CLI configured


Core Components
VPC with proper networking
Application Load Balancer for traffic distribution
Multi-AZ deployment for high availability
S3 static website hosting
Security groups and access controls


Security Implementation
Configured security groups
S3 bucket policies
Network access controls


Cost Optimization
Auto-scaling based on demand
Pay-per-use model
Resource optimization


Support
Create an issue in this repository for any questions or problems.

Author
Leonard S Palad

LinkedIn: https://www.linkedin.com/in/leonardspalad/
Blog: https://aws.leonardspalad.com/

