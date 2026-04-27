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
    python stock_analyzer.py AAPL
    python stock_analyzer.py IIPR GE PLTR   (analyze multiple tickers)
    """

import sys
import json
import os
from groq import Groq
Import yfinance as yf

GROQ_MODEL = "llama3-70b-8192"

#This will be the prompt for the AI to use
SYSTEM_PROMPT = """
