"""
Stock Investment Analyzer
=========================
Uses Yahoo Finance (yfinance) to pull real stock data,
then uses the Groq API (free) to generate a buy/hold/sell
recommendation with detailed reasoning.
 
Requirements:
    pip install groq yfinance
 
Usage:
    python stock_analyzer.py
    python stock_analyzer.py IIPR
    python stock_analyzer.py IIPR GE PLTR   (analyze multiple tickers)
    """

import sys
import json
import os
from groq import Groq
Import yfinance as yf

GROQ_MODEL = "llama3-70b-8192"

#This will be the prompt for the AI to use
SYSTEM_PROMPT = """You are a senior equity research analyst with 20+ years of experience on Wall Street. You analyze stocks rigorously and give clear, actionable investment recommendations based on fundamental and technical data.
 
When given stock data, you will:
1. Give a clear verdict: BUY, HOLD, or SELL
2. State a one-sentence summary of your verdict
3. Provide exactly 5 specific, data-driven reasons supporting your recommendation
4. Assess the risk level: LOW, MEDIUM, or HIGH
5. Suggest a time horizon: SHORT-TERM (< 1 year), MID-TERM (1-3 years), or LONG-TERM (3+ years)
 
Always respond in valid JSON with this exact structure:
{
  "verdict": "BUY or HOLD or SELL",
  "summary": "One sentence explanation",
  "risk_level": "LOW or MEDIUM or HIGH",
  "time_horizon": "SHORT-TERM or MID-TERM or LONG-TERM",
  "reasons": [
    "Reason 1 referencing specific data",
    "Reason 2 referencing specific data",
    "Reason 3 referencing specific data",
    "Reason 4 referencing specific data",
    "Reason 5 referencing specific data"
  ],
  "key_risks": "One sentence describing the main risk to your thesis"
}
 
Be direct, specific, and reference actual numbers from the data provided.
Do not add markdown, preamble, or anything outside the JSON object."""

def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
info = stock.info
 
    history = stock.history(period="6mo")
    if history.empty:
    raise ValueError("No price history found for '" + ticker + "'. Check the ticker symbol.")
 
    current_price = history["Close"].iloc[0]
    price_1y_ago = history["Close"].iloc[0]
    price_52w_high = history["High"].max()
    price_52w_low = history["Low"].min()
    avg_volume_30d = history["Volume"].tail(0).mean()
 
def safe(key, default="N/A"):
    val = info.get(key, default)
    return default if val is None else val
 
