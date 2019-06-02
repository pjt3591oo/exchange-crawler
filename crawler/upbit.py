import requests as rq
import datetime
from utils.t import getToday, dayMinuteCalc, converted
from random import randint
from time import sleep
import json
import os

UNIT = "minutes"
PED = 1
MARKET = "KRW"
COINTICKER = "EOS"
COUNT = 400
ENDTIME = ""

BASEURL = "https://crix-api-endpoint.upbit.com/v1/crix/candles/{uint}/{ped}?code=CRIX.UPBIT.{market}-{cointicker}&count={count}&to={endtime}"

def url(uint, ped, market, cointicker, count, endtime) :
  return BASEURL.format(uint=uint, ped=ped, market=market, cointicker=cointicker, count=count, endtime=endtime)

def start() :
  u = url(UNIT, PED, MARKET, COINTICKER, COUNT, '')
  res = rq.get(u)
  save(res.json())
  endtime = res.json()[-1]["candleDateTime"]

  while len(res.json()):
    endtime = converted(endtime)
    endtime = str(endtime).replace(' ', '%20')
    u = url(UNIT, PED, MARKET, COINTICKER, COUNT, endtime)

    res = rq.get(u)

    endtime = res.json()[-1]["candleDateTime"]
    
    save(res.json())

  
def save(data) :
  fileName = "upbit"+COINTICKER+".csv"
  isExist = os.path.exists('{fileName}'.format(fileName=fileName))
  
  f = open(fileName, 'a')
  if not isExist:
    f.write('code,candleDateTime,candleDateTimeKst,openingPrice,highPrice,lowPrice,tradePrice,candleAccTradeVolume,candleAccTradePrice,timestamp,unit\n',)
  
  form = '{code},{candleDateTime},{candleDateTimeKst},{openingPrice},{highPrice},{lowPrice},{tradePrice},{candleAccTradeVolume},{candleAccTradePrice},{timestamp},{unit}\n'

  for item in data: 

    f.write(form.format(
      code=item['code'],
      candleDateTime=item['candleDateTime'],
      candleDateTimeKst=item['candleDateTimeKst'],
      openingPrice=item['openingPrice'],
      highPrice=item['highPrice'],
      lowPrice=item['lowPrice'],
      tradePrice=item['tradePrice'],
      candleAccTradeVolume=item['candleAccTradeVolume'],
      candleAccTradePrice=item['candleAccTradePrice'],
      timestamp=item['timestamp'],
      unit=item['unit'],
    ))
    
  f.close()
  
  print('start Date : ', data[0]["candleDateTime"])
  print('end Date   : ', data[-1]["candleDateTime"])

  sleep(randint(1,5))
