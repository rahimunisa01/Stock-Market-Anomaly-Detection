import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    """Load processed stock market and sentiment data."""
    try:
        data = pd.read_csv("processed_data.csv")
        data["Date"] = pd.to_datetime(data["Date"])
        return data
    except FileNotFoundError:
        return None

def load_insights():
    """Load AI-generated insights."""
    try:
        with open("insights.txt", "r") as file:
            return file.read()
    except FileNotFoundError:
        return "No insights available."

def display_dashboard():
    st.title("Stock Market & Sentiment Analysis Dashboard")

    data = load_data()
    insights = load_insights()

    if data is not None:
        st.write("### Stock Market Data")
        st.dataframe(data)

        st.write("### Stock Market Trends")
        fig, ax = plt.subplots()
        ax.plot(data["Date"], data["Close"], label="Stock Price", color="blue")
        ax.set_title("Stock Price Over Time")
        ax.legend()
        st.pyplot(fig)

        st.write("### Sentiment Analysis")
        fig, ax = plt.subplots()
        ax.plot(data["Date"], data["Sentiment_Score"], label="Sentiment Score", color="red")
        ax.set_title("Market Sentiment Over Time")
        ax.legend()
        st.pyplot(fig)

        st.write("### AI-Generated Insights")
        st.write(insights)
    else:
        st.write("No data available. Run the pipeline first.")

if __name__ == "__main__":
    display_dashboard()
