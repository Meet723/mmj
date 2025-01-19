import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

def calculate_rsi(data, window=14):
    """
    Calculate the Relative Strength Index (RSI) for a given DataFrame.
    """
    delta = data['Close'].diff()
    
    # Separate gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    
    # Calculate the average gain and average loss
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    
    # Calculate Relative Strength (RS)
    rs = avg_gain / avg_loss
    
    # Calculate RSI
    rsi = 100 - (100 / (1 + rs))
    
    data['RSI'] = rsi
    return data

# Streamlit app
st.title("Nifty Indices RSI Calculator")
st.write("This app calculates the Relative Strength Index (RSI) for selected Nifty indices.")

# List of Nifty indices
nifty_indices = {
    "Nifty 50": "^NSEI",
    "Nifty IT": "^CNXIT",
    "Nifty Pharma": "^CNXPHARMA",
    "Nifty Auto": "^CNXAUTO",
    "Nifty Metal": "^CNXMETAL",
    "Nifty Bank": "^BANKNIFTY",
}

# Sidebar options
st.sidebar.header("Select Options")
selected_indices = st.sidebar.multiselect("Select Nifty Indices", options=nifty_indices.keys(), default=list(nifty_indices.keys()))
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2022-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("2025-01-01"))

# Process data for selected indices
if st.sidebar.button("Calculate RSI"):
    st.write("Fetching data and calculating RSI...")
    all_data = {}
    for index in selected_indices:
        symbol = nifty_indices[index]
        try:
            # Fetch data
            data = yf.download(symbol, start=start_date, end=end_date)
            
            # Calculate RSI
            data = calculate_rsi(data)
            all_data[index] = data
            
            # Plot RSI
            fig = px.line(data, x=data.index, y="RSI", title=f"{index} RSI", labels={"x": "Date", "RSI": "RSI"})
            st.plotly_chart(fig)
        except Exception as e:
            st.error(f"Error fetching data for {index}: {e}")
    
    # Show raw data for each selected index
    for index, data in all_data.items():
        with st.expander(f"View Data for {index}"):
            st.write(data)
    
    st.success("RSI Calculation Completed!")

else:
    st.write("Use the sidebar to select indices and set date ranges, then click 'Calculate RSI'.")

