from data_ingestion import connection_kaggle, reading_dataset, load_data 
from features import features
from sentiment_analysis import sentiment_pipeline, compute_sentiment_for_dates
from anomaly_detection import anomalies
from dashboard import stock_plot, sentiment_plot
import pandas as pd
import matplotlib.pyplot as plt

def main():
    connection_kaggle()
    reading_dataset()
    data = load_data()
    data = features(data)
    data_df = data.dropna()
    sentiment_classifier = sentiment_pipeline()
    sentiment_data = compute_sentiment_for_dates(data, sentiment_classifier)
    sentiment_data.to_csv("daily_sentiment", index=False)
    # data = pd.merge(data, sentiment_data, on="Date", how="left")
    # print(data.head())
    data = anomalies(data)

    #for visualisations
    stock_plot(data)
    plt.savefig("stock_plot.png")
    print("plot saved")
    sentiment_plot(sentiment_data)
    plt.savefig("sentiment_plot.png")

if '__main__':
    main()

