import requests
import pandas as pd
from datetime import datetime
import schedule
import time

# Function to fetch Nifty50 stock list
def fetch_nifty50_list():
    url = "https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)  # Fetch cookies
    response = session.get(url, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    stocks = data["data"]
    
    # Debug step
    print(stocks[0].keys())  # Print the available keys in the response
    
    # Adjust DataFrame creation based on available columns
    df = pd.DataFrame(stocks)
    required_columns = ['symbol', 'dayHigh', 'dayLow', 'lastPrice', 'change', 'pChange']
    df = df[required_columns]
    df.columns = ['Symbol', 'Day High', 'Day Low', 'Last Price', 'Change', 'PChange']
    return df

# Save DataFrame to CSV locally
def save_to_csv_locally(df, file_name):
    file_path = f"./{file_name}"
    df.to_csv(file_path, index=False)
    print(f"File {file_name} saved locally at {file_path}")
    return file_path

# Function to fetch, save, and update the stock data
def update_local_file():
    try:
        print("Fetching Nifty50 stock list...")
        nifty50_df = fetch_nifty50_list()
        
        print("Saving to CSV locally...")
        file_name = "nifty50_stocks.csv"
        save_to_csv_locally(nifty50_df, file_name)
    except Exception as e:
        print(f"An error occurred: {e}")

# Schedule the task every minute
schedule.every(1).minute.do(update_local_file)

# Run the scheduled task
print("Starting the Nifty50 stock updater...")
while True:
    schedule.run_pending()
    time.sleep(1)