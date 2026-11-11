from flask import Flask, jsonify
import MetaTrader5 as mt5
import pandas as pd

app = Flask(__name__)

@app.route('/api/market-data', methods=['GET'])
def get_market_data():
    # 1. Initialize connection to MT5 terminal
    if not mt5.initialize():
        return jsonify({"success": False, "error": "MT5 initialization failed"}), 500

    symbol = "XAUUSD"
    mt5.symbol_select(symbol, True)

    # 2. Get current tick price
    tick = mt5.symbol_info_tick(symbol)
    current_price = tick.bid if tick else 0.0

    # 3. Fetch historical rates to calculate SMA-3
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_H1, 0, 10)
    if rates is not None:
        df = pd.DataFrame(rates)
        df['sma_3'] = df['close'].rolling(3).mean()
        sma_3_value = float(df['sma_3'].iloc[-1])
    else:
        sma_3_value = 0.0

    # 4. Determine a basic signal example
    signal = "SELL / BEARISH" if current_price < sma_3_value else "BUY / BULLISH"

    mt5.shutdown()

    # Return data formatted for your frontend terminal UI
    return jsonify({
        "success": True,
        "symbol": "Gold (XAUUSD)",
        "current_price": round(current_price, 2),
        "sma_3_value": round(sma_3_value, 2),
        "signal": signal
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
