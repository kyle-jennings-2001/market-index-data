# https://chatgpt.com/share/682b227d-0f34-8010-b5a4-c8fa95002c5a

import requests
import pandas as pd
from datetime import datetime, timedelta, date
import os

# User-configurable parameters
timing_parameter = 'Update' # Options: 'All' or 'Update'
file_type = 'csv' # Options: 'csv' or 'xlsx'
ticker_parameter = 'Indices.txt' # Options: 'Entry' or a .txt file name

# Get list of tickers
if ticker_parameter == 'Entry':
    tickers_input = input("Enter ticker symbols (separated by commas): ")
    tickers = [ticker.strip().upper() for ticker in tickers_input.split(',')]
else:
    # Read tickers from .txt file located in Index_Data subfolder
    script_dir = os.path.dirname(os.path.abspath(__file__))
    index_data_dir = os.path.join(script_dir, 'Index_Data')
    txt_file_path = os.path.join(index_data_dir, ticker_parameter)

    if not os.path.isfile(txt_file_path):
        raise FileNotFoundError(f"The file {ticker_parameter} was not found in the Index_Data folder.")

    with open(txt_file_path, 'r') as file:
        tickers = [line.strip().upper() for line in file if line.strip()]

if file_type not in ['csv', 'xlsx']:
    raise ValueError("Invalid file type. Please enter 'csv' or 'xlsx'.")

# API settings
API_KEY = '6fe8c4680cf2609b34c3674e0a32720b'
base_url = 'https://financialmodelingprep.com/api/v3/'
end_date = date.today()

# Ensure Index_Data folder exists
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, 'Index_Data')
os.makedirs(output_dir, exist_ok=True)

# Main logic based on timing_parameter
for ticker in tickers:
    output_file = os.path.join(output_dir, f"{ticker}.{file_type}")

    if timing_parameter == 'All':
        start_date = date(1900, 1, 1)
        existing_df = None
    elif timing_parameter == 'Update':
        # Check if file exists and get last available date
        if os.path.exists(output_file):
            if file_type == 'csv':
                existing_df = pd.read_csv(output_file, parse_dates=['date'])
            else:
                existing_df = pd.read_excel(output_file, parse_dates=['date'])

            if not existing_df.empty:
                last_date = existing_df['date'].max().date()
                start_date = last_date + timedelta(days=1)
            else:
                start_date = date(1900, 1, 1)
        else:
            existing_df = None
            start_date = date(1900, 1, 1)
        
        if start_date > end_date:
            print(f"No new data to fetch for {ticker}.")
            continue
    else:
        raise ValueError("Invalid timing_parameter. Choose 'All' or 'Update'.")

    params = {
        "from": start_date,
        "to": end_date,
        "apikey": API_KEY
    }

    data_url = f'{base_url}/historical-price-full/{ticker}'
    response = requests.get(data_url, params=params)
    if response.status_code != 200:
        print(f"Failed to retrieve data for {ticker}. Status code: {response.status_code}")
        continue

    data_result = response.json()
    if 'historical' not in data_result or not data_result['historical']:
        print(f"No historical data found for {ticker}.")
        continue

    new_data_df = pd.DataFrame(data_result['historical'])
    new_data_df.drop(columns=['label', 'change', 'changePercent', 'changeOverTime'], errors='ignore', inplace=True)
    new_data_df['date'] = pd.to_datetime(new_data_df['date'])

    if timing_parameter == 'Update' and existing_df is not None:
        combined_df = pd.concat([existing_df, new_data_df], ignore_index=True)
        combined_df.drop_duplicates(subset='date', keep='last', inplace=True)
    else:
        combined_df = new_data_df

    combined_df.sort_values('date', inplace=True)

    if file_type == 'csv':
        combined_df.to_csv(output_file, index=False)
    else:
        combined_df.to_excel(output_file, index=False)

    print(f"Data saved for {ticker}.")
