import sqlite3
import urllib.request, urllib.parse, urllib.error
import time

import requests


token_query = "SELECT uid, name,online_presence FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me()) order by name"
params = urllib.parse.urlencode({'q': token_query, 'access_token': TokenKey})
base_url = "https://graph.facebook.com/"
url = "{}/fql?{}".format(base_url, params)
db = sqlite3.connect('C:/data/FacebookOnlineData.db')
custom_rep = {'offline': 0, 'idle': 1, 'active': 2}


def log_individuals():
    ind_db = sqlite3.connect('C:/data/Facebook.db')
    now = time.time()
    cur = ind_db.cursor()
    data = requests.get(url).json()
    users = data['data']
    user_data = [(user['name'], custom_rep[user['online_presence']]) for user in users]
    cur.execute('INSERT OR IGNORE INTO timestamps (timestamp) VALUES (?)', (now,))
    cur.executemany('INSERT OR IGNORE INTO users (username) VALUES  (?)', [(name,) for (name, stat) in user_data])
    cur.executemany('INSERT OR IGNORE INTO datapoints '
                    'SELECT timestamps.rowid, us.rowid, ? FROM users '
                    'INNER JOIN timestamps ON timestamps.timestamp = ? '
                    'INNER JOIN users us ON us.username = ?', ((status, now, name) for name, status in user_data))
    ind_db.commit()


while True:
    log_individuals()
    time.sleep(15)
