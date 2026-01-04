import unittest
import json
import urllib.parse

from currencies import get_currencies


def make_data_url(obj) -> str:
    payload = json.dumps(obj).encode("utf-8")
    return "data:application/json," + urllib.parse.quote(payload.decode("utf-8"))


class TestGetCurrencies(unittest.TestCase):
    def test_correct_return_fake(self):
        fake = {"Valute": {"USD": {"Value": 93.25}, "EUR": {"Value": 101.7}}}
        url = make_data_url(fake)
        res = get_currencies(["USD", "EUR"], url=url)
        self.assertEqual(res, {"USD": 93.25, "EUR": 101.7})

    def test_missing_currency_keyerror(self):
        fake = {"Valute": {"USD": {"Value": 93.25}}}
        url = make_data_url(fake)
        with self.assertRaises(KeyError):
            get_currencies(["EUR"], url=url)

    def test_missing_valute_keyerror(self):
        fake = {"SomethingElse": {}}
        url = make_data_url(fake)
        with self.assertRaises(KeyError):
            get_currencies(["USD"], url=url)

    def test_invalid_json_valueerror(self):
        bad = "data:application/json,%7Bnot-json%7D"
        with self.assertRaises(ValueError):
            get_currencies(["USD"], url=bad)

    def test_connection_error(self):
        with self.assertRaises(ConnectionError):
            get_currencies(["USD"], url="https://invalid.invalid", timeout=1)

    def test_wrong_value_type_typeerror(self):
        fake = {"Valute": {"USD": {"Value": "93.25"}}}
        url = make_data_url(fake)
        with self.assertRaises(TypeError):
            get_currencies(["USD"], url=url)

    def test_real_rates_optional(self):
        try:
            res = get_currencies(["USD", "EUR"])
        except ConnectionError:
            self.skipTest("No internet / API unavailable in test environment")
        self.assertIn("USD", res)
        self.assertIn("EUR", res)
        self.assertIsInstance(res["USD"], float)
        self.assertIsInstance(res["EUR"], float)
