import pandas as pd
import numpy as np

def apply_trading_strategy(data):
    """
    Apply a trading strategy to historical price data.
    
    Parameters:
    data (pd.DataFrame): DataFrame containing historical price data.
    
    Returns:
    pd.DataFrame: DataFrame with trading signals and calculated SMAs.
    """
    # Calculate short-term and long-term SMAs
    data['SMA_10'] = data['Close'].rolling(window=10).mean()
    data['SMA_30'] = data['Close'].rolling(window=30).mean()
    
    # Generate trading signals: Buy (1), Sell (-1), Hold (0)
    data['Signal'] = 0
    data['Signal'][data['SMA_10'] > data['SMA_30']] = 1
    data['Signal'][data['SMA_10'] <= data['SMA_30']] = -1
    
    return data

def simulate_trades(data):
    """
    Simulate trades based on trading signals and calculate P&L.
    
    Parameters:
    data (pd.DataFrame): DataFrame with trading signals.
    
    Returns:
    pd.DataFrame: DataFrame with simulated trades and P&L.
    """
    data['Position'] = data['Signal'].shift()
    data['Trade'] = data['Position'].diff()
    
    # Ensure Trade_P&L calculation is based on the next day's Close price
    data['Trade_P&L'] = data['Trade'] * data['Close'].shift(-1)
    
    # Forward fill for initial missing values
    data['Trade_P&L'] = data['Trade_P&L'].fillna(0)
    data['Daily P&L'] = data['Trade_P&L']
    data['Cumulative P&L'] = data['Daily P&L'].cumsum()
    
    return data
