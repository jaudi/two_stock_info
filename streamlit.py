#!/usr/bin/env python
# coding: utf-8




import pandas as pd
import yfinance as yf




import streamlit as st
import yfinance as yf
import pandas as pd

# Set the title of the Streamlit app
st.title("Stock Analysis Tool")

# Sidebar header for stock selection
st.sidebar.header("Choose two stocks")

# Input fields for stock tickers
stock1 = st.sidebar.text_input("Enter stock ticker symbol-1 (e.g., AAPL)", value="AAPL")
stock2 = st.sidebar.text_input("Enter stock ticker symbol-2 (e.g., MSFT)", value="MSFT")
# List of stock symbols
shares = [stock1, stock2]
# Function to load stock data
def load_data(stock):
    return yf.download(stock, period="1y")

# Load data for the selected stocks
data1 = load_data(stock1)
data2 = load_data(stock2)

# Check for missing data in both datasets
if data1.empty or data2.empty:
    st.error("No data available for the selected stocks.")
else:
    # Drop any NaN values in 'Adj Close' column
    data1.dropna(subset=['Adj Close'], inplace=True)
    data2.dropna(subset=['Adj Close'], inplace=True)

    # Display line chart for stock1
    st.subheader(f"Stock: {stock1}")
    st.line_chart(data1['Adj Close'], use_container_width=True)

    # Display line chart for stock2
    st.subheader(f"Stock: {stock2}")
    st.line_chart(data2['Adj Close'], use_container_width=True)
    
    # Calculate and display the correlation between the two stocks
    correlation = data1['Adj Close'].corr(data2['Adj Close'])
    st.write(f"Correlation between {stock1} and {stock2}: {correlation:.2f}")

# Sidebar headers for additional information
st.sidebar.header("Ratios")

# Function to retrieve stock info from Yahoo Finance
def get_stock_info(stock, info):
    return yf.Ticker(stock).info.get(info, "No information available in Yahoo Finance")

# Display PE ratio
pe_ratio1 = get_stock_info(stock1, 'forwardPE')
st.sidebar.write('PE Ratio', stock1, pe_ratio1)

pe_ratio2 = get_stock_info(stock2, 'forwardPE')
st.sidebar.write('PE Ratio', stock2, pe_ratio2)

# Display payout ratio
payout_ratio1 = get_stock_info(stock1, 'payoutRatio')
st.sidebar.write('Payout Ratio', stock1, payout_ratio1)

payout_ratio2 = get_stock_info(stock2, 'payoutRatio')
st.sidebar.write('Payout Ratio', stock2, payout_ratio2)

# Display earnings quarterly growth
earnings_growth1 = get_stock_info(stock1, 'earningsQuarterlyGrowth')
st.sidebar.write('Earnings Quarterly Growth', stock1, earnings_growth1)

earnings_growth2 = get_stock_info(stock2, 'earningsQuarterlyGrowth')
st.sidebar.write('Earnings Quarterly Growth', stock2, earnings_growth2)

# Sidebar header for prices
st.sidebar.header("Prices")

# Display the last price from the 'Adj Close' column
st.sidebar.write(f"Last price in Yahoo Finance for {stock1}: {data1['Adj Close'][-1]:.2f}")
st.sidebar.write(f"Last price in Yahoo Finance for {stock2}: {data2['Adj Close'][-1]:.2f}")


