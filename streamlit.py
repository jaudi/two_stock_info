#!/usr/bin/env python
# coding: utf-8




import streamlit as st
import yfinance as yf
import pandas as pd

st.title("Stock Analysis Tool")

st.sidebar.header("Choose two stocks")

stock1 = st.sidebar.text_input("Enter stock ticker symbol-1 (e.g., AAPL)", value="AAPL")
stock2 = st.sidebar.text_input("Enter stock ticker symbol-2 (e.g., MSFT)", value="MSFT")

def load_data(stock, period="5y"):
    return yf.download(stock, period=period)

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

# New section for additional stock analysis over 5 years
st.header("Additional Stock Analysis (5 Years)")

# List of stock symbols
shares = [stock1, stock2]

for share in shares:
    data = load_data(share, period="5y")
    data = pd.DataFrame(data)

    # Calculate daily return
    data['daily_return'] = data['Close'].pct_change()
    
    # Select the Close and daily_return columns
    data_selected = data[['Close', 'daily_return']].copy()  # Create a copy to avoid the SettingWithCopyWarning
    
    # Calculate cumulative return
    data_selected['cumulative_return'] = (1 + data_selected['daily_return']).cumprod() - 1
    
    # Fill NaN values
    data_selected = data_selected.fillna(0)
    
    # Plot the cumulative return using Streamlit
    st.subheader(f"Cumulative Return of {share}")
    st.line_chart(data_selected['cumulative_return'], use_container_width=True)

    # Calculate the mean of 'Close' prices
    datamean = data['Close'].mean()
    
    # Function to categorize prices
    def categorize(price):
        if price > datamean:
            return "Over Mean"
        else:
            return "Under Mean"
    
    data['Category'] = data['Close'].apply(categorize)
    
    # Plot the bar chart for categories using Streamlit
    st.subheader(f"Days Above/Below Mean for {share}")
    st.bar_chart(data['Category'].value_counts(), use_container_width=True)
