import datetime

'''
 해당 패키지는 datetime 형으로 반환
'''

def getToday() :
  now = datetime.datetime.now()
  now = now.strftime('%Y-%m-%d %H:%M:00')
  return datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:00')

def converted(s) :
  s = s.replace('T', ' ').replace('+00:00', '')
  return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:00')


def dayMinuteCalc(date, delta) :
  return date + datetime.timedelta(minutes=delta)