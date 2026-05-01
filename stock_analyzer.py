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
 
    history = stock.history(period="1y")
    if history.empty:
        raise ValueError("No price history found for '" + ticker + "'. Check the ticker symbol.")
 
    current_price = history["Close"].iloc[-1]
    price_1y_ago = history["Close"].iloc[0]
    price_52w_high = history["High"].max()
    price_52w_low = history["Low"].min()
    avg_volume_30d = history["Volume"].tail(30).mean()
 
    def safe(key, default="N/A"):
        val = info.get(key, default)
        return default if val is None else val
 
return {
        "ticker": ticker.upper(),
        "company_name": safe("longName", ticker.upper()),
        "sector": safe("sector"),
        "industry": safe("industry"),
        "country": safe("country"),
        "current_price": round(current_price, 2),
        "52w_high": round(price_52w_high, 2),
        "52w_low": round(price_52w_low, 2),
        "price_1y_change": round(((current_price - price_1y_ago) / price_1y_ago) * 100, 2),
        "50d_avg": safe("fiftyDayAverage"),
        "200d_avg": safe("twoHundredDayAverage"),
        "market_cap": safe("marketCap"),
        "pe_ratio": safe("trailingPE"),
        "forward_pe": safe("forwardPE"),
        "peg_ratio": safe("pegRatio"),
        "price_to_book": safe("priceToBook"),
        "price_to_sales": safe("priceToSalesTrailing12Months"),
        "ev_to_ebitda": safe("enterpriseToEbitda"),
        "revenue_ttm": safe("totalRevenue"),
        "gross_margins": safe("grossMargins"),
        "operating_margins": safe("operatingMargins"),
        "profit_margins": safe("profitMargins"),
        "return_on_equity": safe("returnOnEquity"),
        "return_on_assets": safe("returnOnAssets"),
        "revenue_growth": safe("revenueGrowth"),
        "earnings_growth": safe("earningsGrowth"),
        "earnings_quarterly_growth": safe("earningsQuarterlyGrowth"),
        "total_cash": safe("totalCash"),
        "total_debt": safe("totalDebt"),
        "debt_to_equity": safe("debtToEquity"),
        "current_ratio": safe("currentRatio"),
        "free_cashflow": safe("freeCashflow"),
        "analyst_target_price": safe("targetMeanPrice"),
        "analyst_recommendation": safe("recommendationKey"),
        "analyst_count": safe("numberOfAnalystOpinions"),
        "beta": safe("beta"),
        "dividend_yield": safe("dividendYield"),
        "payout_ratio": safe("payoutRatio"),
        "avg_volume_30d": round(avg_volume_30d),
    }


def analyze_with_groq(stock_data):
    api_key = os.environ.get(GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY evironment variable not set. Please set it and try again.")

    client = Groq(api_key=api_key)

    user_message = "Please analize the following stock data and give me your investment recommendation:\n\n" + json.dumps(stock_data, indent=2, default=str)

    response = client.chat.completations.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.3,
        max_tokens=1024,
    )
 
    raw = response.choices[0].message.content.strip()
 
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
 
    return json.loads(raw)
 
 
COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "cyan": "\033[96m",
    "gray": "\033[90m",
    "white": "\033[97m",
}

VERDICT_COLOR = {"BUY": "green", "HOLD": "yellow", "SELL": "red"}
RISK_COLOR = {"LOW": "green", "MEDIUM": "yellow", "HIGH": "red"}
VERDICT_ICON = {"BUY": "▲", "SELL": "▼"}


def c(text, color):
    code = COLORS.get(color)

    if code is None:
        return str(text) + COLORS["reset"]
    return code + str(text)


def fmt_number(val):
    if val == "N/A" or val is None:
        return "N/A"
    try:
        n = float(val)
        if abs(n) >= 1_000_000_000:
            return "$" + str(round(n / 1_000_000_000, 2)) + "B"
        if abs(n) >= 1_000_000:
            return "$" + str(round(n / 1_000_000, 2)) + "M"
        return str(round(n, 2))
    except (ValueError, TypeError):
        return str(val)
 
 
def fmt_pct(val):
    if val == "N/A" or val is None:
        return "N/A"
    try:
        return str(round(float(val) * 100, 1)) + "%"
    except (ValueError, TypeError):
        return str(val)
 
 
def print_report(stock_data, analysis):
    ticker = stock_data["ticker"]
    name = stock_data["company_name"]
    verdict = analysis["verdict"]
    vcol = VERDICT_COLOR.get(verdict, "white")
    icon = VERDICT_ICON.get(verdict, "•")
    width = 60
    line = "-" * width
 
    print()
    print(c("=" * width, "cyan"))
    print(c("  " + ticker + "  -  " + name, "bold"))
    print(c("  " + str(stock_data["sector"]) + " · " + str(stock_data["industry"]), "gray"))
    print(c("=" * width, "cyan"))
    print()
