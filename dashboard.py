import cherrypy
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))

class Dashboard:
    @cherrypy.expose
    def subscribe(self):
        tmp = env.get_template("subscribe.html")
        return tmp.render()
    subscribe.exposed = True

    def dashboard1(self):
        tmp = env.get_template("dashboard1.html")
        return tmp.render()
    dashboard1.exposed = True

    def usage(self):
        tmp = env.get_template("usage.html")
        return tmp.render()
    usage.exposed = True
