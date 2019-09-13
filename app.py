from crawler import upbit, bithumb, coinone
import argparse


parser = argparse.ArgumentParser(description='Exchange Crawler CLI Program.', prog="ECC")
parser.add_argument('--version', action='version', version='%(prog)s Version 1.0 ')


def p_s():
  '''
    upbit
    coinone
    bithumb
  '''

  parser.add_argument('--exchange', type=str, help="exchange      (default: upbit)")
  parser.add_argument('--market', type=str,   help="market        (default: KRW)")
  parser.add_argument('--ticker', type=str,   help="cointicker    (default: BTC)")

  parser.add_argument('--unit', type=str,     help="days, minutes (default: minutes)")
  parser.add_argument('--ped', type=int,      help="간격           (default: 5)")
  
  args = parser.parse_args()
  return args


def parse(a):
  exchanges = ['UPBIT', 'BITHUMB', 'COINONE']
  markets = ['KRW', 'BTC']
  tickers = ['BTC', 'ETH', 'EOS']
  units = ['days', 'minutes']
  peds = {
    'days': [1],
    'minutes': [1, 5, 10]
  }

  exchange = a.exchange and a.exchange.upper() or 'upbit'
  market = a.market and a.market.upper() or 'KRW'
  ticker = a.ticker and a.ticker.upper() or 'BTC'
  unit = a.unit and a.unit or 'minutes'
  ped = a.ped and a.ped or 5

  if not exchange in exchanges:
    exchange = 'upbit'

  if not market in markets:
    market = 'KRW'
  
  if not ticker in tickers:
    ticker = 'BTC'

  if not unit in units:
    unit = 'minutes'

  if not ped in peds[unit]:
    if unit == 'days'   : ped = 1
    if unit == 'minutes': ped = 5

  return {
    "exchange": exchange,
    "market": market,
    "ticker": ticker,
    "unit": unit,
    "ped": ped
  }

if __name__ == "__main__":
  global args
  
  args = p_s()
  args = parse(args)

  exchange = args['exchange']
  market = args['market']
  ticker = args['ticker']
  unit = args['unit']
  ped = args['ped']

  print(exchange)
  print(market)
  print(ticker)
  print(unit)
  print(ped)
  
  try :
    if exchange == 'UPBIT':
      upbit.start(market, ticker, unit, ped)
    elif exchange == 'BITHUMB':
      print('wait')
    elif exchange =='COINONE':
      print('wait')
  except KeyboardInterrupt:
    print('종료')
  # bithumb.start()
  # coinone.start()