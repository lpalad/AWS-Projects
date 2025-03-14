

# AWS Lex Documentation Chatbot

## Author
**Leonard S Palad**  
[Blog](https://www.cloudhermit.com.au/)

## 📌 Overview

The resources here enable you to deploy a chatbot that calls Lambda in one region, accesses a DynamoDB table in another, and uses Cognito credentials to keep your AWS keys secure. This multi-service approach drastically reduces the overhead of building an AI-driven help desk. This is a hands-on lab for building an **Amazon Lex chatbot** that integrates with **Lambda, DynamoDB, and S3**—plus a local **cheat sheet** of blog content. It’s suitable for answering business web site  questions and personal blog queries.

## 📂 Repository Structure

```
aws-docs-chatbot/
├── README.md                  # Documentation (this file)
├── config.py                  # Stores GitHub repo info, DynamoDB table names, and AWS region
├── scraper.py                 # Fetches markdown docs from GitHub and stores them in DynamoDB
├── lexv2_handler.py           # Lambda function scanning DynamoDB for relevant documentation
└── awsbot.js (optional)       # Frontend script for website integration
```

## 🏗 Architecture Overview

1️⃣ **User opens a web page** (served by S3 or any static hosting).  
2️⃣ **JavaScript (awsbot.js)** retrieves temporary credentials from Cognito (**Your-AWS-Region**), calls Lex to interpret user queries.  
3️⃣ **Lex Bot (Your-AWS-Region)** invokes a **Lambda function (us-east-1)** that queries the `AWSDocumentation` table in **DynamoDB**.  
4️⃣ **scraper.py** populates this DynamoDB table by pulling **.md files** from specific GitHub repositories (**e.g., aws-iot-docs**).  
5️⃣ **Combines AWS docs and personal blog posts** into a unified chatbot experience.

---

## ⚙️ Configuration: `config.py`

Replace placeholders with your own values.

```python
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
```

📌 **Security Note:** Do not store GitHub tokens in the config file—use **environment variables** instead.

---

## 🛠 GitHub Scraper: `scraper.py`

This script fetches markdown files from GitHub repos, **converts them to structured text**, and stores them in **DynamoDB**.

```python
import requests
import base64
import markdown
from bs4 import BeautifulSoup
import boto3
import time
import config

headers = {}
if config.GITHUB_TOKEN:
    headers['Authorization'] = f'token {config.GITHUB_TOKEN}'

def get_repo_contents(repo_name, path=""):
    url = f"https://api.github.com/repos/{config.GITHUB_ORG}/{repo_name}/contents/{path}"
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else None

def process_markdown_file(repo_name, file_path):
    url = f"https://api.github.com/repos/{config.GITHUB_ORG}/{repo_name}/contents/{file_path}"
    response = requests.get(url, headers=headers)
    content_data = response.json()
    file_content = base64.b64decode(content_data['content']).decode('utf-8')
    
    # Convert markdown to HTML, then extract text
    html = markdown.markdown(file_content)
    soup = BeautifulSoup(html, 'html.parser')
    paragraphs = [p.text for p in soup.find_all('p')]
    
    return {
        'id': f"{repo_name}#{file_path}",
        'service': repo_name.lower(),
        'title': file_path,
        'content': "\n".join(paragraphs),
        'url': f"https://github.com/{config.GITHUB_ORG}/{repo_name}/blob/master/{file_path}"
    }
```

Run it via:
```bash
python scraper.py
```

Ensure **DynamoDB table** exists before running.

---

## 🏗 Lambda Function: `lexv2_handler.py`

Handles **Amazon Lex** chatbot queries by searching **DynamoDB** for relevant AWS documentation.

```python
import json
import boto3

TABLE_NAME = "AWSDocumentation"
AWS_REGION = "us-east-1"

def lambda_handler(event, context):
    search_term = event.get('inputTranscript', "").strip()
    if not search_term:
        return format_response(event, "Which AWS service or topic do you need help with?")
    
    dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
    table = dynamodb.Table(TABLE_NAME)
    response = table.scan()
    
    matching_items = [item for item in response.get('Items', []) if search_term.lower() in item['content'].lower()]
    
    if matching_items:
        item = matching_items[0]
        message = f"Here's what I found about '{search_term}':\n\n{item['content'][:150]}...\n\nRead more at: {item['url']}"
        return format_response(event, message)
    else:
        return format_response(event, f"I couldn't find info about '{search_term}'. Try another query.")

def format_response(event, message):
    return {
        "sessionState": {"dialogAction": {"type": "Close"}},
        "messages": [{"contentType": "PlainText", "content": message}]
    }
```

**Deployment Instructions:**
```bash
zip function.zip lexv2_handler.py
aws lambda update-function-code \
  --function-name AWSDocsLexHandler \
  --zip-file fileb://function.zip \
  --region us-east-1
```

---

## 🔗 Quick Usage Guide

1️⃣ **Create DynamoDB Table** (`AWSDocumentation` in `us-east-1`).  
2️⃣ **Run `scraper.py`** to populate DynamoDB from GitHub docs.  
3️⃣ **Deploy `lexv2_handler.py`** as an AWS Lambda function.  
4️⃣ **Configure Amazon Lex** to call this Lambda during fulfillment.  
5️⃣ **Test the bot** in the **Lex Console** or integrate it into your website.

---

## 📜 License

This project is licensed under the **MIT License**.

## 📌 Author

[Leonard Palad](https://www.linkedin.com/in/leonardspalad/)  
[Blog](https://www.cloudhermit.com.au/)
