import yfinance as yf
import streamlit as st
import plotly.graph_objects as go

# Configuration
symbol = "BTC-USD"  # You can change to "GC=F" for Gold
interval = "1h"     # You can use '1m', '5m', '15m', '1h', '1d'
period = "5d"       # Data period to fetch

def fetch_data():
    df = yf.download(symbol, period=period, interval=interval)
    df.dropna(inplace=True)
    return df

def draw_levels(df):
    resistance = df['High'].max()
    support = df['Low'].min()
    return float(support), float(resistance)

def detect_candle(df):
    last = df.iloc[[-1]]  # Ensure it stays as DataFrame
    open_price = float(last['Open'].iloc[0])
    close_price = float(last['Close'].iloc[0])
    if close_price > open_price:
        return "Bullish"
    elif close_price < open_price:
        return "Bearish"
    else:
        return "Neutral"

def generate_signal(candle_type, support, resistance, close):
    if candle_type == "Bullish" and abs(close - support) < 10:
        return "🔼 BUY"
    elif candle_type == "Bearish" and abs(close - resistance) < 10:
        return "🔽 SELL"
    else:
        return "📉 No Signal"

def main():
    st.set_page_config(page_title="Divesh Market Zone", layout="wide")
    st.title("📊 Divesh Market Zone - Live BTC/Gold Signal App")

    df = fetch_data()
    support, resistance = draw_levels(df)
    candle_type = detect_candle(df)
    close = float(df['Close'].iloc[-1])
    signal = generate_signal(candle_type, support, resistance, close)

    st.markdown(f"### 🪙 Asset: `{symbol}`")
    st.write(f"🟢 **Support**: `{support}`")
    st.write(f"🔴 **Resistance**: `{resistance}`")
    st.write(f"🕯️ **Candle Type**: `{candle_type}`")
    st.write(f"💰 **Last Close**: `{close}`")
    st.success(f"📣 **Signal**: {signal}")

    fig = go.Figure(data=[go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )])

    fig.add_hline(y=support, line_dash="dot", line_color="green")
    fig.add_hline(y=resistance, line_dash="dot", line_color="red")
    fig.update_layout(title="Live Candlestick Chart", xaxis_rangeslider_visible=False)

    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
