# AWS Projects Repository

## Overview
A collection of AWS and cloud projects demonstrating infrastructure, AI/ML, DevOps, and architecture patterns. Each project includes documentation, code, and best practices.

## Projects

### AI / Machine Learning
- [Pinecone RAG System](./Pinecone-RAG-System/) - Production RAG system for 57 AI/ML books **(Azure Deployed)**
  - Hierarchical semantic chunking with 75th percentile breakpoints
  - Multi-query retrieval, HyDE, Graph RAG
  - Pinecone vector DB, OpenAI embeddings, Cohere reranking
  - 80-95% relevance scores

- [House Price Predictor](./House-Price-Predictor/) - End-to-end MLOps project
  - Data preprocessing and feature engineering
  - Model training and experimentation
  - MLflow tracking and versioning

- [AWS Docs Chatbot](./aws-docs-chatbot/) - AI-powered documentation assistant
  - Natural language querying
  - AWS documentation integration

### Infrastructure as Code
- [Terraform ECS Fargate](./Terraform/) - Production-grade AWS ECS deployment
  - Modular Terraform (VPC, ALB, ECS, IAM, ECR)
  - ECS Fargate with auto-scaling
  - GitHub Actions CI/CD pipeline
  - CloudWatch logging and monitoring

### CI/CD & DevOps
- [CI/CD Pipeline](./CI-CD/) - Automated deployment workflows
  - GitHub Actions with S3 sync
  - Static website hosting
  - Secure credential management

- [AWS DevOps Journey](./aws-devops-journey/) - DevOps learning path and implementations

### Networking & CDN
- [AWS CloudFront with Nginx Reverse Proxy](./AWS%20CloudFront%20with%20Nginx%20Reverse%20Proxy%20Setup/) - CDN and proxy configuration
  - CloudFront distribution setup
  - Nginx reverse proxy integration
  - SSL/TLS configuration

### Architecture
- [AWS Decoupled Architecture](./aws-decoupled-architecture/) - Event-driven microservices pattern
  - Loosely coupled components
  - Message queue integration

- [AWS Multi-Region HA](./aws-multi-region-ha/) - High availability across regions
  - Multi-region failover
  - Disaster recovery patterns

### IoT
- [AWS IoT Core](./IoT/) - ANZ Air Quality Monitoring
  - IoT Core broker setup
  - Lambda Functions
  - DynamoDB integration
  - API Gateway

- [AWS IoT Lambda](./aws-iot-lambda/) - IoT event processing
  - Lambda triggers from IoT events
  - Data transformation pipelines

### API Integration
- [AWS API Integration](./AWS%20API%20Integration/) - API Gateway patterns
  - REST API design
  - Lambda integration
  - Authentication and authorization

## Blog Posts
Related blog posts: https://www.cloudhermit.com.au

## Author
**Leonard S Palad** | MBA | Master of AI (In-progress)
- AI Portfolio: https://salesconnect.com.au/aip.html
- LinkedIn: https://www.linkedin.com/in/leonardspalad/
- Blog: https://www.cloudhermit.com.au/

## Updates
- December 2025: Added Pinecone RAG System (Azure deployed)
- December 2025: Added Terraform ECS Fargate with auto-scaling
- December 2025: Added House Price Predictor MLOps project

## Note
All code and configurations are sanitized for security. Remember to:
- Replace placeholder values
- Follow AWS security best practices
- Review and adapt code for your environment
