import unittest
from unittest.mock import MagicMock
from controllers.currencycontroller import CurrencyController


class TestCurrencyController(unittest.TestCase):
    def test_list_currencies(self):
        mock_db = MagicMock()
        mock_db._read.return_value = [{"id": 1, "char_code": "USD", "value": 90.0}]
        controller = CurrencyController(mock_db)

        result = controller.list_currencies()

        self.assertEqual(result[0]["char_code"], "USD")
        mock_db._read.assert_called_once()

    def test_update_currency(self):
        mock_db = MagicMock()
        mock_db._update.return_value = 1
        controller = CurrencyController(mock_db)

        updated = controller.update_currency("usd", 95.5)

        self.assertEqual(updated, 1)
        mock_db._update.assert_called_once_with({"USD": 95.5})

    def test_delete_currency(self):
        mock_db = MagicMock()
        mock_db._delete.return_value = 1
        controller = CurrencyController(mock_db)

        deleted = controller.delete_currency(10)

        self.assertEqual(deleted, 1)
        mock_db._delete.assert_called_once_with(10)


if __name__ == "__main__":
    unittest.main()
