import sqlite3
import numpy as np
from pylab import *

colors = ['g', 'y', 'r', 'b']

def getColor():
    return colors.pop()

con = sqlite3.connect('C:/data/FacebookFriendsData.db')
c = con.cursor()
users = raw_input("Please enter the user's names with commas in between each:\t").strip()
users = [x.strip() for x in users.strip('\n').split(',')]
times = [[0] * 24 for x in users]

#Load timestamps into memory
c.execute("SELECT timestamp FROM TimestampIds")
timestamps = c.fetchall()

#Get Users's ID
c.execute('SELECT user, id FROM Userids WHERE user in (' + (','.join(['?' for x in xrange(len(users))])) + ')', users)
userList = [[user, id - 1] for user, id in c.fetchall()]

#Query database with userId getting timestamp indexes for user's
c.execute('SELECT userid, timestampid FROM datatable WHERE userId in (' + (
','.join(['?' for x in xrange(len(userList))])) + ')', [x[1] for x in userList])
data = c.fetchall()
for num in xrange(len(userList)):
    userList[num] = [userList[num][0], [x[1] for x in data if x[0] == userList[num][1]]]

for (name, indexs) in userList:
    for x in indexs:
        nTime = datetime.datetime.fromtimestamp(timestamps[x][0]).hour
        times[users.index(name)][int(nTime)] += 1

index = np.arange(24)
bars = []
width = .8 / users.__len__()
for x in times:
    bars.append(plt.bar(index + times.index(x) * width, x, color=getColor(), label=users[times.index(x)], width=width))

plt.xlabel("Hours since midnight")
plt.ylabel("Number of times online recorded")
plt.xlim((0, 24))
plt.title(str([x for x in users]) + "'s Facebook useage")
plt.tight_layout()
plt.legend()
plt.show()
