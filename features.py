import numpy as np
import pandas as pd
import ta

def features(data):
    if "Close*" in data.columns:
        data.rename(columns={"Close*": "Close"}, inplace=True)

    data['Daily_Return'] = data['Close'].pct_change()
    data['Log_Return'] = np.log(data['Close']/data['Close'].shift(1))
    data['MA_20'] = data['Close'].rolling(window=20).mean()
    data['Volatility_20'] = data['Daily_Return'].rolling(window=20).std()
    return data
