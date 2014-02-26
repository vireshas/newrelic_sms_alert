import cherrypy
import sqlite3
from jinja2 import Environment, FileSystemLoader
import json

def connect(thread_index):
    cherrypy.thread_data.db = sqlite3.connect("users.db")

cherrypy.engine.subscribe('start_thread', connect)

class PluginUsers:
    def get_user_and_ph_num(self):
        return self.read("user,ph_num")

    def get_plugins(self):
        return self.read("plugin")

    def read(self, params="*"):
        con = cherrypy.thread_data.db.cursor()
        query = "select %s from plugin_users" % params
        users = con.execute(query).fetchall()
        return users

