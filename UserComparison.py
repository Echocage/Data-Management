import sqlite3
import numpy as np
from pylab import *

colors = ['g', 'y', 'r', 'b']


def getColor():
    return colors.pop()


con = sqlite3.connect('C:/data/FacebookFriendsData.db')
c = con.cursor()

user = ['Becca Redmond', 'Tanner Mindak']
times = [[0] * 24 for x in user]
for row in c.execute(
                'SELECT * FROM CodeTable WHERE user IN ' + ([x for x in user].__str__()).replace('[', '(').replace(']',
                                                                                                                   ')')):
    nTime = datetime.datetime.fromtimestamp(row[0]).hour
    times[user.index(row[1])][int(nTime)] += 1

index = np.arange(24)
bars = []
width = .7 / user.__len__()
for x in times:
    bars.append(plt.bar(index + times.index(x) * width, x, color=getColor(), label=user[times.index(x)], width=width))

plt.xlabel("Hours since midnight")
plt.ylabel("Number of times online recorded")
plt.xlim((0, 24))
plt.title([x for x in user].__str__() + "'s Facebook useage")
plt.tight_layout()
plt.legend()
plt.show()
