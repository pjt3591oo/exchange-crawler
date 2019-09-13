# exchange crawler

업비트, 코인원, 빗썸 크롤러 [문서 바로가기](./docs/crawler.md)

## 의존성 모듈 설치

```bash
$ pip install requirements.txt
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
  --exchange EXCHANGE  exchange (default: upbit)
  --market MARKET      market (default: KRW)
  --ticker TICKER      cointicker (default: BTC)
  --unit UNIT          days, minutes (default: minutes)
  --ped PED            간격 (default: 5)
```

- sample 1

```bash
$ python3 app.py --exchange upbit --market KRW --ticker ETH --unit minutes --ped 5
```

* 거래소: upbit
* 마켓: KRW(한화)
* 거래코인: ETH(이더리움)
* 거래간격: 5분

- sample 2

```
$ python3 app.py --exchange upbit --market BTC --ticker ETH --unit days --ped 1
```

* 거래소: upbit
* 마켓: BTC(비트코인)
* 거래코인: ETH(이오스)
* 거래간격: 1일