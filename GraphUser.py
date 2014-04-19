import sqlite3
from pylab import *
con = sqlite3.connect('C:/data/FacebookFriendsData.db')
c = con.cursor()
times = [0] * 24
#Load timestamps into memory
c.execute("SELECT timestamp FROM TimestampIds")
timestamps = c.fetchall()
#Get Users's ID
user = raw_input("Enter user's name: "),
c.execute('SELECT id FROM Userids WHERE user = ?', user)
userId = (c.fetchone()[0] - 1,)
#Query database with userId getting timestamp indexes for user's
c.execute('SELECT timestampid FROM datatable WHERE userId = ?', userId)
timestampIds = c.fetchall()
#CrossRefrence timestamps in memory vs timestamp's ids which are the in memory timestamp's indexs (+1)
list = [timestamps[x[0] - 1][0] for x in timestampIds]

for row in list:
    nTime = datetime.datetime.fromtimestamp(row).hour
    times[int(nTime)] += 1

plt.bar(xrange(times.__len__()), times)
plt.xlabel("Hours since midnight")
plt.ylabel("Number of times online recorded")
plt.xlim((0, 24))
plt.title(user[0] + "'s Facebook useage")
plt.show()
