import sqlite3

timestampList = []
userList = []
dataList = []
#====User Variables=====
#Path to previous database
oldDb = 'C:/data/FacebookFriendsData.db'
#Path to new database
newDb = 'C:/data/FacebookFriendsData2.db'
#=======================





def addPoint(name, currentTime):
    try:
        if timestampList[-1] == currentTime:
            timestampId = timestampList.__len__()
        else:
            timestampId = timestampList.__len__() + 1
            timestampList.append(currentTime)
    except:
        timestampId = timestampList.__len__() + 1
        timestampList.append(currentTime)

    try:
        userId = userList.index(name)
    except:
        userId = userList.__len__() + 1
        userList.append(name)
    dataList.append([userId, timestampId])


con = sqlite3.connect(newDb)
c = con.cursor()
list = [['UserIds', ['user TEXT', 'id NUMERIC']], ['TimestampIds', ['timestamp INTEGER', 'id INTEGER']],
        ['DataTable', ['userID INTEGER', 'timestampID INTEGER']]]
for i in list:
    try:
        c.execute('SELECT * FROM "' + i[0] + '"')
    except:
        c.execute('CREATE TABLE "' + i[0] + '" (' + ','.join(i[1]) + ')')

con2 = sqlite3.connect(oldDb)
c2 = con2.cursor()
i = 0
for row in c2.execute('SELECT * FROM CodeTable'):
    addPoint(row[1], int(row[0]))
    i += 1
    if i % 1000000 == 0:
        print i
print '============ Converted ============'
ctimestampList = []
cuserList = []
for x in xrange(len(timestampList)):
    ctimestampList.append([timestampList[x], x + 1])
for x in xrange(len(userList)):
    cuserList.append([userList[x], x + 1])

c.executemany('INSERT INTO Timestampids VALUES (?,?)', ctimestampList)
c.executemany('INSERT INTO UserIds VALUES (?,?)', cuserList)
c.executemany('INSERT INTO DataTable VALUES (?,?)', dataList)

con.commit()