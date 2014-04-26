import json
import sqlite3
import urllib
import time
import threading
from Token import TokenKey


def LogUsers():
    con = sqlite3.connect('C:/data/FacebookFriendsData.db')
    onlineConn = sqlite3.connect('C:/data/FacebookOnlineData.db')
    onlineCur = onlineConn.cursor()
    c = con.cursor()
    list = [['UserIds', ['user TEXT', 'id NUMERIC']], ['TimestampIds', ['timestamp REAL', 'id INTEGER']],
            ['DataTable', ['userID INTEGER', 'timestampID INTEGER']]]
    for i in list:
        try:
            c.execute('SELECT * FROM "' + i[0] + '"')
        except:
            c.execute('CREATE TABLE "' + i[0] + '" (' + ','.join(i[1]) + ')')

    query = "SELECT uid, name,online_presence FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me()) order by name"
    params = urllib.urlencode({'q': query, 'access_token': TokenKey})
    url = "https://graph.facebook.com/fql?" + params
    data = urllib.urlopen(url).read()
    currentTime = time.time()

    onlineCur.execute('INSERT INTO CodeTable VALUES (?,?)',
                      [currentTime, len([x for x in json.loads(data)['data'] if x['online_presence'] == 'active'])])
    timestampId = [x for x in c.execute('SELECT * FROM timestampids WHERE timestamp = ' + str(currentTime) + '')]
    if len(timestampId) == 0:
        try:
            timestampId = [x for x in c.execute("SELECT * from timestampids ORDER BY id DESC LIMIT 1")][0][1] + 1
        except:
            print 'New Timestamp'
            timestampId = 1
    else:
        timestampId = timestampId[0][1]
    c.execute('INSERT INTO Timestampids VALUES (?,?)', [int(currentTime), timestampId])
    for i in json.loads(data)['data']:
        if i['online_presence'] == 'active':
            userId = [x for x in c.execute('SELECT * FROM UserIds WHERE user = "' + i['name'] + '"')]
            if len(userId) == 0:
                try:
                    userId = [x for x in c.execute("SELECT * from userIds ORDER BY id DESC LIMIT 1")][0][1] + 1
                except:
                    userId = 1
                c.execute('INSERT INTO UserIds VALUES (?,?)', [i['name'], userId])
            else:
                userId = userId[0][1]
            c.execute('INSERT INTO DataTable VALUES (?,?)', [userId, timestampId])
    con.commit()
    onlineConn.commit()


def do_every(interval, worker_func, iterations=0):
    if iterations != 1:
        threading.Timer(
            interval,
            do_every, [interval, worker_func, 0 if iterations == 0 else iterations - 1]
        ).start()

    worker_func()


do_every(15, LogUsers)