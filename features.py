import numpy as np
import pandas as pd
import ta
def features(data):
    data['Daily_Return'] = data['Close*'].pct_change()
    data['Log_Return'] = np.log(data['Close*']/data['Close*'].shift(1))
    data['MA_20'] = data['Close*'].rolling(window=20).mean()
    data['Volatility_20'] = data['Daily_Return'].rolling(window=20).std()
    data['Intraday_Range'] = data['High'] - data['Low']
    data['DayOfWeek'] = data['Date'].dt.dayofweek
    data['Month'] = data['Date'].dt.month
    data['Quarter'] = data['Date'].dt.quarter
    data['RSI'] = ta.momentum.rsi(data['Close*'], window=14)
    data['MACD'] = ta.trend.macd(data['Close*'])
    data['MACD_Signal'] = ta.trend.macd_signal(data['Close*'])
    data['MACD_Diff'] = ta.trend.macd_diff(data['Close*'])
    
    bollinger = ta.volatility.BollingerBands(close=data['Close*'], window=20, window_dev=2)
    data['Bollinger_High'] = bollinger.bollinger_hband()
    data['Bollinger_Low'] = bollinger.bollinger_lband()
    data['Bollinger_Percent'] = bollinger.bollinger_pband()
    data['Bollinger_Width'] = bollinger.bollinger_wband()
    
    data['OBV'] = ta.volume.on_balance_volume(data['Close*'], data['Volume'])
    data['ADX'] = ta.trend.adx(high=data['High'], low=data['Low'], close=data['Close*'], window=14)
    return data

if "__main__":

    data = features