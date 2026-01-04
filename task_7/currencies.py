import json
import urllib.request
import urllib.error


def get_currencies(currency_codes: list, url="https://www.cbr-xml-daily.ru/daily_json.js", timeout=10) -> dict:
    if not isinstance(currency_codes, list):
        raise TypeError("currency_codes must be a list")

    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            raw = resp.read()
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as e:
        raise ConnectionError(f"API unavailable: {e}") from e

    try:
        data = json.loads(raw.decode("utf-8"))
    except Exception as e:
        raise ValueError("Invalid JSON") from e

    if "Valute" not in data:
        raise KeyError("Valute")

    valute = data["Valute"]
    if not isinstance(valute, dict):
        raise TypeError("Valute must be a dict")

    result = {}
    for code in currency_codes:
        if code not in valute:
            raise KeyError(code)

        item = valute[code]
        if not isinstance(item, dict) or "Value" not in item:
            raise KeyError(f"{code}.Value")

        value = item["Value"]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{code}.Value must be int/float")

        result[code] = float(value)

    return result
