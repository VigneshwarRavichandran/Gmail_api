from datetime import datetime
from time import strptime

test = 'Mon, 10 Jun 2019 11:01:30 +0000 '
temp = test.split(', ')
date_string = temp[len(temp)-1]
date_arr = date_string.split(' ')
day = int(date_arr[0])
month = int(strptime(date_arr[1],'%b').tm_mon)
year = int(date_arr[2])
print(day, month, year)
print(datetime(year, month, day))
print(datetime.now())
# d = datetime.strptime(date, '%d %B %Y')
# print(d)