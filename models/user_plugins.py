import cherrypy
import sqlite3
from jinja2 import Environment, FileSystemLoader
import json

def connect(thread_index):
    cherrypy.thread_data.db = sqlite3.connect("users.db")

cherrypy.engine.subscribe('start_thread', connect)

class UserPlugins:
    def get_user_and_ph_num(self):
        return self.select("user,ph_num")

    def plugins_subscribed_by(self, user):
        return self.select("plugins", "user", user)

    def get_users(self):
        return self.select("user")

    def select(self, params='*', where='', where_params=''):
        con = cherrypy.thread_data.db.cursor()
        if where:
            where_params = tuple(where_params.split(","))
            where = "where %s = ?" % where
            query = "select %s from user_plugins %s" % (params, where)
            users = con.execute(query, where_params).fetchall()
        else:
            query = "select %s from user_plugins" % params
            users = con.execute(query).fetchall()

        return users

