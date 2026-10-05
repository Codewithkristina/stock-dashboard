import sqlite3
import yfinance as yf

TICKERS = ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL"]

def fetch_data():
    conn = sqlite3.connect("market.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            ticker TEXT, date TEXT, open REAL, high REAL,
            low REAL, close REAL, volume INTEGER,
            PRIMARY KEY (ticker, date)
        )
    """)
    for ticker in TICKERS:
        df = yf.Ticker(ticker).history(period="1y")
        rows = [
            (ticker, d.strftime("%Y-%m-%d"), r.Open, r.High, r.Low, r.Close, int(r.Volume))
            for d, r in df.iterrows()
        ]
        conn.executemany("INSERT OR REPLACE INTO prices VALUES (?,?,?,?,?,?,?)", rows)
        print(f"{ticker}: saved {len(rows)} days")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    fetch_data()