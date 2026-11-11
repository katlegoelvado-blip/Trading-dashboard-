from flask import Flask, jsonify
import pandas as pd
import yfinance as yf

app = Flask(__name__)

@app.route('/api/market-data', methods=['GET'])
def get_market_data():
    # Fetch live Gold (XAUUSD) market data using Yahoo Finance
    ticker = "GC=F"
    data = yf.download(ticker, period="5d", interval="1d")
    
    if data.empty:
        return jsonify({"error": "Failed to fetch market data"}), 500
        
    # Calculate SMA-3 value
    data['SMA_3'] = data['Close'].rolling(window=3).mean()
    
    latest_price = float(data['Close'].iloc[-1])
    latest_sma3 = float(data['SMA_3'].iloc[-1])
    
    return jsonify({
        "symbol": "XAUUSD",
        "price": latest_price,
        "SMA_3": latest_sma3
    })

if __name__ == '__main__':
    # Test print when executed directly via GitHub Actions
    ticker = "GC=F"
    data = yf.download(ticker, period="5d", interval="1d")
    if not data.empty:
        data['SMA_3'] = data['Close'].rolling(window=3).mean()
        print("--- Gold (XAUUSD) Cloud Runner Data ---")
        print(data[['Close', 'SMA_3']].tail(3))
