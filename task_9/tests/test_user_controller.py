import unittest
from unittest.mock import MagicMock
from controllers.usercontroller import UserController


class TestUserController(unittest.TestCase):
    def test_list_users(self):
        users_db = MagicMock()
        user_currency_db = MagicMock()
        users_db._read.return_value = [{"id": 1, "name": "Alice"}]

        controller = UserController(users_db, user_currency_db)

        users = controller.list_users()

        self.assertEqual(users[0]["name"], "Alice")
        users_db._read.assert_called_once()

    def test_get_user(self):
        users_db = MagicMock()
        user_currency_db = MagicMock()
        users_db._read_one.return_value = {"id": 2, "name": "Bob"}

        controller = UserController(users_db, user_currency_db)

        user = controller.get_user(2)

        self.assertEqual(user["name"], "Bob")
        users_db._read_one.assert_called_once_with(2)

    def test_get_user_currencies(self):
        users_db = MagicMock()
        user_currency_db = MagicMock()
        user_currency_db._get_user_currencies.return_value = [{"char_code": "USD"}]

        controller = UserController(users_db, user_currency_db)

        cur = controller.get_user_currencies(1)

        self.assertEqual(cur[0]["char_code"], "USD")
        user_currency_db._get_user_currencies.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
