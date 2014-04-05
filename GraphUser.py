import sqlite3

from pylab import *

con = sqlite3.connect('C:/data/FacebookFriendsData.db')
c = con.cursor()
times = [0] * 24
user = "Matthew Moya"

for row in c.execute('SELECT * FROM CodeTable WHERE name = \'' + user + '\''):
    nTime = datetime.datetime.fromtimestamp(row[0]).hour
    times[int(nTime)] += 1

plt.bar(xrange(times.__len__()), times)
plt.xlabel("Hours since midnight")
plt.ylabel("Number of times online recorded")
plt.xlim((0, 24))
plt.title(user + "'s Facebook useage")
plt.show()
