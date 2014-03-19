import sqlite3
import settings
import json
from helper.newrelic_helper import NewrelicHelper

print "connected to db"
a = sqlite3.connect("users.db")

print "creating user_plugins table"
a.execute("create table user_plugins(user varchar, plugins varchar(1000), ph_num varchar(20), first_name varchar(50))")

print "creating plugin_users table"
a.execute("create table plugin_users(plugin varchar, users varchar(1000), type varchar(10))")

print "filling in plugins"
for plugin in settings.plugins:
    a.execute("insert into plugin_users values(?,?,?)", (plugin, json.dumps([]), "plugin"))

newrelic = NewrelicHelper()

print "filling apps"
for app in newrelic.all_alert_policies():
    a.execute("insert into plugin_users values(?,?,?)", (app, json.dumps([]), "app"))

print "filling users"
old_users = settings.users
all_users = newrelic.all_users()
new_users = [u for u in all_users.keys() if u not in old_users.keys()]
for (user,p_num) in old_users.items():
    a.execute("insert into user_plugins values(?,?,?,?)", (user,json.dumps([]), p_num, all_users[user]))

for nu in new_users:
    a.execute("insert into user_plugins values(?,?,?,?)", (nu,json.dumps([]), "new", all_users[nu]))

a.commit()
