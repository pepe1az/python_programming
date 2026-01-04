import unittest
import json
import urllib.parse
from myapp.utils.currencies_api import get_currencies

def make_data_url(obj) -> str:
    payload = json.dumps(obj).encode("utf-8")
    return "data:application/json," + urllib.parse.quote(payload.decode("utf-8"))

class TestCurrenciesAPI(unittest.TestCase):
    def test_ok(self):
        fake = {"Valute": {"USD": {"Value": 93.25}, "EUR": {"Value": 101.7}}}
        url = make_data_url(fake)
        res = get_currencies(["USD", "EUR"], url=url)
        self.assertEqual(res["USD"], 93.25)

    def test_missing_valute(self):
        url = make_data_url({"X": 1})
        with self.assertRaises(KeyError):
            get_currencies(["USD"], url=url)

    def test_missing_currency(self):
        url = make_data_url({"Valute": {"USD": {"Value": 93.25}}})
        with self.assertRaises(KeyError):
            get_currencies(["EUR"], url=url)

    def test_invalid_json(self):
        bad = "data:application/json,%7Bnot-json%7D"
        with self.assertRaises(ValueError):
            get_currencies(["USD"], url=bad)

    def test_connection_error(self):
        with self.assertRaises(ConnectionError):
            get_currencies(["USD"], url="https://invalid.invalid", timeout=1)
