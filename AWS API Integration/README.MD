# THE 3-MINUTES API SOLUTION

A **Python application** that collects data from the **TSM API**, tracks **GPS location data**, and stores power consumption metrics in **Google Sheets**.

## 🚀 Features

✅ **Fetches historical consumption data** from TSM API  
✅ **Tracks GPS location data**  
✅ **Stores data in Google Sheets**  
✅ **Calculates daily power consumption metrics**  
✅ **Supports battery and generator consumption tracking**  

## 🛠 Prerequisites

- **Python 3.7+**
- **Google Sheets API access**
- **TSM API access**
- Required Python packages (see `requirements.txt`)

## ⚙️ Configuration

Create a `config.py` file with the following structure:

```python
# Google Sheets Configuration
SHEET_ID = 'YOUR_GOOGLE_SHEET_ID'
CREDENTIALS_PATH = 'path/to/your/credentials.json'

# TSM API Configuration
TSM_INSTALLATION_ID = 'YOUR_TSM_INSTALLATION_ID'
TSM_TOKEN = 'YOUR_TSM_API_TOKEN'
```

## 📂 Project Structure

```
project-root/
├── src/
│   ├── tess.py
│   └── config.py
├── credentials/
│   └── google_credentials.json
├── requirements.txt
└── README.md
```

## 📥 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/TSM-Data-Collector.git
cd TSM-Data-Collector
```

### 2️⃣ Install Required Packages

```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Configuration Files

Follow the **[Configuration](#-configuration)** section to set up your API keys and credentials.

## ▶️ Usage

Run the main script:

```bash
python src/tess.py
```

## 📊 Data Structure

### **Main Sheet Columns**

| Column Name       | Description                  |
|------------------|------------------------------|
| Date            | Timestamp of entry            |
| Battery (kWh)   | Power consumed from battery   |
| Generator (kWh) | Power generated               |
| Consumption (kWh) | Total power consumed        |
| Installation Name | TSM Installation Identifier |

### **GPS Data Sheet Columns**

| Column Name       | Description                  |
|------------------|------------------------------|
| Date            | Timestamp of GPS entry        |
| Latitude        | GPS Latitude                  |
| Longitude       | GPS Longitude                 |
| Installation Name | TSM Installation Identifier |

## 📦 Required Python Packages

```bash
pip install pandas google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests
```

## 📜 License

This project is licensed under the **MIT License**.

## 📌 Author

[Leonard Palad](https://www.linkedin.com/in/leonardspalad/)  
[Blog](https://www.cloudhermit.com.au/)
