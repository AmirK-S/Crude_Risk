# Quantitative Trading Strategy

## Overview

This project implements a quantitative trading strategy for futures markets using advanced technical indicators and trading signals. It integrates historical price data with complex trading metrics, including Value at Risk (VaR), Maximum Drawdown, and Markov Chain analysis. The strategy is designed to handle futures contracts and provides comprehensive performance reports.

## Features

- **Advanced Trading Strategy:** Utilizes Simple Moving Averages (SMA), Exponential Moving Averages (EMA), Moving Average Convergence Divergence (MACD), and MACD Signal Line to generate trading signals.
- **Futures Contracts Handling:** Simulates trading with futures contracts, taking into account contract size for accurate profit and loss calculations.
- **Quantitative Metrics:** Calculates key financial metrics including Sharpe Ratio, Maximum Drawdown, Value at Risk (VaR), and Expected Shortfall.
- **Markov Chain Analysis:** Analyzes trading signals using Markov Chain models to evaluate transition probabilities between different states.
- **Report Generation:** Generates detailed Excel and PDF reports summarizing trading performance and metrics.

## Requirements

- **Python 3.8+**
- **Libraries:**
  - `pandas`
  - `numpy`
  - `yfinance`
  - `openpyxl` (for Excel report generation)
  - `matplotlib` (for visualizations, if needed)
  - `reportlab` (for PDF report generation)

You can install the required libraries using pip:

```bash
pip install pandas numpy yfinance openpyxl matplotlib reportlab
```

## File Structure

- **`trading_strategy.py`**: Contains functions to apply the trading strategy, simulate trades, and handle futures contracts.
- **`analysis.py`**: Integrates trading strategy, calculates quantitative metrics, performs Markov Chain analysis, and generates reports.
- **`report_generation.py`**: Provides functions to generate Excel and PDF reports.
- **`data`**: Folder where historical price data is stored (if not using live data).

## Usage

### 1. Download Historical Data

The script `analysis.py` downloads historical price data for the specified futures contract using `yfinance`. Ensure you have internet access and the `yfinance` library installed.

### 2. Apply Trading Strategy

The trading strategy applies technical indicators to the historical price data, generating buy and sell signals based on moving averages and MACD.

### 3. Simulate Trades

The strategy simulates trades based on the generated signals, calculating profit and loss with respect to the futures contract size.

### 4. Analyze Performance

The analysis includes calculating key financial metrics, performing Markov Chain analysis on trading signals, and generating performance reports.

### 5. Generate Reports

The results are saved in both Excel and PDF formats, including details of trades, P&L, and quantitative metrics.

### Example Usage

To run the entire analysis and generate reports, execute:

```bash
python analysis.py
```

### Configuration

Modify the `symbol`, `start_date`, `end_date`, and `futures_contract_size` variables in `analysis.py` to customize the analysis for different futures contracts and date ranges.

## Example Output

- **Excel Report:** Contains a detailed spreadsheet with trading signals, trades, P&L, and performance metrics.
- **PDF Report:** A professional PDF summarizing the trading strategy, metrics, and visualizations.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please contact:

- **Author:** [Your Name]
- **Email:** [your.email@example.com]

---

Feel free to adjust the README based on specific details of your project or any additional features you might want to include.