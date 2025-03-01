import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests
from datetime import datetime, timedelta
import json
from config import *  # Import configuration variables

def get_google_sheets_service():
    """Initialize Google Sheets service"""
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH, 
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    return build('sheets', 'v4', credentials=credentials)

def get_installation_name():
    """Get installation name from TSM API"""
    url = f"{BASE_URL}/users/installations"
    headers = {"x-authorization": f"Token {TSM_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        for installation in data.get('records', []):
            if installation.get('idSite') == TSM_INSTALLATION_ID:
                return installation.get('name', INSTALLATION_NAME)
        return INSTALLATION_NAME
    except Exception as e:
        print(f"Error getting installation name: {e}")
        return INSTALLATION_NAME

def get_historical_data():
    """Get historical battery data from TSM API"""
    url = f"{BASE_URL}/installations/{TSM_INSTALLATION_ID}/stats"
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=HISTORICAL_DAYS)
    
    params = {
        'type': 'custom',
        'interval': DATA_INTERVAL,
        'start': int(start_date.timestamp()),
        'end': int(end_date.timestamp()),
        'attributeCodes[]': [
            'Bc'    # Battery consumption
            # Add more attribute codes here for additional metrics
            # Example: 'gc' for generator consumption
            #         'Pc' for power consumption
            #         'Gc' for grid consumption
        ]
    }
    
    headers = {"x-authorization": f"Token {TSM_TOKEN}"}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def process_data(raw_data, installation_name):
    """Process raw data into structured format"""
    data_rows = [
        ['Date', 'Battery (kWh)', 'Installation Name']
        # Add more columns here as needed
        # Example: 'Generator (kWh)', 'Grid (kWh)', 'Total Used (kWh)'
    ]
    
    daily_data = {}
    
    # Process Battery data
    battery_data = raw_data.get('records', {}).get('Bc', [])
    if isinstance(battery_data, list):
        for entry in battery_data:
            if isinstance(entry, list) and len(entry) >= 2:
                timestamp = entry[0]
                value = entry[1]
                date = datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d')
                daily_data[date] = round(value, 2)

    # Convert dictionary to rows
    for date in sorted(daily_data.keys()):
        battery_value = daily_data[date]
        data_rows.append([
            date,
            battery_value if battery_value != 0 else '',
            INSTALLATION_NAME
        ])

    return data_rows

def write_to_sheet(service, data):
    """Write data to Google Sheet"""
    try:
        # Clear existing content
        service.spreadsheets().values().clear(
            spreadsheetId=SHEET_ID,
            range=MAIN_SHEET_RANGE
        ).execute()
        
        # Write new data
        body = {'values': data}
        service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range=f"{MAIN_SHEET_NAME}!A1",
            valueInputOption='RAW',
            body=body
        ).execute()
        print("Data written successfully")
    except Exception as e:
        print(f"Error writing to sheet: {e}")

def main():
    """Main execution function"""
    try:
        service = get_google_sheets_service()
        
        print("Getting installation name...")
        installation_name = get_installation_name()
        
        print("Getting historical data...")
        raw_data = get_historical_data()
        
        print("Processing data...")
        processed_data = process_data(raw_data, installation_name)
        
        print("Writing to Google Sheets...")
        write_to_sheet(service, processed_data)
        
        print("Data collection completed successfully")
        
    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    main()

"""
Note: This is a condensed version focusing on battery consumption.
To expand functionality:
1. Add more attribute codes in get_historical_data()
2. Add corresponding columns in process_data()
3. Modify data processing logic as needed
4. Update sheet range in write_to_sheet() if adding columns

Additional features that can be added:
- Generator consumption tracking
- Grid consumption tracking
- Total power consumption calculation
- GPS tracking
- Data validation
- Error handling and retries
- Logging
- Email notifications
"""
