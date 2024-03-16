#!/usr/bin/env python
# coding: utf-8




import streamlit as st
import yfinance as yf
import pandas as pd

st.title("Stock analysis tool")

st.sidebar.header("Choose two stocks")

stock1 = st.sidebar.text_input("Enter stock ticker symbol-1 eg AAPL", value="AAPL")
stock2 = st.sidebar.text_input("Enter stock ticker symbol-2 eg MSFT", value="MSFT")

def load_data(stock):
    return yf.download(stock, period="3y")

data1 = load_data(stock1)
data2 = load_data(stock2)

# Check for missing data in both data1 and data2
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
    
correlation = data1['Adj Close'].corr(data2['Adj Close'])
st.write(f"Correlation between {stock1} and {stock2}: {correlation}")


st.sidebar.header("Ratios")
pe_ratio1=yf.Ticker(stock1).info.get('forwardPE',"no information in yahoo finance")
st.sidebar.write('PE ratio', stock1, pe_ratio1)

pe_ratio2=yf.Ticker(stock2).info.get('forwardPE', "no information in yahoo finance")
st.sidebar.write('PE ratio', stock2, pe_ratio2)

payoutratio1=yf.Ticker(stock1).info.get('payoutRatio',"no information in yahoo finance")
st.sidebar.write('Payout ratio', stock1, payoutratio1)
payoutratio2=yf.Ticker(stock2).info.get('payoutRatio',"no information in yahoo finance")
st.sidebar.write('Payout ratio', stock2, payoutratio2)

earningsQuarterlyGrowth1=yf.Ticker(stock1).info.get('earningsQuarterlyGrowth',"no information in yahoo finance")
st.sidebar.write('Earning Quarterly Growth', stock1, earningsQuarterlyGrowth1)
earningsQuarterlyGrowth2=yf.Ticker(stock2).info.get('earningsQuarterlyGrowth',"no information in yahoo finance")
st.sidebar.write('Earning Quarterly Growth', stock2, earningsQuarterlyGrowth2)

st.sidebar.header("Prices")
st.sidebar.write("Last price in yahoo finance for", stock1, data1['Adj Close'][-1])
st.sidebar.write("Last price in yahoo finance for", stock2, data2['Adj Close'][-1])
