from crawler import upbit, bithumb, coinone
import argparse
from config import upbit as config_upbit, bithumb as config_bithumb, coinone as config_coinone

parser = argparse.ArgumentParser(description='Exchange Crawler CLI Program.', prog="ECC")
parser.add_argument('--version', action='version', version='%(prog)s Version 1.0 ')

def p_s():
  '''
    upbit
    coinone
    bithumb
  '''

  parser.add_argument('--exchange', type=str, help="upbit, coinone     (default: upbit)")
  parser.add_argument('--market', type=str,   help="market             (default: krw)")
  parser.add_argument('--ticker', type=str,   help="cointicker         (default: btc)")

  parser.add_argument('--unit', type=str,     help="d(day), m(minutes) (default: m)")
  parser.add_argument('--ped', type=int,      help="간격                (default: 5)")
  
  args = parser.parse_args()
  return args


def parse(a):
  exchanges = ['upbit', 'coinone']
  exchange = a.exchange and a.exchange or 'upbit'
  
  exchange_config ={}

  if not exchange in exchanges or exchange == 'upbit':
    exchange = 'upbit'
    exchange_config = config_upbit
  else:
    exchange = 'coinone'
    exchange_config = config_coinone  
  
  MARKETS = exchange_config.MARKETS
  TICKERS = exchange_config.TICKERS
  UNITS = exchange_config.UNITS 
  PEDS = exchange_config.PEDS

  a.market = type(a.market) == type(None) and 'KRW' or a.market
  a.ticker = type(a.ticker) == type(None) and 'BTC' or a.ticker

  market = a.market.lower().strip() in MARKETS and a.market or 'krw'
  ticker = a.ticker.lower().strip() in TICKERS and a.ticker or 'btc'
  unit = a.unit in UNITS.get(a.unit, []) and UNITS[a.unit] or UNITS['m']
  ped = 1

  if not a.ped in PEDS.get(a.unit, []):
    if a.unit == 'm':
      ped = 5
    else:
      ped = 1

  return {
    "exchange": exchange.lower().strip(),
    "market": market.lower().strip(),
    "ticker": ticker.lower().strip(),
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
  
  usages_exchanges = ['upbit', 'coinone']

  try :
    if exchange == 'upbit':
      upbit.start(market, ticker, unit, ped)
    # elif exchange == 'BITHUMB':
    #   bithumb.start(market, ticker, unit, ped)
    elif exchange =='coinone':
      coinone.start(market, ticker, unit, ped)
  except KeyboardInterrupt:
    print('종료')