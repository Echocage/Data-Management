import urllib
import json
import time as usertime

from sqlalchemy import *
from sqlalchemy.engine.reflection import Inspector

from Token import TokenKey


def LogUsers():
    db = create_engine('sqlite:///C:/data/FacebookOnlineData.db') # Create database engine
    inspector = Inspector.from_engine(db)
    metadata = MetaData(db)
    items = Table('CodeTable', metadata,
                  Column('timestamp', INT),
                  Column('users', INT)
    )
    if not inspector.get_table_names().__contains__('CodeTable'):
        items.create()
    db2 = create_engine('sqlite:///C:/data/FacebookFriendsData.db')
    inspector2 = Inspector.from_engine(db2)
    metadata2 = MetaData(db2)
    items2 = Table('CodeTable', metadata2,
                   Column('timestamp', INT),
                   Column('user', TEXT)
    )
    if not inspector2.get_table_names().__contains__('CodeTable'):
        items2.create()
    time = usertime.time()

    def insertNumIntoTable(users):
        print time.__str__() + ': ' + users.__str__()
        items.insert().execute(timestamp=time, users=users)

    def insertIntoTable(name):
        items2.insert().execute(timestamp=time, name=name)

    query = "SELECT uid, name,online_presence FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me()) order by name"
    params = urllib.urlencode({'q': query, 'access_token': TokenKey})
    url = "https://graph.facebook.com/fql?" + params
    data = urllib.urlopen(url).read()
    insertNumIntoTable([x for x in json.loads(data)['data'] if x['online_presence'] == 'active'].__len__())
    for i in json.loads(data)['data']:
        if i['online_presence'] == 'active':
            insertIntoTable(i['name'])


import threading


def do_every(interval, worker_func, iterations=0):
    if iterations != 1:
        threading.Timer(
            interval,
            do_every, [interval, worker_func, 0 if iterations == 0 else iterations - 1]
        ).start()

    worker_func()


do_every(15, LogUsers)