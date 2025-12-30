import yfinance as yf
import pandas as pd
import numpy as np

def predict_stock(ticker, momentum_days=10):
    df = yf.download(ticker, period="1y", interval="1d")

    if df is None or df.empty:
        return None, None

    # Use only numeric relevant fields
    df = df[['Open','High','Low','Close','Volume']].copy()

    # Technical indicators
    df['Returns'] = df['Close'].pct_change()
    df['Momentum'] = df['Close'].pct_change(momentum_days)
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()

    # Remove blank rows
    df = df.dropna().reset_index()

    last = df.iloc[-1]

    # Prediction score
    score = 0
    if last['Momentum'] > 0:
        score += 10
    else:
        score -= 10

    if last['EMA20'] > last['EMA50']:
        score += 5
    else:
        score -= 5

    if score > 5:
        prediction = "Likely Up"
    elif score < -5:
        prediction = "Likely Down"
    else:
        prediction = "Neutral"

    return df, prediction