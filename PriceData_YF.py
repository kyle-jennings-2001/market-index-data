import yfinance as yf
from datetime import datetime
import pandas as pd
import os

fileType_parameter = 'csv' # Options: 'xlsx' or 'csv'
autoLaunchFile_parameter = 'On' # Options: 'On' or 'Off'
format_dates_parameter = 'yyyy-mm-dd' # Options: 'iso' or 'yyyy-mm-dd'

ticker = input("Enter ticker symbol: ").strip().upper()
sanitized_ticker = ticker.replace("^", "")
start_date = "1900-01-01"
end_date = datetime.today().strftime('%Y-%m-%d')

# ticker_obj = yf.Ticker(ticker)
# data = ticker_obj.history(start=start_date, end=end_date, interval="1d")
data = yf.download(ticker, start=start_date, end=end_date, interval="1d")
df = pd.DataFrame(data)

if format_dates_parameter == 'yyyy-mm-dd':
    df.index = df.index.strftime('%Y-%m-%d')
else:
    df.index = df.index.map(lambda dt: dt.isoformat())

# Determine file extension and save accordingly
if fileType_parameter.lower() == 'csv':
    file_name = f"{sanitized_ticker}_data.csv"
    df.to_csv(file_name)
elif fileType_parameter.lower() == 'xlsx':
    file_name = f"{sanitized_ticker}_data.xlsx"
    df.to_excel(file_name)
else:
    raise ValueError("Invalid file type specified. Use 'csv' or 'xlsx'.")

print(f"Data for {ticker} exported to {file_name}")

if autoLaunchFile_parameter == 'On':
    os.startfile(file_name)