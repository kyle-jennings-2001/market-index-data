import os
import glob
import pandas as pd
import yfinance as yf
from datetime import date



machine = 'Laptop'

if machine == 'Server' :
    folder_path = r'C:\Users\paulp\OneDrive - Taiga Group Holdings, LLC\Shared - Taiga Group Holdings\Bedrock by Taiga - Macroeconomic Screener\Data Files\Benchmark_Indices'

if machine == 'Laptop' :
    # folder_path = r'C:\Users\Kyle Jennings\OneDrive - Taiga Group Holdings, LLC\3.  Taiga Group Holdings, LLC\Shared - Taiga Group Holdings\Bedrock by Taiga - Macroeconomic Screener\Benchmark_Indices'
    folder_path = r'C:\Users\Kyle Jennings\OneDrive - Arcadian Holdings LLC\5.  Arcadian Financial\Vista_v0.05\GetEconomicData\Data Files\Benchmark_Indices'

if machine == 'Desktop' :
    folder_path = r'C:\Users\ktjje\OneDrive - Taiga Group Holdings, LLC\3.  Taiga Group Holdings, LLC\Shared - Taiga Group Holdings\Bedrock by Taiga - Macroeconomic Screener\Data Files\Benchmark_Indices'



# Use glob to get a list of all the files in the folder
file_list = glob.glob(os.path.join(folder_path, '*'))


# Loop through the file list
for file_name in file_list :

    df1 = pd.read_csv(file_name)

    # short_file_name is only the name of each file
    short_file_name = os.path.basename(file_name)

    # Get only the ticker name within the string, without '.csv'
    df2 = pd.DataFrame(yf.download(tickers=short_file_name[:-4], period='1d', interval='1d'))
    df2.drop(['Adj Close'], axis=1, inplace=True)
    df2.insert(0, 'Date', date.today())

    df2.to_csv(file_name, mode='a', header=False, index=False)

# Note that ^N225 has a funky timing standard that needs to be adjusted; see row 14924