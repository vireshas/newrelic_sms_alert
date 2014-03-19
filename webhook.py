import cherrypy
import settings
from controller.dashboard import Dashboard
from controller.newrelic_plugins import NewrelicPlugins
from controller.app import App

config = {'/static': {'tools.staticdir.on': True,
    'tools.staticdir.dir': settings.staticfiles_path,
}}

cherrypy.tree.mount(NewrelicPlugins(), "/plugin",{ '/':{
    'request.dispatch': cherrypy.dispatch.MethodDispatcher()
}})

cherrypy.tree.mount(Dashboard(),config=config)

cherrypy.tree.mount(App(), "/webhook",{ '/':{
    'request.dispatch': cherrypy.dispatch.MethodDispatcher()
}})

cherrypy.config.update({'server.socket_host': settings.server_host, })
cherrypy.config.update({'server.socket_port': int(settings.server_port), })

cherrypy.engine.start()
cherrypy.engine.block()
