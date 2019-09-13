# 업비트 채결내용 가져오기

* sample

```
https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.KRW-BTC&count=2&to=2017-12-27%2005:10:00
```

```
https://crix-api-endpoint.upbit.com/v1/crix/candles/{봉기준}/{거리(기간})?code=CRIX.UPBIT.{마켓-코인티커}&count={갯수}&to={최종 데이터 시간}
```

봉기준: minutes, days, weeks, months

거리(기간): 1, 3, 5, 10, 15, 30, 60, 240(분)

마켓: KRW, BTC, ETH, USDT

코인티커: 코인종류(대문자)

갯수: 최종 데이터 시간을 기준으로 몇개를 요청할 지(최대: 400)

최종 데이터 시간: 0번째 인덱스의 시간(최신 데이터). 만약, 해당 값이 비면 가장 최신 데이터 시간을 기준으로 count만큼 가져온다. (2017-09-25T00:00:00.000Z의 형태로 작성되며 선택된 봉기준과 거리(기간)에 딱 떨어져야 함) timestamp는 딱 떨어지는 시간이 아니므로 다음과 같은 작업을 통해 전처리를 한다.

```python
int(timestamp / STEP) * STEP
```

STEP은 봉을 의미한다. 

days, 1이 선택됬으면 86400000이 된다.

소수점을 제외한 몫을 구한후 다시 step을 곱하여 필요없는 부분 제거

최종 데이터 시간은 응답 데이터의 마지막 인덱스 값의 timestamp를 사용하지만 **`None`** 일 경우 **`candleDateTime`** 을 timestamp로 변경하여 사용한다.

```python
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
```

# 코인원 채결내용 가져오기

* sample

```
https://tb.coinone.co.kr/api/v1/chart/olhc/?site=coinone&type=1m&last_time=1559949180000
```

```
https://tb.coinone.co.kr/api/v1/chart/olhc/?site=coinoneeth&type=1m&last_time=1559949180000
```


```
https://tb.coinone.co.kr/api/v1/chart/olhc/?site=coinone{코인티커}&type={거리(기간)}&last_time={최종 데이터 시간}
```

코인티커: 코인종류(소문자). btc의 경우 해당값을 비운다.

거리(기간): 1m, 1d => 1분 단위, 1일단위

최종 데이터 시간: 0번째 인덱스의 시간(최신 데이터). 만약, 해당 값이 비면 가장 최신 데이터 시간을 기준으로 가져온다. (기본값 200개)

코인원은 최종 데이터 시간(`DT`)가 딱 떨어지는 수치로 응답하기 때문에 따로 처리하지 않는다.