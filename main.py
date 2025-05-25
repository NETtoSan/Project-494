import streamlit
import pandas as pd


streamlit.title("AOT Stock visualizer")
streamlit.write("This is a simple stock visualizer app built with Streamlit using pandas, sklearn.")

# Load stock data
df = pd.read_csv("Stock-results.csv")

# Plot all numeric columns as line charts
numeric_cols = df.select_dtypes(include='number').columns
if not numeric_cols.empty:
    if 'วันที่' in df.columns:
        df_sorted = df.sort_values('วันที่')
        df_sorted = df_sorted.set_index('วันที่')
        streamlit.write("Line chart for price and linear trends")
        streamlit.line_chart(df_sorted[numeric_cols])
    else:
        streamlit.write("Column 'วันที่' not found. Showing default line chart.")
        streamlit.line_chart(df[numeric_cols])
else:
    streamlit.write("No numeric columns available for plotting.")

# Show dataframe
streamlit.write("Stock Data", df)