import json
import sqlite3
import urllib
from Token import TokenKey


def LogUsers():
    con = sqlite3.connect('C:/data/FacebookFriendsData2.db')
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
    for i in json.loads(data)['data']:
        if i['online_presence'] == 'active':
            None
    print con.commit()


LogUsers()