from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os

from jinja2 import Environment, PackageLoader, select_autoescape

from myapp.models import Author, App, User, Currency, UserCurrency
from myapp.utils.currencies_api import get_currencies
from myapp.utils.history import RateHistory


env = Environment(
    loader=PackageLoader("myapp", "templates"),
    autoescape=select_autoescape()
)
template_index = env.get_template("index.html")
template_users = env.get_template("users.html")
template_user = env.get_template("user.html")
template_currencies = env.get_template("currencies.html")
template_author = env.get_template("author.html")


main_author = Author(name="Кирилл Коряушкин", group="P4150")
app_info = App(name="CurrenciesListApp", version="1.0.0", author=main_author)

USERS = [
    User(1, "Андрей"),
    User(2, "Акакий"),
]

CURRENCIES = [
    Currency(id=1, num_code="840", char_code="USD", name="US Dollar", value=1.0, nominal=1),
    Currency(id=2, num_code="978", char_code="EUR", name="Euro", value=1.0, nominal=1),
    Currency(id=3, num_code="826", char_code="GBP", name="British Pound", value=1.0, nominal=1),
]

USER_CURRENCIES = [
    UserCurrency(1, user_id=1, currency_id=1),  
    UserCurrency(2, user_id=1, currency_id=2),  
    UserCurrency(3, user_id=2, currency_id=1),  
]

HISTORY = RateHistory()


def find_user(user_id: int) -> User | None:
    for u in USERS:
        if u.id == user_id:
            return u
    return None


def find_currency_by_id(currency_id: int) -> Currency | None:
    for c in CURRENCIES:
        if c.id == currency_id:
            return c
    return None


def find_currency_by_code(code: str) -> Currency | None:
    for c in CURRENCIES:
        if c.char_code == code:
            return c
    return None


def user_subscriptions(user_id: int) -> list[Currency]:
    currency_ids = [uc.currency_id for uc in USER_CURRENCIES if uc.user_id == user_id]
    return [c for c in CURRENCIES if c.id in currency_ids]


def subscribe(user_id: int, currency_id: int):
    next_id = (max([uc.id for uc in USER_CURRENCIES]) + 1) if USER_CURRENCIES else 1
    for uc in USER_CURRENCIES:
        if uc.user_id == user_id and uc.currency_id == currency_id:
            return
    USER_CURRENCIES.append(UserCurrency(next_id, user_id=user_id, currency_id=currency_id))


def unsubscribe(user_id: int, currency_id: int):
    global USER_CURRENCIES
    USER_CURRENCIES = [uc for uc in USER_CURRENCIES if not (uc.user_id == user_id and uc.currency_id == currency_id)]


def update_rates():
    codes = [c.char_code for c in CURRENCIES]
    rates = get_currencies(codes)
    for code, value in rates.items():
        cur = find_currency_by_code(code)
        if cur:
            cur.value = value
            HISTORY.add(code, value)


class MyHandler(BaseHTTPRequestHandler):
    def _send_html(self, html: str, status: int = 200):
        body = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_json(self, obj, status: int = 200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _redirect(self, location: str):
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        if path.startswith("/static/"):
            return self._serve_static(path)

        if path == "/":
            html = template_index.render(
                app_name=app_info.name,
                app_version=app_info.version,
                author_name=app_info.author.name,
                group=app_info.author.group,
                navigation=self._nav()
            )
            return self._send_html(html)

        if path == "/author":
            html = template_author.render(
                author=app_info.author,
                navigation=self._nav()
            )
            return self._send_html(html)

        if path == "/users":
            html = template_users.render(
                users=USERS,
                navigation=self._nav()
            )
            return self._send_html(html)

        if path == "/user":
            if "id" not in query:
                return self._send_html("Missing id", status=400)
            try:
                user_id = int(query["id"][0])
            except ValueError:
                return self._send_html("Invalid id", status=400)

            user = find_user(user_id)
            if not user:
                return self._send_html("User not found", status=404)

            subs = user_subscriptions(user_id)
            chart = {}
            for cur in subs:
                points = HISTORY.last_n_days(cur.char_code, days=90)
                chart[cur.char_code] = [{"t": t.strftime("%Y-%m-%d"), "v": v} for (t, v) in points]

            html = template_user.render(
                user=user,
                subscriptions=subs,
                all_currencies=CURRENCIES,
                chart_data_json=json.dumps(chart, ensure_ascii=False),
                navigation=self._nav()
            )
            return self._send_html(html)

        if path == "/currencies":
            try:
                update_rates()
            except Exception as e:
                html = template_currencies.render(
                    currencies=CURRENCIES,
                    error=f"{type(e).__name__}: {e}",
                    navigation=self._nav()
                )
                return self._send_html(html, status=502)

            html = template_currencies.render(
                currencies=CURRENCIES,
                error=None,
                navigation=self._nav()
            )
            return self._send_html(html)

        if path == "/api/currencies":
            return self._send_json({
                "currencies": [
                    {"id": c.id, "code": c.char_code, "name": c.name, "value": c.value, "nominal": c.nominal}
                    for c in CURRENCIES
                ]
            })

        return self._send_html("Not found", status=404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/subscribe":
            try:
                user_id = int(query.get("user_id", ["0"])[0])
                currency_id = int(query.get("currency_id", ["0"])[0])
            except ValueError:
                return self._send_html("Invalid params", status=400)

            if not find_user(user_id) or not find_currency_by_id(currency_id):
                return self._send_html("User/Currency not found", status=404)

            subscribe(user_id, currency_id)
            return self._redirect(f"/user?id={user_id}")

        if path == "/unsubscribe":
            try:
                user_id = int(query.get("user_id", ["0"])[0])
                currency_id = int(query.get("currency_id", ["0"])[0])
            except ValueError:
                return self._send_html("Invalid params", status=400)

            unsubscribe(user_id, currency_id)
            return self._redirect(f"/user?id={user_id}")

        if path == "/update":
            try:
                update_rates()
            except Exception as e:
                return self._send_html(f"Update failed: {type(e).__name__}: {e}", status=502)
            return self._redirect("/currencies")

        return self._send_html("Not found", status=404)

    def _nav(self):
        return [
            {"caption": "Главная", "href": "/"},
            {"caption": "Пользователи", "href": "/users"},
            {"caption": "Валюты", "href": "/currencies"},
            {"caption": "Автор", "href": "/author"},
        ]

    def _serve_static(self, path: str):
        rel = path.lstrip("/")
        base_dir = os.path.dirname(__file__)
        fs_path = os.path.join(base_dir, rel.replace("/", os.sep))

        if not os.path.isfile(fs_path):
            return self._send_html("Static not found", status=404)

        with open(fs_path, "rb") as f:
            data = f.read()

        self.send_response(200)
        if fs_path.endswith(".css"):
            ctype = "text/css; charset=utf-8"
        elif fs_path.endswith(".js"):
            ctype = "application/javascript; charset=utf-8"
        else:
            ctype = "application/octet-stream"
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def run(host="127.0.0.1", port=8000):
    httpd = HTTPServer((host, port), MyHandler)
    print(f"Server started: http://{host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
