<p align="center">
  <img src="https://img.shields.io/badge/Serverless_Data_Lake-Real--Time_Clickstream_Analytics-FF9900?style=for-the-badge" alt="Serverless Data Lake"/>
</p>

<h3 align="center">Production-Ready AWS Data Lake | Ingestion, ETL, and SQL Analytics</h3>

<p align="center">
  <img src="https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=white" alt="AWS"/>
  <img src="https://img.shields.io/badge/Kinesis-FF4F8B?style=for-the-badge&logo=amazonaws&logoColor=white" alt="Kinesis"/>
  <img src="https://img.shields.io/badge/AWS_Glue-8C4FFF?style=for-the-badge&logo=amazonaws&logoColor=white" alt="Glue"/>
  <img src="https://img.shields.io/badge/Athena-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white" alt="Athena"/>
  <img src="https://img.shields.io/badge/Step_Functions-FF4F8B?style=for-the-badge&logo=amazonaws&logoColor=white" alt="Step Functions"/>
</p>

---

> "Traditional data warehouses are too slow for modern e-commerce. I built this serverless data lake to handle real-time clickstream ingestion, automated schema discovery, and cost-optimised SQL analytics—all without managing a single server."

---

<h2 align="center">Strategic Context: Architecture That Scales</h2>

I don't build "proof-of-concepts"; I build production assets. With over a decade in the IT field and an MBA, I understand that a data lake is only as good as its governance and cost-efficiency. This solution is designed for the Australian market, where minimising "Technical Debt" and "Cloud Waste" is a commercial priority.

My architecture is defined by three logical pillars:

**Certainty:** I use Step Functions for orchestration. Every step—from crawling raw data to the final ETL—is monitored with automated retry logic and SNS failure alerts.

**Efficiency:** I implement PII Masking at the point of ingestion. Using Lambda transformations within Kinesis Firehose, sensitive data (like IP addresses) is sanitised before it ever hits S3.

**Fiscal Discipline:** I utilise Glue Job Bookmarks and Parquet conversion. This ensures we only process new files and reduce Athena query costs by up to 90% through columnar compression.

---

<h2 align="center">Why Hire Me?</h2>

I deploy business-critical assets. I don't play with toys.

| The Asset | The Logical Proof | The Economic Impact |
|-----------|-------------------|---------------------|
| **Real-Time Ingestion** | Kinesis Firehose with inline Lambda for PII masking. | Risk Mitigation. Protects customer privacy and ensures compliance from second one. |
| **Incremental ETL** | Glue PySpark jobs with Job Bookmarks enabled. | Massive Cost Savings. Processes only new data, preventing redundant compute spend. |
| **Serverless Orchestration** | Step Functions managing the Crawler → ETL → Crawler workflow. | Operational Stability. Automated failure handling and real-time SNS alerting. |
| **Optimised Analytics** | Automatic JSON to Parquet conversion with Snappy compression. | Performance ROI. 10x faster Athena queries and significant storage reduction. |

---

<h2 align="center">The Solutions: Real Problems. Solved.</h2>

**The Problem:** E-commerce clickstream data is messy, arrives in real-time, and is expensive to query in raw JSON format.

**The Logic:** We use a Medallion-inspired serverless approach. Raw data is cleaned via Lambda, cataloged by Glue, and transformed into partitioned Parquet for high-speed SQL access.

**The Result:** Business analysts can query real-time trends in Athena with minimal latency and near-zero infrastructure overhead.

---

<h2 align="center">Tech Stack: Tools of Precision</h2>

### Ingestion & Compute

- **Kinesis Data Firehose**: Real-time stream delivery.
- **AWS Lambda**: Data cleansing and PII masking (Strips whitespace, masks IP octets).

### Storage & Metadata

- **Amazon S3**: Multi-tier storage (Raw/Bronze & Curated/Silver).
- **AWS Glue Data Catalog**: Centralised metadata management.

### ETL & Orchestration

- **AWS Glue ETL**: PySpark jobs for JSON → Parquet conversion.
- **AWS Step Functions**: State machine orchestration with retry logic.
- **AWS Glue Crawler**: Automated schema discovery.

### Analytics & Monitoring

- **Amazon Athena**: Columnar SQL queries.
- **Amazon EventBridge**: Event-driven pipeline triggers.
- **Amazon SNS**: Critical failure alerting.

---

<h2 align="center">Project Structure</h2>

```
project-insight/
├── README.md                 # Strategic Overview
├── CLAUDE.md                 # Detailed Architecture Docs
├── cli.md                    # No-Nonsense Setup Commands
├── instruction.md            # Step-by-step Setup Guide
├── test-clickstream.json     # Sample Ingestion Data
└── scripts/                  # Glue PySpark & Lambda Source Code
```

---

<h2 align="center">Usage: No-Nonsense Setup</h2>

### 1. Prerequisites

- AWS CLI v2 configured with `ap-southeast-2` (Sydney) or your preferred region.
- Python 3.9+ for local script testing.

### 2. Environment Configuration

```bash
export AWS_REGION="ap-southeast-2"
export PROJECT_NAME="project-insight"
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
# Define bucket names for the pipeline
export RAW_BUCKET="${PROJECT_NAME}-raw-${AWS_ACCOUNT_ID}"
export CURATED_BUCKET="${PROJECT_NAME}-curated-${AWS_ACCOUNT_ID}"
```

### 3. Deployment

I have provided a comprehensive CLI reference to avoid "Console clicking" errors.

- **Step A**: Follow the sequence in [cli.md](cli.md) to provision S3 buckets and IAM roles.
- **Step B**: Upload the Glue ETL script to the scripts bucket.
- **Step C**: Trigger the Step Functions state machine to start the pipeline.

---

<h2 align="center">Key Implementation Details</h2>

- **PII Masking**: Lambda replaces the last two octets of IP addresses with `xxx.xxx` to comply with privacy standards.
- **Partitioning**: The Glue ETL job extracts year, month, and day from timestamps to create an efficient folder structure in S3 for Athena.
- **Fault Tolerance**: Step Functions ensures that if the ETL job fails, the SNS alert is fired immediately, preventing "silent failures."

---

<h2 align="center">About Me: Leonard S Palad</h2>

**MBA | Master of AI (In Progress)**

I build data systems that connect directly to commercial outcomes. With over a decade in the IT field, I have navigated the shift from legacy infrastructure to modern cloud-native architectures. I bridge the gap between technical rigor and business profit.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/leonardspalad/)
[![Databricks Projects](https://img.shields.io/badge/Databricks-Projects-FF3621?style=for-the-badge&logo=databricks&logoColor=white)](https://github.com/lpalad/DataBricks-Projects)
[![Azure Portfolio](https://img.shields.io/badge/Azure-Portfolio-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://github.com/lpalad/Azure-Projects-Data-AI-Engineering)

---

## License

MIT License
