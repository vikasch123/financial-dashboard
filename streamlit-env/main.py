import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration with dark theme
st.set_page_config(page_title='Stock Market Dashboard', layout='wide', page_icon='📈')

# Custom CSS for modern UI
st.markdown("""
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background-color: #121212;
            color: white;
        }
        .metric-card {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar - Select Stock Symbol
st.sidebar.header("Stock Selection 🏦")
stock_options = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "NFLX", "META"]
stock_symbol = st.sidebar.selectbox("Select Stock Ticker", stock_options, index=0)

# Fetch stock data
def get_stock_data(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1y")
    return hist

data = get_stock_data(stock_symbol)

# Dashboard Title
st.title(f"📈 {stock_symbol} Stock Market Dashboard")

# Stock Price Metrics
latest_price = data["Close"].iloc[-1]
change = latest_price - data["Close"].iloc[-2]
percent_change = (change / data["Close"].iloc[-2]) * 100

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='metric-card'><h4>Latest Price (USD $)</h4><h2>{round(latest_price, 2)}</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='metric-card'><h4>Change (USD $)</h4><h2>{round(change, 2)}</h2></div>", unsafe_allow_html=True)
with col3:
    st.markdown(f"<div class='metric-card'><h4>% Change</h4><h2>{round(percent_change, 2)}%</h2></div>", unsafe_allow_html=True)

# Stock Price Chart with smooth animations
st.subheader("📊 Stock Price Movement")
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', line=dict(color='cyan', width=2)))
fig1.update_layout(title=f"{stock_symbol} Closing Price Trend", xaxis_title="Date", yaxis_title="Close Price (USD)", template="plotly_dark")
st.plotly_chart(fig1, use_container_width=True)

# Volume Chart
st.subheader("📉 Trading Volume")
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=data.index, y=data['Volume'], marker_color='lightblue'))
fig2.update_layout(title=f"{stock_symbol} Trading Volume", xaxis_title="Date", yaxis_title="Volume", template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)

# Footer
st.markdown("**Built with ❤️ using Streamlit & Yahoo Finance API**")
