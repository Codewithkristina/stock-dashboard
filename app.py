import os
import sqlite3
import pandas as pd
import streamlit as st
import altair as alt
from fetch_data import fetch_data

st.set_page_config(page_title="Stock Dashboard", layout="wide")
st.title("📈 Stock Market Analytics Dashboard")

if not os.path.exists("market.db"):
    with st.spinner("Downloading market data..."):
        fetch_data()

conn = sqlite3.connect("market.db")

def load_prices(ticker, window):
    df = pd.read_sql_query(f"""
        SELECT date, close,
               AVG(close) OVER (ORDER BY date ROWS BETWEEN {window - 1} PRECEDING AND CURRENT ROW) AS moving_avg
        FROM prices
        WHERE ticker = ?
        ORDER BY date
    """, conn, params=(ticker,))
    df["date"] = pd.to_datetime(df["date"])
    return df

def price_chart(df, height=350):
    long = df.melt("date", var_name="line", value_name="price")
    return alt.Chart(long).mark_line().encode(
        x=alt.X("date:T", title=None),
        y=alt.Y("price:Q", scale=alt.Scale(zero=False), title="Price ($)"),
        color=alt.Color("line:N", title=None),
    ).properties(height=height)

def one_year_return(df):
    return (df["close"].iloc[-1] / df["close"].iloc[0] - 1) * 100

# Sidebar controls
tickers = pd.read_sql_query("SELECT DISTINCT ticker FROM prices ORDER BY ticker", conn)["ticker"].tolist()
ticker = st.sidebar.selectbox("Choose a stock", tickers)
window = st.sidebar.slider("Moving average (days)", 5, 100, 20)

# Selected stock, big view
df = load_prices(ticker, window)
col1, col2, col3 = st.columns(3)
col1.metric("Latest close", f"${df['close'].iloc[-1]:.2f}")
col2.metric("1-year return", f"{one_year_return(df):.2f}%")
col3.metric("Trading days", len(df))

st.subheader(f"{ticker} price vs. {window}-day moving average")
st.altair_chart(price_chart(df))

# Every stock, in a 2-column grid
st.subheader(f"All stocks: price vs. {window}-day moving average")
cols = st.columns(2)
returns = []
for i, t in enumerate(tickers):
    t_df = load_prices(t, window)
    r = one_year_return(t_df)
    returns.append({"ticker": t, "return_pct": r})
    with cols[i % 2]:
        st.markdown(f"**{t}** · 1-year return: {r:.2f}%")
        st.altair_chart(price_chart(t_df, height=250))

# Compare returns
st.subheader("1-year return: all stocks (%)")
st.bar_chart(pd.DataFrame(returns).set_index("ticker"))

conn.close()