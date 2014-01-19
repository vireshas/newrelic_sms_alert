import cherrypy
import settings
import json
import signal
from sms import Sms
from newrelic_helper import NewrelicHelper
from bitly import Bitly
import sqlite3
from dashboard import Dashboard
from newrelic_plugins import NewrelicPlugins
from jinja2 import Environment, FileSystemLoader

def connect(thread_index):
    cherrypy.thread_data.db = sqlite3.connect("users.db")

cherrypy.engine.subscribe("start_thread", connect)

def handler(signum, frame): 
    reload(settings)
    Webhook.all_users = []
    Webhook().fill_all_users()

signal.signal(signal.SIGUSR1, handler)

class Webhook:
    exposed = True

    def plugins(self):
        con = cherrypy.thread_data.db.cursor()
        all_plugins = con.execute("select plugin from plugin_users").fetchall()
        return [p[0] for p in all_plugins]

    def plugin_users_map(self, plugin):
        con = cherrypy.thread_data.db.cursor()
        plugins = con.execute("select users from plugin_users where plugin = ?", (plugin,)).fetchall()
        return json.loads(plugins[0][0])

    def get_all_users(self):
        con = cherrypy.thread_data.db.cursor()
        u_details = con.execute("select user, ph_num, first_name from user_plugins").fetchall()
        all_users = {}
        for u in u_details:
            all_users[u[0]] = [u[1], u[2]]
        return all_users

    def GET(self, id=None):
        return("request rcved  %s" % id)

    def POST(self, **post_params):
        params = cherrypy.request.body.params
        print params

        #return if its a deployment message
        alert = params.get('alert', None)
        if not alert: return('Deployment alert')

        alert = json.loads(alert)
        app_name = alert.get("application_name", None) or alert["alert_policy_name"]
        severity = alert['severity']
        alert_url = alert['alert_url']
        description = alert['long_description']

        #some messages are filtered out
        #update settings.filters with more filters
        for filter in settings.filters:
            if filter in description.lower(): return('Alert filtered out')

        user_details = NewrelicHelper().fetch_users(app_name)
        short_url = Bitly().shorten_url(alert_url)

        #users_channels subscribed to an application
        for user_detail in user_details:
            user_email = user_detail[2]
            greeting = user_detail[0] and "Hi %s, " % user_detail[0] or "Hi, "
            sms_msg = greeting + description + ". It is %s. Alert url: %s" % (severity, short_url)
            phone_number = settings.users.get(user_email, None)
            if phone_number: Sms().send(phone_number, sms_msg)

        #all the alerts are sent to default person
        for (default_user, ph_no) in settings.default.items():
            sms_msg = "Hi, " + description +  ". It is %s. Alert url: %s" % (severity, short_url)
            Sms().send(ph_no, sms_msg)

        #plugin alerts (its a different path all together)
        all_plugins = self.plugins()
        all_users = self.get_all_users()
        matched_plugins = [p for p in all_plugins if p.lower() in app_name.lower() or p.lower() in description]
        if matched_plugins:
            matched_plugins = matched_plugins[0]
            people_subscribed_to_plugin = self.plugin_users_map(matched_plugins)
            for user_email in people_subscribed_to_plugin:
                u_d = all_users.get(user_email, None)
                if u_d:
                    greeting = u_d[1] and "Hi %s, " % u_d[1] or "Hi, "
                    sms_msg = greeting + description +  ". It is %s. Alert url: %s" % (severity, short_url)
                    print sms_msg
                    if u_d[0] != "new": Sms().send(u_d[0], sms_msg)

        return('Message sent')

config = {'/static': {'tools.staticdir.on': True,
    'tools.staticdir.dir': settings.staticfiles_path, 
}}

cherrypy.tree.mount(NewrelicPlugins(), "/plugin",{ '/':{
    'request.dispatch': cherrypy.dispatch.MethodDispatcher()
}})

cherrypy.tree.mount(Dashboard(),config=config)

cherrypy.tree.mount(Webhook(), "/webhook",{ '/':{ 
    'request.dispatch': cherrypy.dispatch.MethodDispatcher() 
}})

cherrypy.engine.start()
cherrypy.engine.block()
