# 📌 BESS Data Collector

## Overview  
BESS Data Collector is an **AWS Lambda**-based solution that fetches **Battery Energy Storage System (BESS) data** from an **external API**, processes it, and stores it in **Amazon DynamoDB**. Additionally, it integrates with **Google Sheets** for real-time data reporting and supports **GPS data collection** for tracking energy assets.

---

## 🏗 Architecture  

The following **ASCII architecture diagram** illustrates the system flow:

```plaintext
                   +---------------------+
                   |  External API       |
                   |  (Energy Data)      |
                   +---------------------+
                            |
                            v
                   +----------------+
                   |  AWS Lambda     |
                   |  (Python Script)|
                   +----------------+
                            |
        ---------------------------------------
        |                                      |
        v                                      v
+-----------------+                      +-----------------+
|  DynamoDB       |  <-- Stores Data --> | Google Sheets  |
| (Storage Layer) |                      | (Report Layer) |
+-----------------+                      +-----------------+
🚀 Features
✔️ Data Retrieval: Fetches BESS energy stats and GPS data from an external API
✔️ AWS Lambda Ready: Deployable as a serverless function
✔️ DynamoDB Storage: Efficient, scalable NoSQL storage
✔️ Google Sheets Integration: Pushes processed data for live reports
✔️ Security & Logging: Implements error handling and logging for tracking

🛠 Installation
1️⃣ Clone the Repository
bash
Copy
Edit
git clone https://github.com/YOUR_USERNAME/BESS-Data-Collector.git
cd BESS-Data-Collector
2️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Configure Environment Variables
Create a .env file in the root directory and add:

ini
Copy
Edit
API_INSTALLATION_ID=your_installation_id
API_TOKEN=your_api_token
SHEET_ID=your_google_sheets_id
AWS_REGION=your_aws_region
DYNAMODB_TABLE_NAME=your_table_name
📜 Usage
Run Locally
bash
Copy
Edit
python bess.py
Deploy to AWS Lambda
bash
Copy
Edit
zip -r deployment.zip . -x '*.git*'
aws lambda update-function-code \
  --function-name BESS_Data_Collector \
  --zip-file fileb://deployment.zip
📡 API Endpoints (Future Enhancement)
Method	Endpoint	Description
GET	/api/v1/bess-data	Fetch processed BESS data
GET	/api/v1/gps-data	Fetch GPS heatmap data
POST	/api/v1/data	Upload new energy readings
🔧 Sample Code
Fetch External API Data
python
Copy
Edit
import requests
import os

API_URL = "https://external-api.com/v2/installations"
API_TOKEN = os.getenv("API_TOKEN")

def get_api_data():
    headers = {"x-authorization": f"Token {API_TOKEN}"}
    response = requests.get(f"{API_URL}/stats", headers=headers)
    return response.json()
Store Data in DynamoDB
python
Copy
Edit
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE_NAME"))

def save_to_dynamodb(data):
    table.put_item(Item=data)
🔒 Security Considerations
🔹 IAM Role Restrictions: Lambda should have least privilege access
🔹 Environment Variables: Avoid hardcoding sensitive credentials
🔹 API Gateway & Authentication: Secure API access before exposing
🔹 Monitoring & Logging: Implement CloudWatch logs for debugging
📜 License
This project is licensed under the MIT License.

🤝 Contributing
Contributions are welcome! Please submit a Pull Request or open an Issue to discuss changes.
