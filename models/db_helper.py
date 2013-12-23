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

