import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Set the title of the Streamlit app
st.title('Stock Index and Company Performance')

# Sidebar selection menu
st.sidebar.title('Select Stock')
selection = st.sidebar.selectbox('Choose an index or company:', [
    'S&P 500 (^GSPC)',
    'Dow Jones (^DJI)',
    'NASDAQ (^IXIC)',
    'Apple (AAPL)',
    'Microsoft (MSFT)',
    'Amazon (AMZN)',
    'Google (GOOGL)',
    'Tesla (TSLA)'
])

# Dictionary to map selection to ticker symbol
ticker_dict = {
    'S&P 500 (^GSPC)': '^GSPC',
    'Dow Jones (^DJI)': '^DJI',
    'NASDAQ (^IXIC)': '^IXIC',
    'Apple (AAPL)': 'AAPL',
    'Microsoft (MSFT)': 'MSFT',
    'Amazon (AMZN)': 'AMZN',
    'Google (GOOGL)': 'GOOGL',
    'Tesla (TSLA)': 'TSLA'
}

# Get the ticker symbol based on the selection
ticker = ticker_dict[selection]

# Get today's date and the date one year ago
end_date = pd.Timestamp.today().normalize()
start_date = end_date - pd.DateOffset(years=1)

# Fetch the historical data for the selected stock/index
stock_data = yf.download(ticker, start=start_date, end=end_date)

# Display line chart or candlestick chart based on user selection
chart_type = st.sidebar.radio('Chart Type', ['Line Chart', 'Candlestick Chart'])

if chart_type == 'Line Chart':
    # Get the width of time from the user
    chart_width_years = st.sidebar.slider("Chart Width (Years)", min_value=1, max_value=10, value=1, step=1)

    # Calculate the start date based on the width of time
    start_date = end_date - pd.DateOffset(years=chart_width_years)

    # Fetch data for the adjusted time period
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    # Get the height from the user
    line_chart_height = st.sidebar.slider("Line Chart Height", min_value=200, max_value=800, value=400, step=50)

    # Plot the closing price of the selected stock/index
    st.subheader(f'Line Chart for {selection}')
    st.line_chart(stock_data['Close'], use_container_width=True, height=line_chart_height)
elif chart_type == 'Candlestick Chart':
    # Get the width of time from the user
    chart_width_years = st.sidebar.slider("Chart Width (Years)", min_value=1, max_value=10, value=1, step=1)

    # Calculate the start date based on the width of time
    start_date = end_date - pd.DateOffset(years=chart_width_years)

    # Fetch data for the adjusted time period
    stock_data = yf.download(ticker, start=start_date, end=end_date)

    # Plot the candlestick chart
    fig = go.Figure(data=[go.Candlestick(
        x=stock_data.index,
        open=stock_data['Open'],
        high=stock_data['High'],
        low=stock_data['Low'],
        close=stock_data['Close']
    )])

    # Update layout for better visualization
    fig.update_layout(
        #title='Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )

    st.subheader(f'Candlestick Chart for {selection}')
    st.plotly_chart(fig, use_container_width=True)

