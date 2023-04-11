import time
from datetime import date


now1 = time.time
print (now1)
#1530192287.969666

now2 = time.gtime(time.time())
print (now2)
#time.strunct_time(tm_year=2020, tm_mon=7 ...)
now2.tm_year
#2020

date(2024, 1 ,23)
date.today()

