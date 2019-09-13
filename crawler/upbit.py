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
# ENDTIME = "2019-01-01T13:00:00.000Z"

STEP = 0  # 1s => 1000ms

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

def date_str_to_timestamp(d):
  '''
    응답데이터의 `candleDateTime`인 2019-09-12T01:20:00+00:00를 timestamp로 변경
    timestamp가 null값인 경우 해당 함수를 호출하여 candleDateTime를 timestamp로 변경하여 사용
  '''

  splits =d.split('T')
  yymmdd = splits[0]
  hhmmss = splits[1]

  splits_yymmdd = yymmdd.split('-')
  splits_hhmmss = hhmmss.split('+')[0].split(':')

  origin = "%s-%s-%s %s:%s:%s"%(splits_yymmdd[0], splits_yymmdd[1], splits_yymmdd[2], splits_hhmmss[0], splits_hhmmss[1], splits_hhmmss[2])

  return {
    "year": splits_yymmdd[0],
    "month": splits_yymmdd[1],
    "day": splits_yymmdd[2],
    "hour": splits_hhmmss[0],
    "minutes": splits_hhmmss[1],
    "second": splits_hhmmss[2],
    "origin": origin,
    "timestamp": int(time.mktime(datetime.datetime.strptime(origin, '%Y-%m-%d %H:%M:%S').timetuple()) * 1000)
  }

def getData(endtime):

  url = BASEURL[UNIT].format(uint=UNIT, ped=PED, market=MARKET, cointicker=COINTICKER, count=COUNT, endtime=endtime)
  print(url)
  res = rq.get(url)

  result = res.json()
  result_cnt = len(result)

  data= [
    {
      "code": item['code'],
      "openingPrice": item['openingPrice'],
      "highPrice": item['highPrice'],
      "lowPrice": item['lowPrice'],
      "tradePrice": item['tradePrice'],
      "candleAccTradeVolume": item['candleAccTradeVolume'],
      "candleAccTradePrice": item['candleAccTradePrice'],
      "candleDateTime": item["candleDateTime"],
      "timestamp": item['timestamp'] is None and date_str_to_timestamp(item['candleDateTime'])['timestamp'] or item["timestamp"]
    } for item in result 
  ]

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

def start(market, cointicker, unit, ped):
  global MARKET
  global COINTICKER
  global UNIT
  global PED

  MARKET = market.upper()
  COINTICKER = cointicker.upper()
  UNIT = unit
  PED = ped
  ENDTIME = ''

  STEP = STEP_BY_PED_OF_UNIT[UNIT][str(PED)]

  is_continue = True
  page = 1
  while is_continue:

    # print(ENDTIME)
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
    timestamp = result['end'] #- STEP

    timestamp = int(timestamp / STEP) * STEP # endtime이 분/시/일과 딱 떨어지지 않으면 요청에러 발생
    utc_timezone = datetime.timezone(datetime.timedelta(hours=0))

    ENDTIME = datetime.datetime.fromtimestamp(timestamp/1000, utc_timezone) # 2018-09-11 00:00:00+00:00
    ENDTIME = ENDTIME.isoformat()                                           # 2018-09-11T00:00:00+00:00
    ENDTIME = ENDTIME.replace('+00:00', '.000Z')                            # 2018-09-11T00:00:00.000Z

    page += 1

    time.sleep(uniform(0, 2))
