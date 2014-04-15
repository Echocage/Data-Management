import sqlite3
import numpy as np
from pylab import *

colors = ['g', 'y', 'r', 'b']


def getColor():
    return colors.pop()


con = sqlite3.connect('C:/data/FacebookFriendsData.db')
c = con.cursor()
userInput = raw_input('Enter users seprated by commas: ')
users = [x.strip() for x in userInput.strip('\n').split(',')]
times = [[0] * 24 for x in users]
for row in c.execute(
                'SELECT * FROM CodeTable WHERE user IN ' + ([x for x in users].__str__()).replace('[', '(').replace(']',
                                                                                                                    ')')):
    nTime = datetime.datetime.fromtimestamp(row[0]).hour
    times[users.index(row[1])][int(nTime)] += 1

index = np.arange(24)
bars = []
width = .7 / users.__len__()
for x in times:
    bars.append(plt.bar(index + times.index(x) * width, x, color=getColor(), label=users[times.index(x)], width=width))

plt.xlabel("Hours since midnight")
plt.ylabel("Number of times online recorded")
plt.xlim((0, 24))
plt.title([x for x in users].__str__() + "'s Facebook useage")
plt.tight_layout()
plt.legend()
plt.show()
