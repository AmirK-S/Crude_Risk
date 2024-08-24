import yfinance as yf
import pandas as pd
import numpy as np
import os
from trading_strategy import apply_trading_strategy, simulate_trades
from report_generation import generate_excel_report, generate_pdf_report

def calculate_metrics(df):
    """
    Calculate additional quantitative metrics.
    
    Parameters:
    df (pd.DataFrame): DataFrame with trading signals and P&L.
    
    Returns:
    dict: Dictionary with calculated metrics.
    """
    metrics = {}
    
    # Sharpe Ratio
    daily_returns = df['Daily P&L'].dropna()
    annualized_return = daily_returns.mean() * 252
    annualized_volatility = daily_returns.std() * np.sqrt(252)
    sharpe_ratio = annualized_return / annualized_volatility
    metrics['Sharpe Ratio'] = sharpe_ratio
    
    # Maximum Drawdown
    df['Cumulative P&L'] = df['Daily P&L'].cumsum()
    df['Rolling Max'] = df['Cumulative P&L'].cummax()
    df['Drawdown'] = df['Cumulative P&L'] - df['Rolling Max']
    max_drawdown = df['Drawdown'].min()
    metrics['Maximum Drawdown'] = max_drawdown
    
    # Value at Risk (VaR)
    var_95 = df['Daily P&L'].quantile(0.05)
    metrics['Value at Risk (VaR) 95%'] = var_95
    
    # Expected Shortfall
    expected_shortfall = df['Daily P&L'][df['Daily P&L'] <= var_95].mean()
    metrics['Expected Shortfall'] = expected_shortfall
    
    # Additional Metrics
    metrics['Mean Daily P&L'] = daily_returns.mean()
    metrics['Volatility'] = daily_returns.std()
    
    return metrics

def markov_chain_analysis(df):
    """
    Perform Markov chain analysis on trading signals.
    
    Parameters:
    df (pd.DataFrame): DataFrame with trading signals.
    
    Returns:
    pd.DataFrame: Transition matrix of the Markov chain.
    """
    states = df['Signal'].dropna().astype(int).unique()
    transition_matrix = pd.DataFrame(index=states, columns=states).fillna(0)
    
    for (prev_state, next_state) in zip(df['Signal'][:-1], df['Signal'][1:]):
        if not pd.isna(prev_state) and not pd.isna(next_state):
            transition_matrix.loc[prev_state, next_state] += 1
    
    transition_matrix = transition_matrix.div(transition_matrix.sum(axis=1), axis=0)
    
    return transition_matrix

def get_next_filename_number(folder, base_name, extension):
    """
    Get the next available filename number in the specified folder.
    
    Parameters:
    folder (str): Path to the folder.
    base_name (str): Base name of the file.
    extension (str): File extension (e.g., '.xlsx').
    
    Returns:
    int: Next available file number.
    """
    existing_files = [f for f in os.listdir(folder) if f.startswith(base_name) and f.endswith(extension)]
    numbers = [int(f.split('_')[-1].replace(extension, '')) for f in existing_files]
    next_number = max(numbers, default=0) + 1
    return next_number

def main():
    symbol = 'CL=F'  # Futures symbol for Crude Oil
    start_date = '2020-02-20'
    end_date = '2024-02-20'
    futures_contract_size = 1000  # Example contract size for futures
    
    results_folder = 'Results'
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    # Download data
    df = yf.download(symbol, start=start_date, end=end_date)
    
    # Apply trading strategy
    df = apply_trading_strategy(df)
    
    # Simulate trades
    df = simulate_trades(df, futures_contract_size)
    
    # Calculate metrics
    metrics = calculate_metrics(df)
    print("Quantitative Metrics:")
    for key, value in metrics.items():
        print(f"{key}: {value:.2f}")

    # Markov chain analysis
    transition_matrix = markov_chain_analysis(df)
    print("\nMarkov Chain Transition Matrix:")
    print(transition_matrix)
    
    # Generate filenames
    excel_file_number = get_next_filename_number(results_folder, "P&L_Report", ".xlsx")
    pdf_file_number = get_next_filename_number(results_folder, "P&L_Report", ".pdf")
    
    excel_filename = os.path.join(results_folder, f"P&L_Report_{excel_file_number}.xlsx")
    pdf_filename = os.path.join(results_folder, f"P&L_Report_{pdf_file_number}.pdf")
    
    # Generate reports
    generate_excel_report(df, excel_filename, metrics)
    generate_pdf_report(df, pdf_filename, metrics, transition_matrix)

    print(f"\nExcel Report generated: {excel_filename}")
    print(f"PDF Report generated: {pdf_filename}")

if __name__ == "__main__":
    main()
