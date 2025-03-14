# config.py

GITHUB_TOKEN = ""        # Add your GitHub personal access token if needed
GITHUB_ORG = "awsdocs"   # Target GitHub organization

# Target repositories to scrape
TARGET_REPOS = [
    "aws-iot-docs",
    "aws-lambda-developer-guide"
]

# AWS settings
AWS_REGION = "us-east-1"
TABLE_NAME = "AWSDocumentation"
