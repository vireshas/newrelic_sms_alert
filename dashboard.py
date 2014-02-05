import cherrypy
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('static_files'))

class Dashboard:
    @cherrypy.expose
    def subscribe(self):
        tmp = env.get_template("subscribe.html")
        return tmp.render(type="subscribe")
    subscribe.exposed = True

    def usage(self):
        tmp = env.get_template("usage.html")
        return tmp.render(type="usage")
    usage.exposed = True

    def new_models(self):
        from models.user_plugins import UserPlugins
        u = UserPlugins()
        details = u.create_new_user("vv@as.com", "34523")
        return "testing"
    new_models.exposed = True
