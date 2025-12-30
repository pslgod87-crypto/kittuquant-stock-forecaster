# backend.py — FINAL FIXED VERSION

import yfinance as yf
import pandas as pd
import numpy as np

def RSI(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def EMA(series, span):
    return series.ewm(span=span, adjust=False).mean()

def MACD(series, fast=12, slow=26, signal=9):
    ema_fast = EMA(series, fast)
    ema_slow = EMA(series, slow)
    macd_line = ema_fast - ema_slow
    signal_line = EMA(macd_line, signal)
    return macd_line, signal_line

def predict_stock(ticker, momentum_days=10):

    df = yf.download(ticker, period="1y", interval="1d")

    if df.empty:
        return None, "No Data"

    df = df[['Open','High','Low','Close','Volume']].copy()

    df['RSI'] = RSI(df['Close'])
    df['EMA20'] = EMA(df['Close'], 20)
    df['EMA50'] = EMA(df['Close'], 50)
    df['MACD'], df['MACD_signal'] = MACD(df['Close'])

    df = df.dropna().reset_index()   # remove NaN rows

    score = 0
    last = df.iloc[-1]

    if last['RSI'] < 30:
        score += 15
    elif last['RSI'] > 70:
        score -= 15

    if last['MACD'] > last['MACD_signal']:
        score += 10
    else:
        score -= 10

    if last['EMA20'] > last['EMA50']:
        score += 5
    else:
        score -= 5

    if score > 10:
        prediction = "Likely Up"
    elif score < -10:
        prediction = "Likely Down"
        prediction = "Likely Down"
    else:
        prediction = "Neutral"

    return df, prediction