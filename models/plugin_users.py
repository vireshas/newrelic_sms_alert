from models.db_helper import DbHelper

class PluginUsers:
    def __init__(self):
        self.db = DbHelper()
        self.table = "plugin_users"

    def get_plugins(self):
        return self.db.select(self.table, "plugin")

    def get_plugin_of_type(self, type):
        return self.db.select(self.table, "plugin", "type", type)

    def users_subscribed_to_a(self, plugin):
        return self.db.select(self.table, "users", "plugin", plugin)

    def update_users_for(self, users, plugin):
        return self.db.update(self.table, "users", users, "plugin", plugin)

