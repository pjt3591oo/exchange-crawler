import requests as rq
import datetime
from utils.t import getToday, dayMinuteCalc, converted
from random import randint
from time import sleep
import json
import os

UNIT = "M"
PED = "10"
MARKET = "KRW"
COINTICKER = "BTC"
ENDTIME = ""
FROM=""
TO=""

BASE_URL = "https://www.bithumb.com/resources/chart/BTC_xcoinTrade_{ped}{unit}.json?symbol={cointicker}&resolution=0.5&from={fromm}&to={to}"

ONE_DAY_SEC = 86400000
ONE_MUNITE = 60000

def start(market, ticker, unit, ped):
  UNIT = "M"
  PED = "10"
  MARKET = "KRW"
  COINTICKER = "BTC"
  ENDTIME = ""
  FROM=""
  TO=""
  BASE_URL = "https://www.bithumb.com/resources/chart/BTC_xcoinTrade_{ped}{unit}.json?symbol={cointicker}&resolution=0.5&from={fromm}&to={to}"

  while True:
    url = BASE_URL.format(unit=UNIT, ped=PED, cointicker=COINTICKER, fromm=FROM, to=TO)
    print(url)
    res = rq.get(url)
    dataset = reversed(list(res.json()))
    
    # for data in dataset:
    #   print(data)
    ONE_DAY_SEC = len(res.json()) * 60 * 1000
    print('from    : ', res.json()[0])
    print('to      : ', res.json()[-1])
    print('length  : ', len(res.json()), res.json()[-1][0] - res.json()[0][0])
    
    TO=int(res.json()[0][0]) - 60 * int(PED) * 1000
    FROM=TO - ONE_DAY_SEC

    print(' from    : ', FROM)
    print(' to      : ', TO)
    print('=================')

    sleep(1)