import pandas as pd
import numpy as np
import time
import requests
from transformers import pipeline
from kaggleapi import SERPAPI_KEY  # Ensure SERPAPI_KEY is set in your config

def generate_business_dates(start="2023-01-01", end="2023-02-28"):
    """Generate a list of business dates between Jan 1 and Feb 28, 2023, in YYYY-MM-DD format."""
    business_dates = pd.date_range(start=start, end=end, freq='B')
    return [d.strftime("%Y-%m-%d") for d in business_dates]

def extract_headlines_from_response(data):
    headlines = []
    if "top_news" in data and isinstance(data["top_news"], dict):
        if "snippet" in data["top_news"]:
            headlines.append(data["top_news"]["snippet"])
    if "markets" in data and isinstance(data["markets"], dict):
        for region in data["markets"].values():
            if isinstance(region, list):
                for article in region:
                    if isinstance(article, dict) and article.get("name"):
                        headlines.append(article["name"])
    if "discover_more" in data and isinstance(data["discover_more"], list):
        for item in data["discover_more"]:
            items = item.get("items", [])
            if isinstance(items, list):
                for sub_item in items:
                    if isinstance(sub_item, dict) and sub_item.get("name"):
                        headlines.append(sub_item["name"])
    return headlines

def headlines_serpapi(date_str, query="finance"):
    params = {
        "engine": "google_finance",
        "q": f"{query} {date_str}",
        "api_key": SERPAPI_KEY,
        "hl": "en",
        "gl": "us",
    }
    response = requests.get("https://serpapi.com/search", params=params)
    try:
        data = response.json()
    except Exception as e:
        print("Error parsing JSON from SerpApi:", e)
        return []
    # Debug prints (optional)
    print(f"Status Code for {date_str}: {response.status_code}")
    print(f"Response Text for {date_str}: {response.text[:200]}")
    headlines = extract_headlines_from_response(data)
    return headlines

def sentiment_pipeline():
    sentiment_classifier = pipeline("sentiment-analysis", model="ProsusAI/finbert", device=0, framework='pt')
    return sentiment_classifier

def compute_sentiment_for_dates(sentiment_classifier, query="finance"):
    dates = generate_business_dates()  # Now only generates dates for Jan-Feb 2023
    sentiment_dict = {}
    for date_str in dates:
        headlines = headlines_serpapi(date_str, query=query)
        sentiments = []
        for headline in headlines:
            try:
                result = sentiment_classifier(headline)[0]
                if result['label'].lower() == "positive":
                    sentiments.append(result['score'])
                elif result['label'].lower() == "negative":
                    sentiments.append(-result['score'])
                else:
                    sentiments.append(0)
            except Exception as e:
                print(f"Error processing headline: {headline}\n{e}")
        if sentiments:
            sentiment_dict[date_str] = np.nanmean(sentiments)
        else:
            print(f"No headlines or sentiment scores for date {date_str}. Setting sentiment to 0.")
            sentiment_dict[date_str] = 0.0
        time.sleep(5)  # Delay to comply with rate limits
    sentiment_data = pd.DataFrame(list(sentiment_dict.items()), columns=['Date', 'Sentiment'])
    sentiment_data['Date'] = pd.to_datetime(sentiment_data['Date'], format="%Y-%m-%d")
    return sentiment_data
