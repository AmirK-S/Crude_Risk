import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def generate_excel_report(data, filename):
    """
    Generate an Excel report of trading performance.
    
    Parameters:
    data (pd.DataFrame): DataFrame containing trading data.
    filename (str): Path to the output Excel file.
    """
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        data.to_excel(writer, sheet_name='Trading Data')
        worksheet = writer.sheets['Trading Data']
        worksheet.set_column('B:N', 12)  # Set column width for other columns

def generate_pdf_report(data, filename):
    """
    Generate a PDF report of trading performance.
    
    Parameters:
    data (pd.DataFrame): DataFrame containing trading data.
    filename (str): Path to the output PDF file.
    """
    with PdfPages(filename) as pdf:
        fig, ax = plt.subplots(figsize=(10, 6))
        data[['Close', 'SMA_10', 'SMA_30']].plot(ax=ax)
        ax.set_title('Price and Moving Averages')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.legend(['Close', 'SMA_10', 'SMA_30'])
        plt.xticks(rotation=45)
        pdf.savefig(fig)
        plt.close()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        data[['Daily P&L', 'Cumulative P&L']].plot(ax=ax)
        ax.set_title('Daily and Cumulative P&L')
        ax.set_xlabel('Date')
        ax.set_ylabel('P&L')
        ax.legend(['Daily P&L', 'Cumulative P&L'])
        plt.xticks(rotation=45)
        pdf.savefig(fig)
        plt.close()
