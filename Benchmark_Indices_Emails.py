import pandas as pd
import glob
import os
from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


machine = 'Desktop'

if machine == 'Server' :
    folder_path = r'C:\Users\paulp\OneDrive - Taiga Group Holdings, LLC\Shared - Taiga Group Holdings\Bedrock by Taiga - Macroeconomic Screener\Data Files\Benchmark_Indices'

if machine == 'Desktop' :
    # folder_path = r'C:\Users\ktjje\OneDrive - Taiga Group Holdings, LLC\3.  Taiga Group Holdings, LLC\Shared - Taiga Group Holdings\Bedrock by Taiga - Macroeconomic Screener\Data Files\Benchmark_Indices'
    folder_path = r'C:\Users\Kyle Jennings\OneDrive - Arcadian Holdings LLC\5.  Arcadian Financial\Vista_v0.05\GetEconomicData\Data Files\Benchmark_Indices'

# Use glob to get a list of all the files in the folder
file_list = glob.glob(os.path.join(folder_path, '*'))


# Define the function to calculate the 'Peak-Trough' column
def peak_trough(row) :
    try :

        if row['% Change'] < 0 :
            return (row['Low'] - row['High']) / row['High']
        else :
            return (row['High'] - row['Low']) / row['Low']
    
    except ZeroDivisionError:
        return "-"


list_LastRows = []


# Loop through the file list and get the daily % change for each index in the folder_path
for file_name in file_list :

    df1 = pd.read_csv(file_name)
    df1['% Change'] = df1['Close'].pct_change()
    df1['% Change'] = pd.to_numeric(df1['% Change'])
    
    # apply the function to each row of the dataframe
    df1['Peak-Trough'] = df1.apply(peak_trough, axis=1)

    list_LastRows.append(df1.tail(1))


df_LastRows = pd.concat(list_LastRows, ignore_index=True)

df_LastRows.drop(['Date'], axis=1, inplace=True)
df_LastRows.drop(['Volume'], axis=1, inplace=True)

df_LastRows['% Change'] = df_LastRows['% Change'].map(lambda x: '{:.2%}'.format(x))
df_LastRows['Peak-Trough'] = df_LastRows['Peak-Trough'].map(lambda x: '{:.2%}'.format(x))

df_LastRows['Open'] = df_LastRows['Open'].map(lambda x: '{:,.2f}'.format(x))
df_LastRows['High'] = df_LastRows['High'].map(lambda x: '{:,.2f}'.format(x))
df_LastRows['Low'] = df_LastRows['Low'].map(lambda x: '{:,.2f}'.format(x))
df_LastRows['Close'] = df_LastRows['Close'].map(lambda x: '{:,.2f}'.format(x))


indices = [
    'Dow Jones',
    'CAC 40',
    'FTSE 100',
    'DAX 40',
    'S&P 500',
    'TSX',
    'NASDAQ Composite',
    'Nikkei 225',
    'Russell 2000',
    'US10Y Yield',
    'VIX',
    ]    


regions = [
    'USA-Equities',
    'France-Equities',
    'UK-Equities',
    'Germany-Equities',
    'USA-Equities',
    'Canada-Equities',
    'USA-Equities',
    'Japan-Equities',
    'USA-Equities',
    'USA-Bonds',
    'USA-Derivatives'
    ]


df_LastRows.insert(0, 'Index', indices)
df_LastRows.insert(1, 'Description', regions)

NewRowOrder = [9, 10, 4, 6, 8, 0, 7, 3, 2, 1, 5]
NewColumnOrder = ['Index', 'Description', '% Change', 'Peak-Trough', 'Close', 'High', 'Low', 'Open']

df_LastRows = df_LastRows.reindex(NewRowOrder)
df_LastRows = df_LastRows.reindex(columns=NewColumnOrder)


html = df_LastRows.to_html(index=False)
smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
smtp_server.starttls()

userName = 'taigascript@gmail.com'
password = 'cbljjeypphdtehgj'

smtp_server.login(userName, password)

msg = MIMEMultipart()
msg['From'] = 'ktj.jennings@gmail.com'
msg['To'] = 'kylejennings@arcadianholdings.io'
msg['Subject'] = 'Markets Wrap: ' + str(date.today())
msg.attach(MIMEText(html, 'html'))

smtp_server.send_message(msg)

smtp_server.quit()


# from email.message import EmailMessage
# msg = EmailMessage()
# msg.set_content(MIMEText(html, 'html'))
# msg = MIMEText(finalOutput)
# msg = MIMEText(html, 'html')
# smtp_server.sendmail('ktj.jennings@gmail.com', 'kylej@taigagroup.io', msg.as_string())