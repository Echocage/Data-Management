import sqlite3
import time
from matplotlib.dates import DateFormatter
from pylab import *


con = sqlite3.connect('C:/data/FacebookOnlineData.db')
c = con.cursor()
DataList = []
times = []
nums = []
i = 0

for row in c.execute('SELECT * FROM CodeTable'):
    now = datetime.date.today()
    t = datetime.datetime.fromtimestamp(row[0]).replace(year=now.year, day=now.day, month=now.month)
    DataList.append([t, row[1]])

plt.plot([x[0] for x in DataList], [x[1] for x in DataList], 'go')
formatter = DateFormatter('%H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
plt.show()








