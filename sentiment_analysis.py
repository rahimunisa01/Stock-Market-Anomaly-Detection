import requests
import pandas as pd
from transformers import pipeline
from bs4 import BeautifulSoup
from time import sleep

class SentimentAnalysis:
    def __init__(self):
        print("Initializing Sentiment Analysis on CPU...")
        self.sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert", device=-1)
        self.news_cache = {}

    def fetch_market_news(self, date):
        if date in self.news_cache:
            return self.news_cache[date]

        try:
            url = "https://finance.yahoo.com/topic/stock-market-news/"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code != 200:
                return ["Error fetching market news"]

            soup = BeautifulSoup(response.text, "html.parser")
            headlines = [a.get_text(strip=True) for a in soup.select("h3 a")]

            if not headlines:
                return ["No market news available"]

            self.news_cache[date] = headlines[:5]
            sleep(1)
            return headlines[:5]

        except Exception:
            return ["Error fetching market news"]

    def analyze_sentiment(self, headlines):
        if not headlines or headlines[0] == "No market news available":
            return ["Neutral"]

        sentiment_results = [self.sentiment_pipeline(headline)[0]['label'] for headline in headlines]
        sentiment_mapping = {"positive": "Positive", "neutral": "Neutral", "negative": "Negative"}
        return [sentiment_mapping.get(sentiment.lower(), "Neutral") for sentiment in sentiment_results]
