import urllib
import urllib2
import json
import settings

class NewrelicHelper:
    app_id = settings.newrelic_appid 
    parent_url = "https://api.newrelic.com/v2/"
    api_endpoints = {
            "alert_policy" : "alert_policies",
            "alert_channels" : "notification_channels",
            "users": "users"
    }
    api_resp_type = "json"

    def all_alert_policies(self):
        end_point = "alert_policies"
        resp = self.api_call(end_point, {})
        alert_policies = resp[end_point]
        alerts = [a["name"] for a in alert_policies]
        return(alerts)

    def all_users(self):
        end_point = "users"
        resp = self.api_call(end_point, {})
        users = resp[end_point]
        u_dict = {}
        u_new = [u_dict.update({u["email"].lower():u["first_name"]}) for u in users]
        return(u_dict)

    def all_applications(self):
        end_point = "applications"
        resp = self.api_call(end_point, {})
        applications = resp[end_point]
        apps = [app["name"] for app in applications]
        return(apps)

    def fetch_users(self, application_name):
        users = []
        applicaiton_details = self.fetch_alert_policies(application_name)
        if not applicaiton_details: return(users)

        notifications = applicaiton_details[0]["links"]["notification_channels"]
        for notification in notifications:
            user_id = self.fetch_notification_details(notification)
            if user_id == None: continue
            users.append(self.fetch_user_details(user_id))
        return users

    def fetch_user_details(self, user_id):
        end_point = "users"
        params = {"filter[ids]" : user_id}
        resp = self.api_call(end_point, params)
        user_details = resp["users"][0]
        first_name = user_details["first_name"]
        last_name = user_details["last_name"]
        email = user_details["email"]
        return (first_name, last_name, email)

    def fetch_notification_details(self, notification_id):
        end_point = "notification_channels"
        params = {"filter[ids]" : notification_id}
        resp = self.api_call(end_point, params)
        notification_channels = resp[end_point]
        links = notification_channels[0]
        if "links" in links.keys():
            links = links["links"]
            user_id = links["user"]
        else:
            user_id = None
        return user_id

    def fetch_alert_policies(self, application_name):
        end_point = NewrelicHelper.api_endpoints["alert_policy"]
        params = {"filter[name]" : application_name}
        resp = self.api_call(end_point, params)
        applications = resp[end_point]
        filtered_app = [app for app in applications if app["name"].lower() == application_name.lower()]
        return filtered_app

    def api_call(self, end_point, params):
        params = urllib.urlencode(params)
        req = urllib2.Request(self.url_builder(end_point), params)
        req.add_header("X-Api-Key", NewrelicHelper.app_id)
        resp = urllib2.urlopen(req)
        return(json.load(resp))

    def url_builder(self, end_point):
        return(NewrelicHelper.parent_url + end_point + "." + NewrelicHelper.api_resp_type)
