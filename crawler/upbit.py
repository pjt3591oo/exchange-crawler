import requests as rq
import json, time
import datetime
from random import *

import os

UNIT = "minutes" # days, minutes
PED = 5
MARKET = "KRW"
COINTICKER = "BTC"
COUNT = 400      # max: 400
ENDTIME = ""

STEP=0  # 1s => 1000ms

STEP_BY_PED_OF_UNIT = {
  "days": {
    "1": 86400000
  }, 
  "minutes": {
    "1": 60000,
    "5": 300000,
    "10": 600000
  }
}

BASEURL = {
  "days": "https://crix-api-cdn.upbit.com/v1/crix/candles/{uint}?code=CRIX.UPBIT.{market}-{cointicker}&count={count}&to={endtime}",   # days
  "minutes": "https://crix-api-cdn.upbit.com/v1/crix/candles/{uint}/{ped}?code=CRIX.UPBIT.{market}-{cointicker}&count={count}&to={endtime}"   # days
}

def getData(et):
  url = BASEURL[UNIT].format(uint=UNIT, ped=PED, market=MARKET, cointicker=COINTICKER, count=COUNT, endtime=ENDTIME)
  # print(url)
  res = rq.get(url)

  result = res.json()
  result_cnt = len(result)
  data= [{
      "code": item['code'],
      "openingPrice": item['openingPrice'],
      "highPrice": item['highPrice'],
      "lowPrice": item['lowPrice'],
      "tradePrice": item['tradePrice'],
      "candleAccTradeVolume": item['candleAccTradeVolume'],
      "candleAccTradePrice": item['candleAccTradePrice'],
      "candleDateTime": item["candleDateTime"],
      "timestamp": item["timestamp"] and item["timestamp"] or 0
    } for item in result if isinstance(item['timestamp'], int)]

  first = data[0]
  end = data[-1]

  '''
  code,openingPrice,highPrice,lowPrice,tradePrice,candleAccTradeVolume,candleAccTradePrice
  '''

  return {
    "first": first['timestamp'],
    "firstCandleDateTime": first["candleDateTime"],
    "end": end['timestamp'],
    "endCandleDateTime": end["candleDateTime"],
    "count": result_cnt,
    "data": data,
    "really_data_cnt": len(data)
  }

def start():
  STEP = STEP_BY_PED_OF_UNIT[UNIT][str(PED)]
  
  is_continue = True
  page = 1
  ENDTIME = ''

  while is_continue:
    result = getData(ENDTIME)
    print('latest : %s'%(result['firstCandleDateTime']))
    print('last   : %s'%(result['endCandleDateTime']))
    print('total count  : %s'%(result['count']))
    print('really  cnt  : %s'%(result['really_data_cnt']))
    
    for item in result['data']:
      filename = './data/%s_%s_%s_%s_%s.csv'%('upbit', MARKET, COINTICKER, UNIT, PED )
      file_save(filename, item)

    print('=========> %d page complete <========='%(page))
    is_continue = result['count'] < COUNT and False or True
    timestamp = result['end'] # - STEP
    
    timestamp = int(timestamp / STEP) * STEP # endtime이 분/시/일과 딱 떨어지지 않으면 요청에러 발생
    utc_timezone = datetime.timezone(datetime.timedelta(hours=0))

    ENDTIME = datetime.datetime.fromtimestamp(timestamp/1000, utc_timezone) # 2018-09-11 00:00:00+00:00
    ENDTIME = ENDTIME.isoformat()                                           # 2018-09-11T00:00:00+00:00
    ENDTIME = ENDTIME.replace('+00:00', '.000Z')                            # 2018-09-11T00:00:00.000Z
    
    page += 1

    time.sleep(uniform(0, 2))

def file_save(filename, data):
  '''
  code,openingPrice,highPrice,lowPrice,tradePrice,candleAccTradeVolume,candleAccTradePrice
  '''
  
  if not os.path.isfile(filename) :  
    f = open(filename, 'a')
    f.write('code,time,timestamp,openingPrice,highPrice,lowPrice,tradePrice,candleAccTradeVolume,candleAccTradePrice\n')
    f.close()

  f = open(filename, 'a')
  f.write(
    "%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(
      data["code"],
      data['candleDateTime'],
      data['timestamp'],
      data["openingPrice"],
      data["highPrice"],
      data["lowPrice"],
      data["tradePrice"],
      data["candleAccTradeVolume"],
      data["candleAccTradePrice"]
    )
  )

  f.close()