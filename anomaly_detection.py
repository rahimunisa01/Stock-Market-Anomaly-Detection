import pandas as pd
from sklearn.ensemble import IsolationForest

def anomalies(data, features =['Daily_Return', 'Volatility_20'], contamination = 0.01):
    model_data = data[features].dropna()
    iso_model = IsolationForest(contamination=contamination, random_state=42)
    model_data['Anomaly'] = iso_model.fit_predict(model_data)
    data.loc[model_data.index, 'Anomaly'] = model_data['Anomaly']
    return data