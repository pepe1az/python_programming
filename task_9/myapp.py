import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from jinja2 import Environment, FileSystemLoader, select_autoescape

from controllers.databasecontroller import init_db, CurrencyRatesCRUD, UsersCRUD, UserCurrencyCRUD
from controllers.currencycontroller import CurrencyController
from controllers.usercontroller import UserController
from controllers.pages import PagesController
from controllers.router import Router


def seed_data(conn: sqlite3.Connection) -> None:
    currency_db = CurrencyRatesCRUD(conn)
    users_db = UsersCRUD(conn)
    user_currency_db = UserCurrencyCRUD(conn)

    data = [
        {"num_code": "840", "char_code": "USD", "name": "Доллар США", "value": 90.0, "nominal": 1},
        {"num_code": "978", "char_code": "EUR", "name": "Евро", "value": 91.0, "nominal": 1},
        {"num_code": "826", "char_code": "GBP", "name": "Фунт стерлингов", "value": 105.0, "nominal": 1},
    ]
    currency_db._create_many(data)

    u1 = users_db._create("Alice")
    u2 = users_db._create("Bob")

    usd = currency_db._read_by_char_code("USD")["id"]
    eur = currency_db._read_by_char_code("EUR")["id"]
    gbp = currency_db._read_by_char_code("GBP")["id"]

    user_currency_db._subscribe(u1, usd)
    user_currency_db._subscribe(u1, eur)
    user_currency_db._subscribe(u2, gbp)


def build_app():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row

    init_db(conn)
    seed_data(conn)

    env = Environment(
        loader=FileSystemLoader("templates"),
        autoescape=select_autoescape(["html", "xml"]),
    )

    currency_db = CurrencyRatesCRUD(conn)
    users_db = UsersCRUD(conn)
    user_currency_db = UserCurrencyCRUD(conn)

    currency_controller = CurrencyController(currency_db)
    user_controller = UserController(users_db, user_currency_db)

    pages = PagesController(env)

    author_info = {
        "name": "Коряушкин Кирилл",     
        "group": "P4150",    
        "login": "pepe1az"         
    }

    router = Router(pages, currency_controller, user_controller, author_info)
    return router


ROUTER = build_app()


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)  

        status, headers, body = ROUTER.dispatch(path, query)

        self.send_response(status)
        for k, v in headers:
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        super().log_message(format, *args)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), AppHandler)
    print("Server started: http://127.0.0.1:8000")
    server.serve_forever()
