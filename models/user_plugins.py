from models.db_helper import DbHelper
import json

class UserPlugins:
    def __init__(self):
        self.db = DbHelper()
        self.table = "user_plugins"

    def get_user_and_ph_num(self):
        return self.db.select(self.table, "user,ph_num")

    def plugins_subscribed_by(self, user):
        return self.db.select(self.table, "plugins", "user", user)

    def get_users(self):
        return self.db.select(self.table, "user")

    def update_plugins_for(self, plugins, user):
        return self.db.update(self.table, "plugins", plugins,"user",user)

    def update_ph_num_for(self, ph_num, user):
        return self.db.update(self.table, "ph_num", ph_num, "user", user, "false")

    def create_new_user(self, user, ph_num):
        query = 'insert into user_plugins values(?,?,?,?)'
        params = (user, json.dumps([]), ph_num, None)
        return self.db.insert(query, params)

