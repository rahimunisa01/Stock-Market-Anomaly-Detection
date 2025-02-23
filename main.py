from data_ingestion import connection_kaggle, reading_dataset, load_data 
from features import features
from sentiment_analysis import sentiment_pipeline, compute_sentiment_for_dates
from anomaly_detection import anomalies
from dashboard import stock_plot, sentiment_plot
import pandas as pd
import matplotlib.pyplot as plt
import os
import plotly.express as px

def main():
    plot_dir = 'static/images'
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
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
    #add to website here as data frame
    
    #for visualisations
    stock_plot(data)
    # plt.savefig("stock_plot.png")
    stock_plot_path = os.path.join(plot_dir, "stock_plot.png")
    # fig.write_image(file_path)
    # plt.savefig(stock_plot_path)
    # plt.close()
    print("plot saved")

    # sentiment_plot(sentiment_data)
    # sentiment_plot_path = os.path.join(plot_dir, "sentiment_plot.png")
    # plt.savefig(sentiment_plot_path)
    # plt.close()
    return stock_plot_path, 7, data_df
    # return stock_plot_path, sentiment_plot_path, data_df
    # plt.savefig("sentiment_plot.png")

if '__main__':
    main()

