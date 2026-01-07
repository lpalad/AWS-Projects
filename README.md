<h1 align="center">⚡ The AWS Production Vault: 12 Architected Solutions. Zero Fluff.</h1>

![Build with AWS](https://img.shields.io/badge/Build_with-AWS-FF9900?style=for-the-badge&logo=amazonwebservices&logoColor=white)

> "Most portfolios show tutorials. This one shows results. Twelve production-ready systems built to survive real-world chaos, not just pass a test."

[![Live Demo](https://img.shields.io/badge/Live_Demo-See_It_Working-FF6B6B?style=for-the-badge)](https://salesconnect.com.au/aip.html)

---

## Executive Summary: Engineering Profit through Data Rigor

In the Australian and New Zealand tech landscape, "good enough" is a liability. Companies need systems that scale without exploding the budget and AI that provides answers, not hallucinations.

With over a decade in the IT field and an MBA, I bridge the gap between technical complexity and commercial reality. My AWS architecture is defined by three logical pillars:

**Certainty:** I build Infrastructure as Code (IaC). Using modular Terraform patterns, I eliminate the "human error" of manual console clicks.

**Efficiency:** From IoT Core monitoring to ECS Fargate auto-scaling, I build for "Hands-Off" operations. I turn maintenance hours into innovation time.

**Fiscal Discipline:** I treat AWS credits like cash. By using decoupled architectures and serverless Lambda processing, I ensure you only pay for what you compute.

---

## The Solutions: Real Problems. Solved.

### 01: AI & Machine Learning

**[Pinecone RAG System](./Pinecone-RAG-System/):** A production-grade retrieval engine. Uses hierarchical semantic chunking and reranking to achieve 95% relevance scores.

**[House-Price-Predictor](./House-Price-Predictor/):** Full MLOps lifecycle. Every experiment is logged in MLflow to ensure results are never a "one-off" fluke.

**[AWS Docs Chatbot](./aws-docs-chatbot/):** Natural language interface to official documentation. No more digging through manuals.

### 02: Infrastructure & Architecture

**[Terraform ECS Fargate](./Terraform/):** Five modular components (VPC, ALB, ECS, IAM, ECR). One command to deploy a high-availability environment.

**[IoT Core ANZ Monitoring](./IoT/):** Real-time environmental tracking across Australia and New Zealand. Built for real sensors, not simulated data.

**[Multi-Region HA](./aws-multi-region-ha/):** Disaster recovery that actually works. Automated failover logic across AWS regions.

**[Decoupled Architecture](./aws-decoupled-architecture/):** Event-driven microservices. Components fail independently so the business keeps running.

---

## Why Hire Me?

**I deploy business-critical assets. I don't play with toys.**

| The Asset | The Logical Proof | The Economic Impact |
|-----------|-------------------|---------------------|
| **Production RAG AI** | 57 AI/ML books indexed with 80-95% retrieval accuracy. | Ends AI Hallucination. Factual, technical answers for real support teams. |
| **Self-Scaling Infra** | Terraform-managed ECS Fargate that scales 2-10 tasks. | Optimises OpEx. Never pay for idle compute; never crash during a spike. |
| **IoT ANZ Network** | Real-time air quality monitoring across AU & NZ. | Operational Intelligence. Sub-second latency for thousands of real sensors. |
| **Disciplined MLOps** | XGBoost prediction with 100% tracking in MLflow. | Eliminates "Black Box" Risk. Every model version is audit-ready. |

---

## Project Structure (The Architecture)

```
AWS-Projects/
├── Pinecone-RAG-System/       # AI Retrieval — 80-95% Accuracy
├── House-Price-Predictor/     # MLOps Pipeline (XGBoost + MLflow)
├── Terraform/                 # ECS Fargate (Auto-scaling Infrastructure)
├── IoT/                       # ANZ Air Quality Monitoring (Real Sensors)
├── aws-multi-region-ha/       # Disaster Recovery (Failover Logic)
└── CI-CD/                     # Automated Deployment Workflows
```

---

## Tech Stack: Tools of Precision

### Cloud & Platform
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=white)
![Microsoft Azure](https://img.shields.io/badge/Microsoft_Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)
![Pinecone](https://img.shields.io/badge/Pinecone-000000?style=for-the-badge&logo=pinecone&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![Cohere](https://img.shields.io/badge/Cohere-39594D?style=for-the-badge&logo=cohere&logoColor=white)

**AWS:** ECS, Fargate, Lambda, S3, CloudFront, IoT Core, API Gateway, Route53.
**Azure:** Production deployment for RAG systems.

### Infrastructure & DevOps
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)
![NGINX](https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=nginx&logoColor=white)

**IaC:** Terraform (Modular Architecture).
**CI/CD:** GitHub Actions.
**Containers:** Docker, ECR.

### AI/ML & Data Processing
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-FF6600?style=for-the-badge&logo=xgboost&logoColor=white)
![MLflow](https://img.shields.io/badge/MLflow-0194E2?style=for-the-badge&logo=mlflow&logoColor=white)

**Models & Frameworks:** XGBoost, OpenAI, Cohere (Reranking), LangChain.
**MLOps:** MLflow (Experiment & Model Tracking).
**Vector DB:** Pinecone.

### Frameworks & APIs
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)

**Backend:** FastAPI, Python.
**Web:** Nginx (Reverse Proxy), REST APIs.

### Data Storage & Monitoring
![DynamoDB](https://img.shields.io/badge/DynamoDB-4053D6?style=for-the-badge&logo=amazondynamodb&logoColor=white)
![S3](https://img.shields.io/badge/Amazon_S3-569A31?style=for-the-badge&logo=amazons3&logoColor=white)
![CloudWatch](https://img.shields.io/badge/CloudWatch-FF4F8B?style=for-the-badge&logo=amazoncloudwatch&logoColor=white)

**Databases:** DynamoDB (Time-series), SQL Server.
**Monitoring:** AWS CloudWatch, MLflow UI.

---

## Usage: No-Nonsense Setup

1. **Clone the Vault:**
   ```bash
   git clone https://github.com/lpalad/AWS-Projects.git
   ```

2. **Deploy Infrastructure:**
   Navigate to `Terraform/` and run:
   ```bash
   terraform init && terraform apply
   ```

3. **Review MLOps:**
   Navigate to `House-Price-Predictor/` to view MLflow logs.

---

## About Me: Leonard S Palad

**MBA | Master of AI (In Progress)**

I build data systems that connect directly to commercial outcomes. With over a decade in the IT field, I have navigated the shift from legacy infrastructure to modern cloud-native architecture. I bridge the gap between technical rigor and business profit.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/leonardspalad/)
[![AI Portfolio](https://img.shields.io/badge/AI_Portfolio-View_Projects-4285F4?style=for-the-badge)](https://salesconnect.com.au/aip.html)
[![Blog](https://img.shields.io/badge/Blog-Cloud_Hermit-FF5722?style=for-the-badge)](https://www.cloudhermit.com.au/)

---

*I built these projects to demonstrate what I can do. If you are hiring for cloud, AI/ML, or DevOps roles, I would like to talk.*
