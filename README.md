# 업비트 채결내용 가져오기

* sample

```
https://crix-api-endpoint.upbit.com/v1/crix/candles/minutes/1?code=CRIX.UPBIT.KRW-BTC&count=2&to=2017-12-27%2005:10:00
```

```
https://crix-api-endpoint.upbit.com/v1/crix/candles/봉기준/거리(기간)?code=CRIX.UPBIT.마켓-코인티커&count=갯수&to=최종 데이터 시간
```

봉기준: minutes, days, weeks, months

거리(기간): 1, 3, 5, 10, 15, 30, 60, 240(분)

마켓: KRW, BTC, ETH, USDT

코인티커: 코인종류

갯수: 최종 데이터 시간을 기준으로 몇개를 요청할 지

최종 데이터 시간: 0번째 인덱스의 시간(최신 데이터). 만약, 해당 값이 비면 가장 최신 데이터 시간을 기준으로 count만큼 가져온다.

* start

```bash
$ python app.py
```