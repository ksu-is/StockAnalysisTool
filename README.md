# Stock Analysis Tool (Python)

## Overview

This project is a Python-based stock analysis tool designed to help users evaluate whether a company may be a worthwhile investment. By entering a stock ticker symbol, such as INTC, the program retrieves key historical financial data and applies simple analytical rules to generate a recommendation such as **Buy**, **Hold**, or **Avoid**. In addition to the recommendation, the tool explains the reasoning behind its evaluation and highlights potential risks, making it a practical decision-support system rather than a blind predictor.

---

## Who This Project Is For

* Students studying **finance, business, or data analytics**
* Beginner Python developers interested in real-world applications
* Individuals who may be curious about **stock market fundamentals**

---

## Features & Functionality

* Accepts user input for almost any stock ticker symbol excluding digital coins
* Retrieves real-time financial data using an API
* Analyzes key metrics, including:

  * Price-to-Earnings (P/E) Ratio
  * Revenue Growth
  * Debt-to-Equity Ratio
  * Profit Margins
* Evaluates company performance using simple decision logic
* Generates a clear recommendation for the ticker: **Buy, Hold, or Avoid**
* Provides explanations for each metric to help improve the understanding of the user
* Highlights potential risks associated with the stock
* (Optional extension) Analyzes recent stock price trends

---

## Similar Projects / Guides
https://www.youtube.com/watch?v=buLNFOvHK8o
https://github.com/LastAncientOne/SimpleStockAnalysisPython
https://github.com/venky14/Stock-Market-Analysis-and-Prediction
---

## Setup
1. pip install -r requirements.txt
2. Get an API key from console.anthropic.com
3. export ANTHROPIC_API_KEY="your-key-here"
4. python stock_analyzer.py

## Disclaimer

This tool is based on historical data taken from Yahoo Finance. You should always conduct your own research or consult a financial professional before investing.
