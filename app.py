from crawler import upbit, bithumb,coinone
import argparse


parser = argparse.ArgumentParser(description='Exchange Crawler CLI Program.', prog="ECC")
parser.add_argument('--version', action='version', version='%(prog)s Version 1.0 ')

def p_s():
  
  parser.add_argument('--ticker', type=str, help="cointicker")
  parser.add_argument('--market', type=str, help="market")
  

  args = parser.parse_args()
  return args


if __name__ == "__main__":
  global args
  args = p_s()
  print(args)
  # upbit.start()
  # bithumb.start()
  # coinone.start()