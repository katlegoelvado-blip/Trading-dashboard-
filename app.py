import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="SMA-3 Trading Dashboard", layout="wide")

st.title("📈 SMA-3 Trading Strategy Dashboard")
st.write("Welcome to your mobile-friendly trading dashboard!")

ticker = st.text_input("Enter Stock/Crypto Ticker", value="AAPL")
data = yf.download(ticker, period="1mo", interval="1d")

if not data.empty:
    st.subheader(f"Recent Data for {ticker}")
    st.dataframe(data.tail())
else:
    st.warning("Could not fetch data. Please check the ticker symbol.")
