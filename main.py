import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
from sklearn.linear_model import LinearRegression
import numpy as np
import sys

# Load stock data
def read_stock(name):
    global end_date, start_date, hist, df
    try:
        stock = yf.Ticker(f"{name}.BK")
        end_date = datetime.datetime.today()
        start_date = end_date - datetime.timedelta(days=180)
        hist = yf.Ticker(f"{default_stock}.BK").history(start=start_date, end=end_date)

        # Save "Date" and "Close" columns from hist to a CSV file
        if not hist.empty:
            hist_reset = hist.reset_index()

            hist_reset['Date'] = pd.to_datetime(hist_reset['Date'])
            hist_reset = hist_reset.sort_values('Date')
            hist_reset['Date'] = hist_reset['Date'].dt.strftime('%y/%m/%d')

            # Calculate linear regression (trend) for 'Close'

            # Prepare data for regression
            X = np.arange(len(hist_reset)).reshape(-1, 1)
            y = hist_reset['Close'].to_numpy()
            model = LinearRegression()
            model.fit(X, y)
            trend = model.predict(X)
            hist_reset['Trend'] = trend

            # Calculate average price
            hist_reset['Avg_Close'] = hist_reset['Close'].expanding().mean()

            # Save to CSV
            hist_reset[['Date', 'Close', 'Trend', 'Avg_Close']].to_csv("Stock-results.csv", index=False)
            df = pd.read_csv("Stock-results.csv")
        return stock.info
        
    except:
        st.write(f"Error fetching stock from {name}!")

default_stock = "aot"
stock_info = read_stock(default_stock)

if stock_info is not None:
    st.title(f"{stock_info.get('longName', default_stock.upper())} (THB {stock_info.get('currentPrice', '')})")
else:
    st.title(f"Stock: {default_stock.upper()} (info unavailable)")

st.write("This is a simple stock visualizer app built with Streamlit using pandas, sklearn.")

# Initialize session state for toggles
for key in ("show_graph", "show_data", "show_history"):
    if key not in st.session_state:
        st.session_state[key] = False

col1, col2 = st.columns(2)
with col1:
    if st.button("Show/Hide Stock Graphs"):
        st.session_state.show_graph = not st.session_state.show_graph
with col2:
    if st.button("Show/Hide Stock Dataframe"):
        st.session_state.show_data = not st.session_state.show_data

if st.button("Show/Hide Stock History"):
    st.session_state.show_history = not st.session_state.show_history
    
# Show graphs
if st.session_state.show_graph:
    # Plot all numeric columns as line charts
    numeric_cols = df.select_dtypes(include='number').columns
    if not numeric_cols.empty:
        if 'Date' in df.columns:
            df_sorted = df.sort_values('Date')
            df_sorted = df_sorted.set_index('Date')
            st.write("Line chart for price and linear trends")
            st.line_chart(df_sorted[numeric_cols])
        else:
            st.write("Column 'Date' not found. Showing default line chart.")
            st.line_chart(df[numeric_cols])
    else:
        st.write("No numeric columns available for plotting.")

# Show dataframe
if st.session_state.show_data:
    if not hist.empty:
        hist_reset = hist.reset_index()
        st.write("Stock Price (Past 6 Months)")
        hist_reset['Date'] = pd.to_datetime(hist_reset['Date']).dt.strftime('%m %d %y')
        st.dataframe(hist_reset[['Date', 'Open', 'Close']])
    else:
        st.write("No historical price data available for the past 6 months.")
    #st.write("Stock Data", df)

# Show sidebar menu when stock history is toggled
if st.session_state.show_history:
    
    if stock_info:
        st.sidebar.header("Stock Details")
        st.sidebar.write(f"*{stock_info.get('longBusinessSummary', 'N/A')}*")
        st.sidebar.markdown("<br />", unsafe_allow_html=True)
        st.sidebar.write(f"**Owner:** {stock_info.get('companyOfficers', [{}])[0].get('name', 'N/A') if stock_info.get('companyOfficers') else 'N/A'}")
        st.sidebar.write(f"**Current Price:** {stock_info.get('currentPrice', 'N/A')}")
        st.sidebar.write(f"**Liquidity (Current Ratio):** {stock_info.get('currentRatio', 'N/A')}")
    else:
        st.sidebar.write("Stock information unavailable.")


