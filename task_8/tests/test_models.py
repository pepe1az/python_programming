import unittest
from myapp.models import Author, App, User, Currency, UserCurrency

class TestModels(unittest.TestCase):
    def test_author_validation(self):
        with self.assertRaises(ValueError):
            Author("", "X")
        a = Author("Kirill", "M321")
        self.assertEqual(a.name, "Kirill")

    def test_user_validation(self):
        with self.assertRaises(ValueError):
            User(0, "A")
        with self.assertRaises(ValueError):
            User(1, "")
        u = User(1, "Alice")
        self.assertEqual(u.id, 1)

    def test_currency_validation(self):
        with self.assertRaises(ValueError):
            Currency(1, "840", "US", "Dollar", 1.0, 1)  # bad char_code
        with self.assertRaises(TypeError):
            Currency(1, "840", "USD", "Dollar", "x", 1)
        c = Currency(1, "840", "USD", "Dollar", 93.25, 1)
        self.assertAlmostEqual(c.value, 93.25)

    def test_user_currency_validation(self):
        with self.assertRaises(ValueError):
            UserCurrency(1, 0, 1)
        uc = UserCurrency(1, 1, 2)
        self.assertEqual(uc.currency_id, 2)

    def test_app(self):
        a = Author("Kirill", "M321")
        app = App("X", "1.0", a)
        self.assertEqual(app.author.name, "Kirill")
