# Project Insight: Serverless Data Lake on AWS

Production-grade serverless data lake solution for real-time e-commerce clickstream analytics.

## Architecture Overview

```
Web Servers → Kinesis Firehose → Lambda (Data Cleanse) → S3 (Raw/Bronze)
                                                              ↓
                                                       Glue Crawler
                                                              ↓
                                                       Glue Data Catalog
                                                              ↓
                                                       Glue ETL Job (PySpark)
                                                              ↓
                                                       S3 (Curated/Silver - Parquet)
                                                              ↓
                                                       Athena (SQL Queries)

Step Functions orchestrates: Crawler → ETL Job → Curated Crawler
EventBridge triggers pipeline on new S3 objects
SNS sends alerts on pipeline failures
```

## Features

- **Real-time Ingestion**: Kinesis Firehose with Lambda transformation for data cleansing and PII masking
- **Automated Schema Discovery**: Glue Crawlers detect schema changes automatically
- **Incremental ETL**: Glue Job Bookmarks process only new files (cost optimization)
- **Optimized Storage**: JSON → Parquet conversion with Snappy compression
- **Event-Driven Architecture**: EventBridge triggers pipeline when new data arrives
- **Orchestration**: Step Functions manages workflow with retry logic
- **Alerting**: SNS notifications on pipeline failures
- **SQL Analytics**: Athena queries on partitioned Parquet data

## AWS Services Used

| Service | Purpose |
|---------|---------|
| Kinesis Data Firehose | Real-time data ingestion |
| AWS Lambda | Data transformation and PII masking |
| Amazon S3 | Raw (Bronze) and Curated (Silver) data storage |
| AWS Glue Crawler | Schema discovery and Data Catalog updates |
| AWS Glue ETL | PySpark transformation (JSON → Parquet) |
| AWS Glue Data Catalog | Centralized metadata repository |
| Amazon Athena | SQL query engine |
| AWS Step Functions | Workflow orchestration |
| Amazon EventBridge | Event-driven pipeline triggers |
| Amazon SNS | Failure alerting |

## Project Structure

```
project-insight/
├── README.md                 # This file
├── CLAUDE.md                 # Architecture documentation
├── cli.md                    # CLI commands reference (sanitized)
├── instruction.md            # Step-by-step setup guide
├── .gitignore                # Git ignore patterns
├── test-clickstream.json     # Sample clickstream data
├── test-clickstream.csv      # Sample clickstream data (CSV)
└── test-ecommerce.csv        # Sample e-commerce data (sanitized)
```

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI v2 installed and configured
- Python 3.9+ (for local testing)
- ~$0.30 - $1.00 AWS cost for a 48-hour lab

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/project-insight-aws-data-lake.git
cd project-insight-aws-data-lake
```

### 2. Set Environment Variables
```bash
export AWS_REGION="ap-southeast-2"  # or your preferred region
export PROJECT_NAME="project-insight"
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export RAW_BUCKET="${PROJECT_NAME}-raw-${AWS_ACCOUNT_ID}"
export CURATED_BUCKET="${PROJECT_NAME}-curated-${AWS_ACCOUNT_ID}"
export SCRIPTS_BUCKET="${PROJECT_NAME}-scripts-${AWS_ACCOUNT_ID}"
export ATHENA_BUCKET="${PROJECT_NAME}-athena-${AWS_ACCOUNT_ID}"
```

### 3. Follow the Setup Guide
See [cli.md](cli.md) for complete step-by-step CLI commands to deploy the entire infrastructure.

## Key Implementation Details

### Lambda Data Transformation
- Strips whitespace from all string fields
- Masks IP addresses (last two octets replaced with `xxx.xxx`)
- Adds `processed_at` timestamp
- Handles malformed records gracefully

### Glue ETL Job
- Reads from Glue Data Catalog (not S3 directly)
- Extracts year/month/day from timestamp for partitioning
- Converts to Parquet with Snappy compression
- Job Bookmarks ensure incremental processing

### Step Functions Workflow
1. Start Raw Crawler → Wait for completion
2. Run ETL Job (sync) → Wait for completion
3. Start Curated Crawler → Wait for completion
4. On any failure → Send SNS alert

## Cost Optimization

- **Glue Job Bookmarks**: Only process new files
- **Parquet Format**: 10x smaller than JSON, columnar for Athena
- **G.1X Workers**: Minimum Glue worker size
- **Serverless**: Pay only for what you use

## Cleanup

To avoid ongoing charges, run the cleanup commands in [cli.md](cli.md#phase-13-cleanup-tear-down).

## License

MIT License - See [LICENSE](LICENSE) for details.

## Author

Leonard S Palad

## Related Projects

- [Azure Data Engineering Portfolio](https://github.com/lpalad/Azure-Projects-Data-AI-Engineering)
- [Databricks Projects](https://github.com/lpalad/DataBricks-Projects)
