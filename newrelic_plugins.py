import cherrypy
import sqlite3
from jinja2 import Environment, FileSystemLoader
import json
from models.user_plugins import UserPlugins
from models.plugin_users import PluginUsers

def connect(thread_index):
    cherrypy.thread_data.db = sqlite3.connect("users.db")

cherrypy.engine.subscribe('start_thread', connect)
env = Environment(loader=FileSystemLoader('static_files'))

class NewrelicPlugins:
    exposed = True
    def GET(self, user='', plugin='', type=''):
        con = cherrypy.thread_data.db.cursor()
        tmp = env.get_template('user_plugins.html')
        tmp_json = env.get_template('users.html')

        if plugin == "plugin" or plugin == "app":
            plugins = PluginUsers().get_plugin_of_type(plugin)
            plugins = [u[0] for u in plugins]
            if type=="json":
                return tmp_json.render(elements=json.dumps(plugins))
            else:
                return tmp.render(elements=plugins, type="plugin")

        if user == "all_details":
            users = UserPlugins().get_user_and_ph_num()
            new_list = []
            for u in users:
                if u[1] != "new":
                    new_list.append([u[0], "existing"])
                else:
                    new_list.append([u[0], "new_user"])
            return tmp.render(elements=new_list, type="user")

        #pass user = all to fetch all the users
        if user == "all":
            users = UserPlugins().get_users()
            users = [u[0] for u in users]
            if type=="json":
                return tmp_json.render(elements=json.dumps(users))
            else:
                return tmp.render(elements = users, type="user")

        #pass plugin = all to fetch all the plugins
        if plugin == "all":
            plugins = PluginUsers().get_plugins()
            plugins = [u[0] for u in plugins]
            if type=="json":
                return tmp_json.render(elements=json.dumps(plugins))
            else:
                return tmp.render(elements=plugins, type="plugin")

        #pass user email or plugin name to fetch more details
        if user:
            res = UserPlugins().plugins_subscribed_by(user)
            if not res:
                return tmp.render(plugins = [])
            elif type == "json":
                return tmp_json.render(elements = res[0][0])
            else:
                return tmp.render(plugins = json.loads(res[0][0]))

        if plugin:
            plugins = PluginUsers().users_subscribed_to_a(plugin)
            if not plugins:
                return tmp.render(plugins = [])
            elif type == "json":
                return tmp_json.render(elements = plugins[0][0])
            else:
                return tmp.render(plugins = json.loads(plugins[0][0]))


    def POST(self, user="", plugin="", ph_num="new"):
        con = cherrypy.thread_data.db.cursor()
        tmp = env.get_template('user_plugins.html')

        if user and ph_num != "new":
            res = UserPlugins().update_ph_num_for(ph_num, user)
            return("user details updated")

        #if not plugin: return(tmp.render(plugins = [], warnings = "Please pass a plugin name"))
        if user:
            res = UserPlugins().plugins_subscribed_by(user)
            if res:
                plugins = json.loads(res[0][0])

                #unsubscribe from all alerts
                if plugin == "":
                    for p in plugins:
                        plugin_users_map = PluginUsers().users_subscribed_to_a(p)
                        users = json.loads(plugin_users_map[0][0])
                        del users[users.index(user)]
                        PluginUsers().update_users_for(users, p)
                UserPlugins().update_plugins_for([], user)

                #unsubscribe from few alerts
                plugin_new = plugin.split(",")
                for p in plugin_new:
                    if p in plugins:
                        continue
                    else:
                        plugin_users_map = PluginUsers().users_subscribed_to_a(p)
                        if not plugin_users_map: return tmp.render(plugins = [], warnings = "Please check if plugin name is valid")
                        users = json.loads(plugin_users_map[0][0])
                        if user in users: continue
                        users.append(user)
                        PluginUsers().update_users_for(users, p)

                deleted_plugins = [plug for plug in plugins if plug not in plugin_new]
                #update user with new plugins == deleting older plugins
                UserPlugins().update_plugins_for(plugin_new, user)

                for p in deleted_plugins:
                    plugin_users_map = PluginUsers().users_subscribed_to_a(p)
                    users = json.loads(plugin_users_map[0][0])
                    del users[users.index(user)]
                    PluginUsers().update_users_for(users, p)
                msg = "You are now subscribed to %s" % p
                return tmp.render(plugins = [], warnings = msg)

            else:
                print "creating new user %s with ph_num %s" % (user,ph_num)
                res = con.execute("insert into user_plugins values(?,?,?)", (user, json.dumps([]), ph_num))
                cherrypy.thread_data.db.commit()
                return("created new user")
