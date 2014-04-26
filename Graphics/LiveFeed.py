from _tkinter import TclError
import sqlite3
import time as usertime
import os
from pylab import *
from matplotlib.dates import DateFormatter


def extractTime(fTime):
    return datetime.datetime.fromtimestamp(fTime)  # Turns timestamp into datetime object


def updateArrays():
    global timeLastChecked
    for row in c.execute('SELECT * FROM CodeTable WHERE timestamp > ' + timeLastChecked.__str__()):
        times.append(extractTime(row[0]))
        nums.append(row[1])
    timeLastChecked = usertime.time()


def updateGraph():
    plt.xlim(max(times) - datetime.timedelta(minutes=15), max(times))
    plt.ylim(0, max(nums) * 1.2)
    plt.plot_date(times, nums, 'r-')
    plt.draw()


path = 'C:/data/FacebookOnlineData.db'
timeLastChecked = usertime.time() - 3000
con = sqlite3.connect(path)
c = con.cursor()
size = os.path.getmtime(path)
times, nums = [], []
plt.ion()
updateArrays()
updateGraph()
plt.show()
formatter = DateFormatter('%H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
while True:
    try:
        if os.path.getmtime(path) > size:
            updateArrays()
            updateGraph()
            size = os.path.getmtime(path)
            plt.pause(
                15)  # Database "Should" update every 15 seconds, so lets way until it should be updated before trying.
        else:
            plt.pause(1)
    except TclError:  # Can't sleep due to graph being closed
        break




