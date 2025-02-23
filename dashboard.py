import matplotlib.pyplot as plt
import seaborn as sns

def stock_plot(data):
    plt.figure(figsize=(12,6))
    plt.plot(data['Date'], data['Close*'], label = 'Close Price', color = 'blue')
    anomalies = data[data['Anomaly']== -1]
    plt.scatter(anomalies['Date'], anomalies['Close*'], color = 'red', label = 'Anomaly')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('Market Anomaly Detection')
    plt.legend()
    plt.savefig("static\images\stock_plot.png")
    
    plt.show()

def sentiment_plot(data):
    plt.figure(figsize=(10,6))
    sns.kdeplot(data[data['Anomaly']==-1]['Daily_Return'].dropna(), label='Anomaly', shade=True)
    sns.kdeplot(data[data['Anomaly']==1]['Daily_Return'].dropna(), label='Normal', shade=True)
    plt.title("Distribution of Daily Returns: Anomaly vs Normal")
    plt.xlabel("Daily Return")
    plt.legend()
    plt.show()

def plot_correlation_heatmap(df):
    plt.figure(figsize=(10,8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.show()