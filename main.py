import streamlit
import pandas as pd
import yfinance as yf



# Load stock data
df = pd.read_csv("Stock-results.csv")
default_stock = "aot"

def read_stock(name):
    try:
        stock = yf.Ticker(f"{name}.BK")
        return stock.info.get('longName', 'Unknown stock!')
    except:
        streamlit.write(f"Error fetching stock from {name}!")

streamlit.title(read_stock(default_stock))
streamlit.write("This is a simple stock visualizer app built with Streamlit using pandas, sklearn.")

# Add a button to show/hide the stock graphs using session_state
if "show_graph" not in streamlit.session_state:
    streamlit.session_state.show_graph = False

if streamlit.button("Show/Hide Stock Graphs"):
    streamlit.session_state.show_graph = not streamlit.session_state.show_graph

if streamlit.session_state.show_graph:
    # Plot all numeric columns as line charts
    numeric_cols = df.select_dtypes(include='number').columns
    if not numeric_cols.empty:
        if 'Date' in df.columns:
            df_sorted = df.sort_values('Date')
            df_sorted = df_sorted.set_index('Date')
            streamlit.write("Line chart for price and linear trends")
            streamlit.line_chart(df_sorted[numeric_cols])
        else:
            streamlit.write("Column 'Date' not found. Showing default line chart.")
            streamlit.line_chart(df[numeric_cols])
    else:
        streamlit.write("No numeric columns available for plotting.")

# Show dataframe
streamlit.write("Stock Data", df)
