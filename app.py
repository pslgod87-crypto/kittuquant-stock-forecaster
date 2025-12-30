# app.py — Streamlit UI

import streamlit as st
from backend import predict_stock
import plotly.graph_objects as go

st.set_page_config(page_title="Kittu Quant Stock Forecaster", layout="wide")
st.title("Kittu Quant Stock Forecaster")

ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA, SPY):", "AAPL")
momentum_days = st.number_input("Momentum Lookback Days:", min_value=5, max_value=30, value=10)

if st.button("Predict"):
    df, prediction = predict_stock(ticker, momentum_days)
    st.subheader(f"Prediction: {prediction}")

# Plot chart properly using Plotly
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name="Close Price"))
fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], mode='lines', name="EMA20"))
fig.add_trace(go.Scatter(x=df.index, y=df['EMA50'], mode='lines', name="EMA50"))

fig.update_layout(
    title=f"{ticker} Price and Moving Averages",
    xaxis_title="Date",
    yaxis_title="Price ($)",
    template="plotly_dark",  # matches your Wall-Street fintech theme
    autosize=True
)

st.plotly_chart(fig, use_container_width=True)