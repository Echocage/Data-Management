import sqlite3

from pylab import *

con = sqlite3.connect('C:/data/FacebookFriendsData.db')
c = con.cursor()
times = [0] * 24
user = "Kevin Mykal"

for row in c.execute('SELECT * FROM CodeTable WHERE name = \'' + user + '\''):
    nTime = datetime.datetime.fromtimestamp(row[0]).hour
    times[int(nTime)] += 1
#x =  [x.__str__()+"AM" if int(x/12)==0 else (x/12).__str__() + "PM" for x in xrange(times.__len__())]
plt.bar(xrange(times.__len__()), times)
plt.xlabel("Hours since midnight")
plt.ylabel("Number of times online recorded")
plt.xlim((0, 24))
plt.title(user + "'s Facebook useage")
plt.show()
