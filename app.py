import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Pro Trading Terminal", layout="wide")

# Initialize Session State for Virtual Wallet & Portfolio tracking
if "balance" not in st.session_state:
    st.session_state.balance = 10000.00  # Starting virtual capital ($10,000)
if "positions" not in st.session_state:
    st.session_state.positions = []      # Track active trades

st.title("⚡ Pro Trading Terminal & Wallet")
st.write("Live Market Signals, SMA-3 Strategy, Risk Management & Wallet Management.")

# --- SIDEBAR: WALLET & BANKING ---
st.sidebar.header("💳 Account Wallet")
st.sidebar.metric("Available Balance", f"${st.session_state.balance:,.2f}")

wallet_action = st.sidebar.selectbox("Banking Actions", ["View Wallet", "Deposit Funds", "Withdraw Funds"])

if wallet_action == "Deposit Funds":
    dep_amount = st.sidebar.number_input("Enter Deposit Amount ($)", min_value=10.0, max_value=50000.0, value=500.0, step=50.0)
    if st.sidebar.button("Confirm Deposit"):
        st.session_state.balance += dep_amount
        st.sidebar.success(f"Successfully deposited ${dep_amount:,.2f}!")

elif wallet_action == "Withdraw Funds":
    wit_amount = st.sidebar.number_input("Enter Withdrawal Amount ($)", min_value=10.0, max_value=st.session_state.balance, value=100.0, step=50.0)
    if st.sidebar.button("Confirm Withdrawal"):
        if wit_amount <= st.session_state.balance:
            st.session_state.balance -= wit_amount
            st.sidebar.success(f"Successfully withdrew ${wit_amount:,.2f}!")
        else:
            st.sidebar.error("Insufficient funds!")

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Asset Selector")

# Asset presets including Gold!
asset_options = {
    "Gold (GC=F)": "GC=F",
    "Bitcoin (BTC-USD)": "BTC-USD",
    "Apple (AAPL)": "AAPL",
    "EUR/USD (EURUSD=X)": "EURUSD=X",
    "Crude Oil (CL=F)": "CL=F"
}

selected_option = st.sidebar.selectbox("Choose Asset", list(asset_options.keys()))
ticker = asset_options[selected_option]

# Fetch data
data = yf.download(ticker, period="3mo", interval="1d")

if not data.empty:
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    # Calculate 3-Period SMA
    data['SMA_3'] = data['Close'].rolling(window=3).mean()
    
    current_price = float(data['Close'].iloc[-1])
    current_sma3 = float(data['SMA_3'].iloc[-1])
    
    st.subheader(f"📊 Market Analysis: {selected_option} ({ticker})")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"${current_price:,.2f}")
    col2.metric("SMA-3 Value", f"${current_sma3:,.2f}")
    
    # Strategy Logic
    if current_price > current_sma3:
        signal = "🟢 BUY / BULLISH"
        stop_loss = current_price * 0.98
        take_profit = current_price * 1.04
    else:
        signal = "🔴 SELL / BEARISH"
        stop_loss = current_price * 1.02
        take_profit = current_price * 0.96

    col3.metric("Signal", signal)

    st.markdown("---")
    st.markdown("### 🎯 Trade Setup & Execution")
    
    col_info, col_action = st.columns([2, 1])
    
    with col_info:
        st.info(f"""
        * **Recommended Action:** {signal}
        * **Entry Price:** ~${current_price:,.2f}
        * **Stop Loss (SL):** ${stop_loss:,.2f}
        * **Take Profit (TP):** ${take_profit:,.2f}
        """)
        
    with col_action:
        trade_shares = st.number_input("Units / Shares", min_value=0.1, max_value=100.0, value=1.0)
        total_cost = current_price * trade_shares
        
        if st.button("🚀 Execute Trade"):
            if st.session_state.balance >= total_cost:
                st.session_state.balance -= total_cost
                st.session_state.positions.append({
                    "Ticker": ticker,
                    "Action": signal,
                    "Shares": trade_shares,
                    "Entry": current_price,
                    "SL": stop_loss,
                    "TP": take_profit
                })
                st.success(f"Trade executed successfully for {trade_shares} units of {ticker}!")
            else:
                st.error("Not enough balance in wallet to execute this trade!")

    st.markdown("---")
    st.subheader("📋 Active Portfolio & Open Positions")
    if len(st.session_state.positions) > 0:
        pos_df = pd.DataFrame(st.session_state.positions)
        st.dataframe(pos_df, use_container_width=True)
    else:
        st.write("No active open positions yet. Execute a trade above to see it here!")

    st.markdown("---")
    st.subheader("📉 Price & Moving Average Chart")
    st.line_chart(data[['Close', 'SMA_3']])

else:
    st.warning("Could not fetch market data. Please try again.")
