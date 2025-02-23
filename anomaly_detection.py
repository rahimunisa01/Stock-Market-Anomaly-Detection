from numba import njit
import numpy as np
import pandas as pd

@njit
def detect_anomalies(data):
    median = np.median(data)
    std_dev = np.std(data)
    return np.abs(data - median) > 2 * std_dev

def anomalies(data):
    if "Daily_Return" not in data.columns:
        print("Error: 'Daily_Return' column not found.")
        return data
    
    anomaly_indices = detect_anomalies(data["Daily_Return"].to_numpy())
    data["Anomaly"] = anomaly_indices.astype(int)
    return data
