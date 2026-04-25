"""
Stock Investment Analyzer
=========================
Uses Yahoo Finance (yfinance) to pull real stock data,
then uses the Anthropic API to generate a buy/hold/sell
recommendation with detailed reasoning.
 
Requirements:
    pip install yfinance anthropic
 
Usage:
    python stock_analyzer.py
    python stock_analyzer.py AAPL
    python stock_analyzer.py IIPR GE PLTR   (analyze multiple tickers)
