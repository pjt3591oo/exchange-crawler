# exchange crawler

업비트, 코인원 크롤러 [문서 바로가기](./docs/crawler.md)

## 의존성 모듈 설치

```bash
$ pip install requirements.txt
```

## 설정파일

**`./config/*.py`**

* upbit

```python
MARKETS = ['krw', 'btc']
TICKERS = ['btc', 'eth', 'eos']
UNITS = { # d: day, m: minutes
  'd': 'days',
  'm': 'minutes'
} 
PEDS = {
  'd': [1],
  'm': [1, 5, 10]
}
```

* coinone

```python
MARKETS = ['krw']
TICKERS = ['btc', 'eth', 'eos']
UNITS = { # d: day, m: minutes
  'd': 'd',
  'm': 'm'
} 
PEDS = {
  'd': [1],
  'm': [1, 5, 10]
}
```

## 실행

```bash
$ python3 app.py --help

usage: ECC [-h] [--version] [--exchange EXCHANGE] [--market MARKET]
           [--ticker TICKER] [--unit UNIT] [--ped PED]

Exchange Crawler CLI Program.

optional arguments:
  -h, --help           show this help message and exit
  --version            show program's version number and exit
  --exchange EXCHANGE  upbit, coinone (default: upbit)
  --market MARKET      market (default: krw)
  --ticker TICKER      cointicker (default: btc)
  --unit UNIT          d(day), m(minutes) (default: m)
  --ped PED            간격 (default: 5)
```

> 결과 데이터는 **`./data/거래소_마켓_거래코인_거래간격.csv`** 형태로 저장

### upbit

- sample 1

```bash
$ python3 app.py --exchange upbit --market KRW --ticker ETH --unit m --ped 5
```

* 거래소: upbit
* 마켓: KRW(한화)
* 거래코인: ETH(이더리움)
* 거래간격: 5분

- sample 2

```
$ python3 app.py --exchange upbit --market BTC --ticker ETH --unit d --ped 1
```

* 거래소: upbit
* 마켓: BTC(비트코인)
* 거래코인: ETH(이오스)
* 거래간격: 1일

### coinone

- sample 1

```
$ python3 app.py --exchange coinone --market KRW --ticker ETH --unit m --ped 1
```

* 거래소: coinone
* 마켓: KRW(한화)
* 거래코인: ETH(이더리움)
* 거래간격: 1분

- sample 2

```
$ python3 app.py --exchange coinone --market KRW --ticker ETH --unit m --ped 5
```

* 거래소: coinone
* 마켓: KRW(한화)
* 거래코인: ETH(이더리움)
* 거래간격: 5분

- sample 3

```
$ python3 app.py --exchange coinone --market KRW --ticker ETH --unit d --ped 1
```

* 거래소: coinone
* 마켓: KRW(한화)
* 거래코인: ETH(이더리움)
* 거래간격: 1일