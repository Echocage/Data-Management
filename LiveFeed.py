import sqlite3
import time
import time as usertime
import os
from pylab import *


def extractTime(fTime):
    rTime = time.ctime(int(fTime)).split(' ')[3].split(':')
    return float(rTime[0]) + float(rTime[1]) / 60.0 + float(rTime[2]) / 3600.0


def updateArrays():
    global timeLastChecked
    for row in c.execute('SELECT * FROM CodeTable WHERE timestamp > ' + timeLastChecked.__str__()):
        times.append(extractTime(row[0]))
        nums.append(row[1])
    timeLastChecked = usertime.time()


timeLastChecked = usertime.time() - 6000
con = sqlite3.connect('C:/data/FacebookOnlineData.db')
c = con.cursor()
size = os.path.getmtime('C:/data/FacebookOnlineData.db')
times = []
nums = []

updateArrays()

plt.ylim(0, max(nums) * 1.2)
plt.interactive(True)
plt.xlim(max(times) - .25, max(times))
plt.ion() # set plot to animated
graph = plt.plot(times, nums, 'r-')
plt.draw()
while True:
    if os.path.getmtime('C:/data/FacebookOnlineData.db') > size:
        updateArrays()
        plt.xlim(max(times) - .25, max(times))
        plt.ylim(0, max(nums) * 1.2)
        plt.plot(times, nums, 'r-')
        plt.draw()
        size = os.path.getmtime('C:/data/FacebookOnlineData.db')
        plt.pause(15)
    plt.pause(1)




