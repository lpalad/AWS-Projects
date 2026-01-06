# 12 Production-Ready AWS Projects. Built. Deployed. Documented.

![Build with AWS](https://img.shields.io/badge/Build_with-AWS-FF9900?style=for-the-badge&logo=amazonwebservices&logoColor=white)

Most portfolios show tutorials. This one shows results.

Every project here solves a real problem. Every system runs in production. Every line of code is tested. I built these projects because I wanted to prove I can deliver—not just learn.

[![Live Demo](https://img.shields.io/badge/Live_Demo-See_It_Working-FF6B6B?style=for-the-badge)](https://salesconnect.com.au/aip.html)

---

## What I Built (And Why It Matters)

**A RAG system that actually works.** 57 AI/ML books. 80-95% retrieval accuracy. Deployed on Azure. Most RAG demos fail in production. This one does not.

**Infrastructure that scales itself.** Terraform modules deploy ECS Fargate containers. They scale from 2 to 10 tasks based on CPU load. No manual intervention. No downtime.

**An MLOps pipeline with full tracking.** House price predictions using XGBoost. Every experiment logged in MLflow. Every model versioned. Every result reproducible.

**IoT monitoring across Australia and New Zealand.** Real-time air quality data flows through MQTT, gets processed by Lambda, stored in DynamoDB, and served via REST API. The system handles thousands of sensor readings without breaking.

---

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

## The Projects

### AI & Machine Learning

#### [Pinecone RAG System](./Pinecone-RAG-System/) — Live on Azure
I indexed 57 AI/ML books into a production RAG system. The results speak for themselves:
- **80-95% relevance scores** on retrieval tests
- Hierarchical semantic chunking with 75th percentile breakpoints
- Multi-query retrieval, HyDE, and Graph RAG techniques
- Pinecone for vectors, OpenAI for embeddings, Cohere for reranking

This is not a tutorial project. This is a system that answers complex technical questions accurately.

#### [House Price Predictor](./House-Price-Predictor/) — Full MLOps Pipeline
End-to-end machine learning with proper engineering discipline:
- 15+ engineered features from raw housing data
- XGBoost model with systematic hyperparameter tuning
- MLflow tracks every experiment, every metric, every model version
- Reproducible results. No guesswork.

#### [AWS Docs Chatbot](./aws-docs-chatbot/)
Natural language interface for AWS documentation. Ask questions in plain English. Get accurate answers from official docs.

---

### Infrastructure as Code

#### [Terraform ECS Fargate](./Terraform/) — Production Architecture
Five Terraform modules. One command to deploy. Zero manual configuration.
- **VPC, ALB, ECS, IAM, ECR** — all modular, all reusable
- Auto-scaling from 2 to 10 tasks based on CPU utilization
- GitHub Actions deploys on every push to main
- CloudWatch captures every log, every metric, every health check

I built this because clicking through the AWS console is slow and error-prone. Infrastructure should be code.

---

### CI/CD & DevOps

#### [CI/CD Pipeline](./CI-CD/)
GitHub Actions workflow that deploys to S3 on every commit. Static website hosting with secure credential management. Simple. Reliable. Fast.

#### [AWS DevOps Journey](./aws-devops-journey/)
Documentation of DevOps practices I implemented and learned. Real implementations, not theory.

---

### Networking & CDN

#### [CloudFront + Nginx Reverse Proxy](./AWS%20CloudFront%20with%20Nginx%20Reverse%20Proxy%20Setup/)
CloudFront distribution with Nginx backend. SSL/TLS configured properly. Content served fast from edge locations worldwide.

---

### Architecture Patterns

#### [Decoupled Architecture](./aws-decoupled-architecture/)
Event-driven microservices that communicate through message queues. Components fail independently. The system keeps running.

#### [Multi-Region High Availability](./aws-multi-region-ha/)
Failover across AWS regions. When one region goes down, traffic routes to another. Disaster recovery that actually works.

---

### IoT Solutions

#### [IoT Core — ANZ Air Quality Monitoring](./IoT/)
Real-time environmental monitoring across Australia and New Zealand:
- IoT Core MQTT broker ingests sensor data
- Lambda processes each reading in milliseconds
- DynamoDB stores time-series data efficiently
- REST API serves the data to any client

This handles production traffic. Not simulated loads. Real sensors. Real data.

#### [IoT Lambda Processing](./aws-iot-lambda/)
Event-driven data transformation. IoT events trigger Lambda functions. Data gets cleaned, transformed, and stored automatically.

---

### API Integration

#### [AWS API Integration](./AWS%20API%20Integration/)
REST API patterns using API Gateway and Lambda. Proper authentication. Proper authorization. Proper error handling.

---

## Project Structure

```
AWS-Projects/
├── Pinecone-RAG-System/       # Production RAG — 80-95% accuracy
├── House-Price-Predictor/     # MLOps with MLflow tracking
├── aws-docs-chatbot/          # AI documentation assistant
├── Terraform/                 # ECS Fargate infrastructure
├── CI-CD/                     # GitHub Actions pipelines
├── aws-devops-journey/        # DevOps implementations
├── Integration/               # CloudFront + Nginx
├── aws-decoupled-architecture/# Event-driven microservices
├── aws-multi-region-ha/       # Multi-region failover
├── IoT/                       # Air quality monitoring
├── aws-iot-lambda/            # IoT event processing
└── Setup/                     # API Gateway patterns
```

---

## About Me

**Leonard S Palad** | MBA | Master of AI (In Progress)

I build systems that work. I document everything. I believe infrastructure should be code, experiments should be tracked, and production systems should be tested.

[![AI Portfolio](https://img.shields.io/badge/AI_Portfolio-View_Projects-4285F4?style=for-the-badge)](https://salesconnect.com.au/aip.html)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/leonardspalad/)
[![Blog](https://img.shields.io/badge/Blog-Cloud_Hermit-FF5722?style=for-the-badge)](https://www.cloudhermit.com.au/)

---

## Recent Updates

- **December 2025:** Deployed Pinecone RAG System to Azure production
- **December 2025:** Released Terraform ECS Fargate with auto-scaling
- **December 2025:** Completed House Price Predictor MLOps pipeline

---

## A Note on Security

All credentials are removed. All secrets are sanitized. If you use this code, replace the placeholder values with your own. Follow AWS security best practices. Test in a non-production environment first.

---

*I built these projects to demonstrate what I can do. If you are hiring for cloud, AI/ML, or DevOps roles, I would like to talk.*
