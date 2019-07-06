from filterpy.kalman import KalmanFilter
import pandas as pd
from utils.t import converted, beautify
import os
import numpy as np
import matplotlib.pyplot as plt

COINTICKER = "BTC"

fileName = "data/analisyus_"+COINTICKER+"_6m11d.csv"
isExist = os.path.exists('{fileName}'.format(fileName=fileName))
F = open(fileName, 'a')

if not isExist:
    F.write('ts,ubit,coinone,spead\n',)


def data_load(filename) :
  origin_data = pd.read_csv(filename, error_bad_lines=False, low_memory=False )
  reverse_data = origin_data.reindex(index=origin_data.index[::-1] )  
  return reverse_data


def save(data):
  form = '{ts},{ubit},{coinone},{spead}\n'

  F.write(form.format(
    ts=data['ts'],
    ubit=data['ubit'],
    coinone=data['coinone'],
    spead=data['spead']
  ))


'''
  * 데이터 분석 기준: 업비트(upbit)
  * 데이터 시작 시점
    BTC: 1506308400000 (2017년 09월 25일 12시 한국시간 기준)
'''

upbit_btc = data_load("data/upbit_BTC_6M11D.csv")

upbit_btc = upbit_btc[upbit_btc.TimeStamp >= 1559343600000 ]
upbit_btc_lastIdx = len(upbit_btc)  - 1

coinone_btc = data_load("data/coinone_BTC.csv")
coinone_btc = coinone_btc[coinone_btc.DT >=  1559343600000]
coinone_btc_lastIdx = len(coinone_btc) - 1

print(upbit_btc)
print(coinone_btc)

loss_lastIdx = upbit_btc_lastIdx > coinone_btc_lastIdx and coinone_btc_lastIdx or upbit_btc_lastIdx

print('======================== start ===========================')

cnt = 0
msg_form = 'count: {cnt}, time: {ts}, upbitPrice: {upbit}, coinonePrice: {coinone}, spread: {spread}'

df_spread = {
  "timestamp": [],
  "spread": []
}

for idx in range(loss_lastIdx + 1):
  upbit_price = upbit_btc.loc[upbit_btc_lastIdx]['tradePrice']
  coinone_price = coinone_btc.loc[coinone_btc_lastIdx]['Close']

  spread = upbit_price - coinone_price
  df_spread["timestamp"].append(upbit_btc.loc[upbit_btc_lastIdx]['TimeStamp'])
  df_spread['spread'].append(spread)

  print(upbit_btc_lastIdx, msg_form.format(
    ts=upbit_btc.loc[upbit_btc_lastIdx]['candleDateTimeKst'], 
    spread=spread,
    upbit=upbit_price,
    coinone=coinone_price,
    cnt=cnt
  ))

  # save({
  #   "ts": upbit_btc.loc[upbit_btc_lastIdx]['candleDateTimeKst'], 
  #   "ubit": upbit_price,
  #   "coinone": coinone_price,
  #   "spead": spread
  # })

  upbit_btc_lastIdx -= 1
  coinone_btc_lastIdx -= 1
  cnt += 1

df = pd.DataFrame(df_spread)
# print(df)

# plt.figure(figsize=(15,8))
plt.plot(df.timestamp, df.spread)
plt.title('spread data chart')
plt.xlabel('time (s)')
plt.ylabel('spread')
# plt.axis([4, 25, 0, 250])
plt.grid(True)

plt.show()
  # if (cnt >100) : break