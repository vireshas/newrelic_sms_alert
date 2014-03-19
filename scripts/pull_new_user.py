import sqlite3
import settings
import json
from helper.newrelic_helper import NewrelicHelper

print "connecting to db"
a = sqlite3.connect("users.db")

newrelic = NewrelicHelper()

print "fetching new users"
old_users = a.execute('select user from user_plugins').fetchall()
old_users = [i[0] for i in old_users]
all_users = newrelic.all_users()
new_users = [u for u in all_users.keys() if u not in old_users]

print "inserting %d new users" % len(new_users)
for nu in new_users:
    a.execute("insert into user_plugins values(?,?,?,?)", (nu,json.dumps([]), "new", all_users[nu]))

a.commit()
print "done :^)"
