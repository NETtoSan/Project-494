import streamlit
import pandas as pd


streamlit.title("Stock visualizer")
streamlit.write("This is a simple stock visualizer app built with Streamlit using pandas, sklearn.")

# Load stock data
df = pd.read_csv("Stock-results.csv")

# Plot all numeric columns as line charts
numeric_cols = df.select_dtypes(include='number').columns
if not numeric_cols.empty:
    streamlit.write("Line charts for all numeric columns:")
    streamlit.line_chart(df[numeric_cols])
else:
    streamlit.write("No numeric columns available for plotting.")

# Show dataframe
streamlit.write("Stock Data", df)

# Plot closing price if available
if 'Close' in df.columns:
    streamlit.line_chart(df['Close'])
else:
    streamlit.write("No 'Close' column found in the CSV.")