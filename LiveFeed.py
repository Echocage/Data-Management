from _tkinter import TclError
from collections import OrderedDict
import datetime
import os
import time
from pylab import plt
from matplotlib.dates import DateFormatter

from database import session, Datapoint


def format_timestamp(timestamp):
    real_timestamp = datetime.datetime.fromtimestamp(float(timestamp))
    now = datetime.datetime.now()
    return real_timestamp.replace(year=now.year, day=now.day, month=now.month)


def refresh():
    global time_checked

    grouped_data = OrderedDict()
    for datapoint in session.query(Datapoint):
        timestamp = datapoint.timestamp.timestamp
        if datapoint.status == 2:
            grouped_data[timestamp] = grouped_data.get(timestamp, 0) + 1

    time_checked = time.time()


    fifteen_ago = time.time() -  datetime.timedelta(minutes=20).total_seconds()
    relevant_data = [(t, n) for t, n in grouped_data.items() if float(t) > fifteen_ago]

    update_graph([format_timestamp(t) for t, n in relevant_data], [n for t, n in relevant_data])


def update_graph(times, nums):
    plt.xlim(max(times) - datetime.timedelta(minutes=15), max(times))
    plt.ylim(0, max(nums) * 1.2)
    plt.plot_date(times, nums, 'ro')
    plt.draw()


path = 'datastore.db'
time_checked = time.time() - 3000
size = os.path.getmtime(path)
plt.ion()
refresh()
formatter = DateFormatter('%H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
while True:
    try:
        if os.path.getmtime(path) > size:
            refresh()
            size = os.path.getmtime(path)
            plt.pause(10)
        else:
            plt.pause(1)
    except TclError:  # Can't sleep due to graph being closed
        break




