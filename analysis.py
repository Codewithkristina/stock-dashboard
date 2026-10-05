import sqlite3
import pandas as pd

conn = sqlite3.connect("market.db")

def show(title, query):
    print(f"\n=== {title} ===")
    print(pd.read_sql_query(query, conn).to_string(index=False))

# 1. Which stock gained the most over the year?
show("1-Year Return", """
    SELECT p.ticker,
           ROUND((MAX(CASE WHEN p.date = d.last_date THEN p.close END) /
                  MAX(CASE WHEN p.date = d.first_date THEN p.close END) - 1) * 100, 2) AS return_pct
    FROM prices p
    JOIN (SELECT ticker, MIN(date) AS first_date, MAX(date) AS last_date
          FROM prices GROUP BY ticker) d ON p.ticker = d.ticker
    GROUP BY p.ticker
    ORDER BY return_pct DESC
""")

# 2. Best day, worst day, and how often each stock went up
show("Daily Moves", """
    WITH daily AS (
        SELECT ticker,
               (close / LAG(close) OVER (PARTITION BY ticker ORDER BY date) - 1) * 100 AS daily_pct
        FROM prices
    )
    SELECT ticker,
           ROUND(MAX(daily_pct), 2) AS best_day_pct,
           ROUND(MIN(daily_pct), 2) AS worst_day_pct,
           ROUND(SUM(daily_pct > 0) * 100.0 / COUNT(daily_pct), 1) AS up_days_pct
    FROM daily
    GROUP BY ticker
    ORDER BY best_day_pct DESC
""")

# 3. 20-day moving average for Apple (last 5 days)
show("AAPL 20-Day Moving Average", """
    SELECT date, ROUND(close, 2) AS close,
           ROUND(AVG(close) OVER (ORDER BY date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW), 2) AS ma_20
    FROM prices
    WHERE ticker = 'AAPL'
    ORDER BY date DESC
    LIMIT 5
""")

conn.close()