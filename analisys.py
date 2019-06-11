from filterpy.kalman import KalmanFilter
import pandas as pd
from utils.t import converted, beautify

def data_load(filename) :
  origin_data = pd.read_csv(filename, error_bad_lines=False) 
  reverse_data = origin_data.reindex(index=origin_data.index[::-1])  
  return reverse_data

'''
데이터 시작 시점
  BTC: 1506308400000 (2017년 09월 25일 12시 한국시간 기준)
'''

upbit_btc = data_load("data/upbit_BTC.csv")
upbit_btc_lastIdx = len(upbit_btc)  - 1

coinone_btc = data_load("data/coinone_BTC.csv")
coinone_btc = coinone_btc[coinone_btc.DT >=  1506308400000]
coinone_btc_lastIdx = len(coinone_btc) - 1

print(upbit_btc.head())
print(coinone_btc.head())

for idx in upbit_btc.index:
  upbit_price = upbit_btc.loc[upbit_btc_lastIdx]['tradePrice']
  coinone_price = coinone_btc.loc[coinone_btc_lastIdx]['Close']

  spread = upbit_price - coinone_price
  print(upbit_btc_lastIdx, spread)

  upbit_btc_lastIdx -= 1
  coinone_btc_lastIdx -= 1