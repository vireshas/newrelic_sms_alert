from models.db_helper import DbHelper

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

