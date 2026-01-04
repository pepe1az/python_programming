from controllers.databasecontroller import UsersCRUD, UserCurrencyCRUD


class UserController:
    def __init__(self, users_db: UsersCRUD, user_currency_db: UserCurrencyCRUD):
        self.users_db = users_db
        self.user_currency_db = user_currency_db

    def list_users(self):
        return self.users_db._read()

    def get_user(self, user_id: int):
        return self.users_db._read_one(int(user_id))

    def get_user_currencies(self, user_id: int):
        return self.user_currency_db._get_user_currencies(int(user_id))
