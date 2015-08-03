import urllib.request
import urllib.parse
import urllib.error
import time

import requests

from database import session, User, Timestamp, Datapoint


token = open('Token.txt').read().strip()
token_query = "SELECT uid, name, online_presence " \
              "FROM user " \
              "WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me()) order by name"
params = urllib.parse.urlencode({'q': token_query, 'access_token': token})
base_url = "https://graph.facebook.com/"
url = "{}/fql?{}".format(base_url, params)
custom_rep = {'offline': 0, 'idle': 1, 'active': 2}

user_store = {user.name: user.ROWID for user in session.query(User).all()}


def get_user_data():
    data = requests.get(url)
    if data.status_code:
        users = data.json()['data']
        return [(user['name'], user['online_presence']) for user in users]


def log_individuals():
    timestamp = Timestamp(timestamp=time.time())
    user_data = get_user_data()
    if not user_data:
        return
    formatted_data = [(User(name=name), custom_rep[status]) for name, status in user_data if status != 'offline']
    new_users = [user for user, status in formatted_data if user.name not in user_store]
    session.add_all(new_users)
    session.add(timestamp)

    session.commit()
    session.flush()
    user_store.update({user.name: user.ROWID for user in new_users})

    datapoints = [Datapoint(user_id=user_store[user.name], timestamp_id=timestamp.ROWID, status=status)
                  for user, status in formatted_data]

    session.add_all(datapoints)
    session.commit()


while True:
    log_individuals()
    time.sleep(5)
