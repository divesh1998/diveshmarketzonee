import streamlit as st import yfinance as yf import plotly.graph_objs as go import pandas as pd from io import StringIO import requests

Page setup

st.set_page_config(page_title="Divesh Market Zone", layout="wide") st.title("📈 Divesh Market Zone") st.markdown("Live BTC/Gold Chart + Signal + Support/Resistance + Elliott Wave + SL/TP + Export")

Select symbol

symbol = st.selectbox("📌 Select Asset", ["BTC-USD", "XAUUSD=X"], index=0)

Fetch data

df = yf.download(symbol, period="5d", interval="1h") df.dropna(inplace=True)

Support/Resistance

df["EMA50"] = df['Close'].ewm(span=50, adjust=False).mean() support = round(df['Low'].min(), 2) resistance = round(df['High'].max(), 2)

Latest data

open_price = df['Open'].iloc[-1] close_price = df['Close'].iloc[-1] candle_type = "Bullish" if close_price > open_price else "Bearish" trend = "Uptrend" if close_price > df["EMA50"].iloc[-1] else "Downtrend"

Signal logic

signal = "NO TRADE ZONE" if close_price > resistance: signal = "📈 BUY" elif close_price < support: signal = "📉 SELL"

SL & TP

if signal == "📈 BUY": sl = round(support, 2) tp = round(close_price + (close_price - support), 2) elif signal == "📉 SELL": sl = round(resistance, 2) tp = round(close_price - (resistance - close_price), 2) else: sl = tp = None

Display results

st.markdown(f"🟥 Resistance: {resistance}") st.markdown(f"🟩 Support: {support}") st.markdown(f"🕯️ Candle Type: {candle_type}") st.markdown(f"📊 Trend: {trend}") st.markdown(f"🚦 Signal: {signal}") if sl and tp: st.markdown(f"🛡️ Stop Loss: {sl}") st.markdown(f"🎯 Take Profit: {tp}")

Elliott Wave Input

wave1_high = st.number_input("📏 Wave 1 High Price", value=0.0) if wave1_high and close_price > wave1_high: st.success("🚀 Wave 3 Buy Signal Triggered!")

Plot candlestick chart

fig = go.Figure(data=[go.Candlestick( x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], increasing_line_color='green', decreasing_line_color='red' )]) fig.add_hline(y=support, line_dash="dot", line_color="green", annotation_text="Support", annotation_position="bottom right") fig.add_hline(y=resistance, line_dash="dot", line_color="red", annotation_text="Resistance", annotation_position="top right") fig.update_layout(xaxis_rangeslider_visible=False, height=500, margin=dict(l=10, r=10, t=30, b=10), template="plotly_dark") st.plotly_chart(fig, use_container_width=True)

Description box

description = st.text_area("📝 Write Your Analysis/Notes")

Chart upload

uploaded_image = st.file_uploader("📤 Upload Chart Image (Optional)", type=["png", "jpg", "jpeg"]) if uploaded_image: st.image(uploaded_image, caption="Uploaded Chart", use_column_width=True)

Telegram Send (Optional, requires setup)

def send_telegram(msg): token = "YOUR_BOT_TOKEN" chat_id = "YOUR_CHAT_ID" url = f"https://api.telegram.org/bot{token}/sendMessage" data = {"chat_id": chat_id, "text": msg} requests.post(url, data=data)

if st.button("📲 Send Signal to Telegram"): msg = f"Asset: {symbol}\nSignal: {signal}\nSupport: {support}\nResistance: {resistance}" send_telegram(msg) st.success("✅ Signal sent to Telegram!")

CSV Export

data = { "Asset": [symbol], "Support": [support], "Resistance": [resistance], "Trend": [trend], "Signal": [signal], "SL": [sl], "TP": [tp] } df_report = pd.DataFrame(data) st.download_button("📥 Download Report", df_report.to_csv(index=False), "report.csv", "text/csv")

