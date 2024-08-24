import pandas as pd
import numpy as np

def apply_trading_strategy(data):
    """
    Apply a more sophisticated trading strategy to historical price data.
    
    Parameters:
    data (pd.DataFrame): DataFrame containing historical price data.
    
    Returns:
    pd.DataFrame: DataFrame with trading signals and calculated indicators.
    """
    # Calculate short-term and long-term SMAs
    data['SMA_10'] = data['Close'].rolling(window=10).mean()
    data['SMA_30'] = data['Close'].rolling(window=30).mean()
    
    # Calculate Exponential Moving Average (EMA)
    data['EMA_12'] = data['Close'].ewm(span=12, adjust=False).mean()
    data['EMA_26'] = data['Close'].ewm(span=26, adjust=False).mean()
    
    # Calculate MACD and MACD Signal Line
    data['MACD'] = data['EMA_12'] - data['EMA_26']
    data['MACD_Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()
    
    # Generate trading signals
    data['Signal'] = 0
    data['Signal'][(data['SMA_10'] > data['SMA_30']) & (data['MACD'] > data['MACD_Signal'])] = 1  # Buy
    data['Signal'][(data['SMA_10'] <= data['SMA_30']) | (data['MACD'] < data['MACD_Signal'])] = -1  # Sell
    
    return data

def simulate_trades(data, futures_contract_size):
    """
    Simulate trades based on trading signals and calculate P&L for futures contracts.
    
    Parameters:
    data (pd.DataFrame): DataFrame with trading signals.
    futures_contract_size (float): Size of the futures contract.
    
    Returns:
    pd.DataFrame: DataFrame with simulated trades and P&L.
    """
    data['Position'] = data['Signal'].shift()
    data['Trade'] = data['Position'].diff()
    
    # Ensure Trade_P&L calculation is based on the next day's Close price
    data['Trade_P&L'] = data['Trade'] * data['Close'].shift(-1) * futures_contract_size
    
    # Forward fill for initial missing values
    data['Trade_P&L'] = data['Trade_P&L'].fillna(0)
    data['Daily P&L'] = data['Trade_P&L']
    data['Cumulative P&L'] = data['Daily P&L'].cumsum()
    
    return data
