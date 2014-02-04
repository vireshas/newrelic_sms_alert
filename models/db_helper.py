import cherrypy
import sqlite3
from jinja2 import Environment, FileSystemLoader
import json

def connect(thread_index):
    cherrypy.thread_data.db = sqlite3.connect("users.db")

cherrypy.engine.subscribe('start_thread', connect)

class DbHelper:
    def select(self, table, params='*', where='', where_params=''):
        con = cherrypy.thread_data.db.cursor()
        if where:
            where_params = tuple(where_params.split(","))
            where = "where %s = ?" % where
            query = "select %s from %s %s" % (params, table, where)
            response = con.execute(query, where_params).fetchall()
        else:
            query = "select %s from %s" % (params, table)
            response = con.execute(query).fetchall()
        return response


    def update(self, table, set_key, set_value, where_key, where_value, json_value=""):
        con = cherrypy.thread_data.db.cursor()
        partial_query = "update %s set %s=? where %s=?" % (table, set_key, where_key)
        if not json_value: set_value = json.dumps(set_value)
        params = (set_value, where_value)
        con.execute(partial_query, params)
        cherrypy.thread_data.db.commit()
