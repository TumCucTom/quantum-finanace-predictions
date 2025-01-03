import pandas as pd
import numpy as np
import requests
import json
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime

# Load the API key from a JSON file
def load_api_key(file_path='API_KEY.json'):
    """Load API key from a JSON file."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data['API_KEY']

# Fetch the API key
API_KEY = load_api_key()

# Function to fetch stock data from Alpha Vantage API
def fetch_stock_data(symbol, interval='daily', outputsize='full'):
    """Fetch stock data from Alpha Vantage API."""
    url = f"https://www.alphavantage.co/query"
    params = {
        'function': 'TIME_SERIES_DAILY' if interval == 'daily' else 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '1d',  # 1 minute, 5 minutes, etc. for intraday
        'apikey': API_KEY,
        'outputsize': outputsize  # full or compact
    }
    response = requests.get(url, params=params)
    data = response.json()

    # Check if the request was successful and data is present
    if 'Time Series (Daily)' not in data:
        raise Exception(f"Error fetching data for {symbol}: {data.get('Note', 'Unknown error')}")

    # Convert the fetched data into a pandas DataFrame
    time_series = data[f'Time Series ({interval.capitalize()})']
    df = pd.DataFrame.from_dict(time_series, orient='index')

    # Convert the index to datetime format
    df.index = pd.to_datetime(df.index)

    # Rename columns to more convenient names
    df.columns = ['open', 'high', 'low', 'close', 'volume']

    # Convert column data to numeric
    df = df.astype({
        'open': 'float64',
        'high': 'float64',
        'low': 'float64',
        'close': 'float64',
        'volume': 'int64'
    })

    # Sort data by date (ascending)
    df = df.sort_index()

    return df

# Function to preprocess data (handling missing values, scaling, etc.)
def preprocess_data(df, scale=True):
    """Preprocess stock data (handle missing values and scale)."""

    # Handle missing data: drop rows with any missing values
    df = df.dropna()

    # Feature engineering: Extracting additional features if needed
    # For example: daily returns, moving averages, etc.
    df['daily_return'] = df['close'].pct_change()  # daily percentage change in closing price
    df['5_day_moving_avg'] = df['close'].rolling(window=5).mean()
    df['30_day_moving_avg'] = df['close'].rolling(window=30).mean()

    # Drop rows with NaN created by rolling calculations
    df = df.dropna()

    # Scaling data: Use MinMaxScaler to scale data (feature normalization)
    if scale:
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_columns = ['open', 'high', 'low', 'close', 'volume', 'daily_return', '5_day_moving_avg', '30_day_moving_avg']
        df[scaled_columns] = scaler.fit_transform(df[scaled_columns])

    return df

def get_stock(stock_symbol = 'AAPL'):
    # Example: Apple Inc.
    print(f"Fetching data for {stock_symbol}...")

    # Step 1: Fetch stock data from Alpha Vantage
    df = fetch_stock_data(stock_symbol)
    print(f"Data for {stock_symbol} fetched successfully.")

    # Step 2: Preprocess the data (clean and scale)
    df_preprocessed = preprocess_data(df)
    print(f"Data preprocessing complete.")

    # Step 3: Save preprocessed data to a CSV file (optional)
    df_preprocessed.to_csv(f'{stock_symbol}_preprocessed_data.csv')
    print(f"Preprocessed data saved to '{stock_symbol}_preprocessed_data.csv'.")

    # Optionally, you can print the first few rows of the preprocessed data
    print(df_preprocessed.head())

# Example usage:
if __name__ == '__main__':
    stock_symbol = 'AAPL'  # Example: Apple Inc.
    get_stock(stock_symbol)
