"""
Configuration file for TSM Data Collection Application

# Google Sheets Configuration
SHEET_ID = 'YOUR_GOOGLE_SHEET_ID'  # ID from your Google Sheet URL
CREDENTIALS_PATH = 'path/to/your/credentials.json'  # Path to Google Service Account credentials

# TSM API Configuration
TSM_INSTALLATION_ID = 'YOUR_TSM_INSTALLATION_ID'  # Your TSM installation ID
TSM_TOKEN = 'YOUR_TSM_API_TOKEN'  # Your TSM API access token

# Installation Details
INSTALLATION_NAME = 'TESS001 - MachineName'  # Default installation name

# API Endpoints
BASE_URL = 'https://tsmapi.example.com/v2'  # Replace with actual TSM API base URL
ENDPOINTS = {
    'installations': '/users/installations',
    'stats': '/installations/{installation_id}/stats',
    'gps': '/installations/{installation_id}/gps'
}

# Data Collection Settings
HISTORICAL_DAYS = 180  # Number of days of historical data to collect
DATA_INTERVAL = 'days'  # Data collection interval (days, hours, etc.)

# Sheet Names
MAIN_SHEET_NAME = 'Sheet1'
GPS_SHEET_NAME = 'GPS_Data'

# Sheet Ranges
MAIN_SHEET_RANGE = 'A1:E1000'
GPS_SHEET_RANGE = 'A1:D1000'
