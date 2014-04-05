from _tkinter import TclError
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


def updateGraph():
    plt.xlim(max(times) - .25, max(times))
    plt.ylim(0, max(nums) * 1.2)
    plt.plot(times, nums, 'r-')
    plt.draw()


timeLastChecked = usertime.time() - 6000
con = sqlite3.connect('C:/data/FacebookOnlineData.db')
c = con.cursor()
size = os.path.getmtime('C:/data/FacebookOnlineData.db')
times, nums = [], []

plt.ion()
updateArrays()
updateGraph()
plt.show()

while True:
    try:
        if os.path.getmtime('C:/data/FacebookOnlineData.db') > size:
            updateArrays()
            updateGraph()
            size = os.path.getmtime('C:/data/FacebookOnlineData.db')
            plt.pause(
                15)  # Database "Should" update every 15 seconds, so lets way until it should be updated before trying.
        else:
            plt.pause(1)
    except TclError:  # Can't sleep due to graph being closed
        None




