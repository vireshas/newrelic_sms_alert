import cherrypy
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('static_files'))

class Dashboard:
    @cherrypy.expose
    def subscribe(self):
        tmp = env.get_template("subscribe.html")
        return tmp.render()
    subscribe.exposed = True

    def usage(self):
        tmp = env.get_template("usage.html")
        return tmp.render()
    usage.exposed = True

    def new_models(self):
        from models.user_plugins import UserPlugins
        from models.plugin_users import PluginUsers

        #u = UserPlugins()
        #details = u.get_users()
        #details = u.plugins_subscribed_by("viresh.sanagoudar@ibibogroup.com")
        #details = u.update_plugins_for(['memcache', "redis"],"viresh.sanagoudar@ibibogroup.com")

        p = PluginUsers()
        #details = p.update_users_for(["viresh.sanagoudar@ibibogroup.com"], "redis")
        details = p.users_subscribed_to_a('redis')
        print details
        return "testing"
    new_models.exposed = True
