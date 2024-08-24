import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

def generate_excel_report(df, filename, metrics):
    """
    Generate an Excel report with detailed trading performance and metrics.
    
    Parameters:
    df (pd.DataFrame): DataFrame with trading data and metrics.
    filename (str): Path to save the Excel file.
    metrics (dict): Dictionary containing calculated metrics.
    """
    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Trading Data', index=True)
        
        # Add a worksheet for metrics
        metrics_df = pd.DataFrame.from_dict(metrics, orient='index', columns=['Value'])
        metrics_df.to_excel(writer, sheet_name='Metrics', index=True)
        
        # Plot and save charts
        df[['Close', 'SMA_10', 'SMA_30']].plot(title='Price and Moving Averages')
        plt.savefig('SMA_Chart.png')
        plt.close()
        
        df[['MACD', 'MACD_Signal']].plot(title='MACD and Signal Line')
        plt.savefig('MACD_Chart.png')
        plt.close()
        
        workbook  = writer.book
        worksheet = workbook.add_worksheet('Charts')
        worksheet.insert_image('A1', 'SMA_Chart.png')
        worksheet.insert_image('A20', 'MACD_Chart.png')

def generate_pdf_report(df, filename, metrics, transition_matrix):
    """
    Generate a PDF report summarizing trading performance and Markov Chain analysis.
    
    Parameters:
    df (pd.DataFrame): DataFrame with trading data and metrics.
    filename (str): Path to save the PDF file.
    metrics (dict): Dictionary containing calculated metrics.
    transition_matrix (pd.DataFrame): Markov Chain transition matrix.
    """
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Trading Performance Report', 0, 1, 'C')
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Trading Metrics', 0, 1, 'L')
    pdf.set_font('Arial', '', 12)
    
    # Add metrics
    for key, value in metrics.items():
        pdf.cell(0, 10, f"{key}: {value:.2f}", 0, 1, 'L')
    
    # Add Markov Chain Analysis
    pdf.add_page()
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Markov Chain Analysis', 0, 1, 'L')
    
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, 'Transition Matrix:', 0, 1, 'L')
    
    for index, row in transition_matrix.iterrows():
        pdf.cell(0, 10, f"{index}: {row.to_dict()}", 0, 1, 'L')
    
    pdf.output(filename)
