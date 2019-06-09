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

갯수: 최종 데이터 시간을 기준으로 몇개를 요청할 지

최종 데이터 시간: 0번째 인덱스의 시간(최신 데이터). 만약, 해당 값이 비면 가장 최신 데이터 시간을 기준으로 count만큼 가져온다.

* start

```bash
$ python app.py
```

* config

`./crawler/upbit.py`에서 아래 코드를 수정하면 수집 데이터 종류, 주기를 변경할 수 있다.

```
UNIT = "minutes"
PED = 1
MARKET = "KRW"
COINTICKER = "EOS"
COUNT = 400
ENDTIME = ""
```

# 코인원 채결내용 가져오기

* sampl;e

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

거리(기간): 1m => 1분 단위

최종 데이터 시간: 0번째 인덱스의 시간(최신 데이터). 만약, 해당 값이 비면 가장 최신 데이터 시간을 기준으로 가져온다. (기본값 200개)

* config

`./crawler/coinone.py`에서 아래 코드를 수정하면 수집 데이터 종류, 주기를 변경할 수 있다.

```
UNIT = "m"
PED = 1
MARKET = "KRW"
COINTICKER = "EOS"
TO = ""
```