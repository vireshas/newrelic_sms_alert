import sqlite3
import settings
import json
from helper.newrelic_helper import NewrelicHelper

a = sqlite3.connect("users.db")
print "connected to db"

newrelic = NewrelicHelper()

apps = newrelic.all_alert_policies()
print "pulled all policies"

plugins = a.execute("select plugin from plugin_users").fetchall()
plugins = [i[0] for i in plugins]
print "pulled old plugins"

new_policies = [i for i in apps if not i in plugins]
print new_policies

for app in new_policies:
    a.execute("insert into plugin_users values(?,?,?)", (app, json.dumps([]), "app"))
print "inserting new policies %s" % str(new_policies)
a.commit()
