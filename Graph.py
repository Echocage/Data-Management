from collections import defaultdict
from datetime import datetime
from matplotlib.dates import DateFormatter

from pylab import plt

from database import session, Datapoint


session.query(Datapoint).all()


def format_timestamp(timestamp):
    real_timestamp = datetime.fromtimestamp(float(timestamp.timestamp))
    now = datetime.now()
    return real_timestamp.replace(year=now.year, day=now.day, month=now.month)


datapoints = [(datapoint.user.name, datapoint.timestamp) for datapoint in session.query(Datapoint)]

grouped_data = defaultdict(int)
for datapoint in session.query(Datapoint):
    if datapoint.status == 2:
        grouped_data[datapoint.timestamp] += 1

print('Here')
x = list(map(format_timestamp, grouped_data.keys()))
plt.plot(x, list(grouped_data.values()), 'go')
formatter = DateFormatter('%H:%M')
plt.gcf().axes[0].xaxis.set_major_formatter(formatter)
plt.show()




