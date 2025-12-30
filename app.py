# app.py — Kittu Quant Stock Forecaster

import streamlit as st
from backend import predict_stock
import plotly.graph_objects as go

st.set_page_config(page_title="Kittu Quant Stock Forecaster", layout="wide")
st.title("Kittu Quant Stock Forecaster")
st.markdown("Enter a stock ticker (e.g., AAPL, TSLA, SPY) and momentum period. App predicts likely trend.")

ticker = st.text_input("Enter Stock Ticker:", "AAPL")
momentum_days = st.number_input("Momentum Lookback Days:", min_value=5, max_value=30, value=10)

if st.button("Predict"):
    try:
        df, prediction = predict_stock(ticker, momentum_days)
        st.subheader(f"Prediction: {prediction}")

        # Plot chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name="Close Price"))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['EMA20'], mode='lines', name="EMA20"))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['EMA50'], mode='lines', name="EMA50"))

        fig.update_layout(
            title=f"{ticker} Price and Moving Averages",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            template="plotly_dark",
            autosize=True
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")