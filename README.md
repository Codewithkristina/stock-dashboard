# Stock Market Analytics Dashboard

Interactive dashboard analyzing one year of daily prices for 6 major stocks.

**Live demo:** [add link after deploying]

## What it does
- Downloads daily price data with yfinance and stores it in SQLite
- Analyzes returns, best/worst days, and moving averages using SQL window functions (LAG, AVG OVER)
- Interactive Streamlit dashboard with stock selector and adjustable moving average

## Finding
[Your insight, e.g.: AAPL rose on the most days (53%) but GOOGL had the highest return (40%), showing that the size of moves matters more than how often a stock goes up.]

## Run locally
pip install -r requirements.txt
python fetch_data.py
streamlit run app.py

## Limitations
- Data is a snapshot and does not update automatically yet
- Only 6 stocks
- For learning purposes, not financial advice