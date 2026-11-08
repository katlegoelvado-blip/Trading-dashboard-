import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="SMA-3 Trading Dashboard", layout="wide")

st.title("📈 SMA-3 Trading Strategy Dashboard")
st.write("Clean signals, Moving Averages, and Risk Management.")

# Sidebar or Inputs for Ticker
ticker = st.text_input("Enter Stock/Crypto Ticker", value="AAPL").upper()

# Fetch data
data = yf.download(ticker, period="3mo", interval="1d")

if not data.empty:
    # Handle multi-index columns if returned by yfinance
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Calculate 3-Period SMA on 'Close' price
    data['SMA_3'] = data['Close'].rolling(window=3).mean()
    
    # Get current price and latest SMA-3
    current_price = float(data['Close'].iloc[-1])
    current_sma3 = float(data['SMA_3'].iloc[-1])
    
    st.subheader(f"📊 Analysis for {ticker}")
    
    # Display key metric cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"${current_price:.2f}")
    col2.metric("SMA-3 Value", f"${current_sma3:.2f}")
    
    # Simple Strategy Logic: Price vs SMA-3
    if current_price > current_sma3:
        signal = "🟢 BUY / BULLISH"
        # Set target and stop loss rules based on recent volatility/price
        stop_loss = current_price * 0.98  # 2% Risk
        take_profit = current_price * 1.04 # 4% Reward
    else:
        signal = "🔴 SELL / BEARISH"
        stop_loss = current_price * 1.02
        take_profit = current_price * 0.96

    col3.metric("Signal", signal)

    st.markdown("---")
    st.markdown("### 🎯 Trade Setup (SL & TP Targets)")
    
    # Clear structured box for Stop Loss and Take Profit
    st.info(f"""
    * **Action Recommended:** {signal}
    * **Entry Price:** ~${current_price:.2f}
    * **Stop Loss (ST):** ${stop_loss:.2f} *(Protect your capital here)*
    * **Take Profit (TP):** ${take_profit:.2f} *(Lock in your profits here)*
    """)

    st.markdown("---")
    st.subheader("📉 Recent Price & Moving Average Chart")
    st.line_chart(data[['Close', 'SMA_3']])

    with st.expander("View Raw Data Table"):
        st.dataframe(data.tail(10))

else:
    st.warning("Could not fetch data. Please check the ticker symbol.")
