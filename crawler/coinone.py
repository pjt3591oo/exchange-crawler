import requests as rq
import datetime
from utils.t import getToday, dayMinuteCalc, converted, beautify
from random import randint
from time import sleep
import json
import os

UNIT = "minutes" # days, minutes
PED = 5
MARKET = "KRW"
TICKER = "BTC"
COUNT = 400      # max: 400

STEP_BY_PED_OF_UNIT = {
  "d": {
    "1": 86400000
  }, 
  "m": {
    "1": 60000,
    "5": 300000,
    "10": 600000
  }
}

def save(filename, dataset):
  f = open(filename, 'a')

  form = '{DT},{Open},{Low},{High},{Close},{Volume},{Adj_Close}\n'
  for data in dataset:
    f.write(
      form.format(
        DT=data['DT'],
        Open=data['Open'],
        Low=data['Low'],
        High=data['High'],
        Close=data['Close'],
        Volume=data['Volume'],
        Adj_Close=data['Adj_Close']
      )
    )
  
  f.close()


def filecheck(MARKET, TICKER, UNIT, PED):
  filename = './data/%s_%s_%s_%s_%s.csv'%('coinone', MARKET, TICKER, UNIT, PED )
  isExist = os.path.exists('{filename}'.format(filename=filename))
  f = open(filename, 'a')
  
  if not isExist:
    f.write('DT,Open,Low,High,Close,Volume,Adj_Close\n',)

  f.close() 


def start(market, ticker, unit, ped):
  TO = ''
  UNIT = unit.lower()
  PED = ped
  TICKER = not ticker.lower() == 'btc'.strip() and  ticker.lower() or '' # ''는 btc, 코인원은 cointicker를 소문자로 처리함
  print(TICKER, TICKER == '')
  BASE_URL = "https://tb.coinone.co.kr/api/v1/chart/olhc/?site=coinone{ticker}&type={ped}{unit}&last_time={to}"
  
  filecheck(MARKET, ticker, UNIT, ped)
  while True:
    url = BASE_URL.format(to=TO, ticker=TICKER, ped=PED, unit=UNIT)
    print(url)
    res = rq.get(url)
    dataset = reversed(list(res.json()['data']))

    filename = './data/%s_%s_%s_%s_%s.csv'%('coinone', MARKET, TICKER, UNIT, PED )
    save(filename, dataset)

    print(url)
    print(beautify(res.json()['data'][-1]['DT']))
    print(beautify(res.json()['data'][0]['DT']))
    print(len(res.json()['data']))
    TO = int(res.json()['data'][0]['DT']) - STEP_BY_PED_OF_UNIT[UNIT][str(PED)]
    print('================***=================')
    sleep(1)

  

  