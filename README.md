# AWS Projects Repository

## Tech Stack

### Cloud & Platform
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=white)
![Microsoft Azure](https://img.shields.io/badge/Microsoft_Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-000000?style=for-the-badge&logo=pinecone&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Cohere](https://img.shields.io/badge/Cohere-39594D?style=for-the-badge&logo=cohere&logoColor=white)

### Infrastructure & DevOps
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![NGINX](https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=nginx&logoColor=white)

### AI/ML & Data Processing
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-FF6600?style=for-the-badge&logo=xgboost&logoColor=white)

### Frameworks & APIs
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LlamaIndex](https://img.shields.io/badge/LlamaIndex-8B5CF6?style=for-the-badge&logoColor=white)

### Data Storage & Monitoring
![DynamoDB](https://img.shields.io/badge/DynamoDB-4053D6?style=for-the-badge&logo=amazondynamodb&logoColor=white)
![S3](https://img.shields.io/badge/Amazon_S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white)
![CloudWatch](https://img.shields.io/badge/CloudWatch-FF4F8B?style=for-the-badge&logo=amazoncloudwatch&logoColor=white)
![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)

### Tools
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

---

## Overview
A collection of AWS and cloud projects demonstrating infrastructure, AI/ML, DevOps, and architecture patterns. Each project includes documentation, code, and best practices.

![AWS Architecture](./aws.png)

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
