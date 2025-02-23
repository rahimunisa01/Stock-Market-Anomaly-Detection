import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from dotenv import load_dotenv
from multiprocessing import Pool

# Import modules
from data_ingestion import connection_kaggle, reading_dataset, load_data
from features import features
from sentiment_analysis import SentimentAnalysis
from anomaly_detection import anomalies
from llama_api import generate_llama_response

# Load environment variables
load_dotenv()

def process_sentiment(date):
    """Fetch and analyze sentiment for a specific date."""
    sentiment_analyzer = SentimentAnalysis()
    headlines = sentiment_analyzer.fetch_market_news(date)
    sentiments = sentiment_analyzer.analyze_sentiment(headlines)

    return {
        "Date": date,
        "Headline": headlines[0] if headlines else "No News",
        "Sentiment": sentiments[0] if sentiments else "Neutral"
    }

def main():
    print("Starting Data Processing...")

    # Step 1: Data Ingestion
    connection_kaggle()
    reading_dataset()
    data = load_data()

    # Step 2: Feature Engineering
    data = features(data)
    data = data.dropna()

    # Fix column naming issue
    if "Close*" in data.columns:
        data.rename(columns={"Close*": "Close"}, inplace=True)

    # Step 3: Sentiment Analysis (Parallel Processing)
    print("Starting Sentiment Analysis...")
    dates = data["Date"].dt.strftime('%Y-%m-%d').tolist()

    with Pool(processes=4) as pool:
        sentiment_results = pool.map(process_sentiment, dates)

    sentiment_data = pd.DataFrame(sentiment_results)
    sentiment_data["Date"] = pd.to_datetime(sentiment_data["Date"])
    sentiment_mapping = {"Positive": 1, "Neutral": 0, "Negative": -1}
    sentiment_data["Sentiment_Score"] = sentiment_data["Sentiment"].map(sentiment_mapping)

    # Step 4: Merge Sentiment Data with Market Data
    data["Date"] = pd.to_datetime(data["Date"])
    sentiment_data["Date"] = pd.to_datetime(sentiment_data["Date"])
    data = pd.merge(data, sentiment_data, on="Date", how="left")

    # Step 5: Anomaly Detection
    print("Detecting Anomalies...")
    data = anomalies(data)

    # Step 6: Generate AI Insights
    print("Generating AI Insights...")
    insights = generate_llama_response(data)

    # Save Data for Streamlit
    data.to_csv("processed_data.csv", index=False)
    with open("insights.txt", "w") as file:
        file.write(insights)

    print("Pipeline Completed.")

if __name__ == "__main__":
    main()
