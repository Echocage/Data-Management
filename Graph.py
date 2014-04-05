import sqlite3
import time

from pylab import *


con = sqlite3.connect('C:/data/FacebookOnlineData.db')
c = con.cursor()
DataList = []
times = []
nums = []
i = 0

for row in c.execute('SELECT * FROM CodeTable'):
#  if datetime.date.today() == datetime.date.fromtimestamp(row[0]):
    rTime = time.ctime(int(row[0])).split(' ')[3].split(':')
    nTime = float(rTime[0]) + float(rTime[1]) / 60.0 + float(rTime[2]) / 3600.0
    DataList.append([nTime, row[1]])


#Having the list sorted isn't useful in this particular plotting method,
#but it was helpful when experimenting with others.
DataList.sort(key=lambda x: x[0])

print DataList.__len__()
times = [x[0] for x in DataList]
nums = [x[1] if x[1] != 0 else None for x in DataList]
plt.ylim(0, max(nums))
plt.xlim(0, 24)
plt.plot(times, nums, 'go')
plt.show()








