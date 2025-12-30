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

    # Plot chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name="Close Price"))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA20'], name="EMA20"))
    fig.add_trace(go.Scatter(x=df.index, y=df['EMA50'], name="EMA50"))
    st.plotly_chart(fig, use_container_width=True)