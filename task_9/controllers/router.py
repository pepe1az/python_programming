from typing import Dict, Tuple, List, Any


def _first(query: Dict[str, List[str]], key: str, default: str = "") -> str:
    vals = query.get(key)
    return vals[0] if vals else default


class Router:
    def __init__(self, pages, currency_controller, user_controller, author_info: Dict[str, Any]):
        self.pages = pages
        self.currency_controller = currency_controller
        self.user_controller = user_controller
        self.author_info = author_info

    def _response(self, status: int, body: bytes, headers: List[Tuple[str, str]] | None = None):
        hdrs = headers or []
        hdrs.append(("Content-Type", "text/html; charset=utf-8"))
        hdrs.append(("Content-Length", str(len(body))))
        return status, hdrs, body

    def _text(self, status: int, text: str):
        body = text.encode("utf-8")
        return self._response(status, body, headers=[("Content-Type", "text/plain; charset=utf-8")])

    def _redirect(self, location: str):
        body = b""
        headers = [("Location", location), ("Content-Length", "0")]
        return 302, headers, body

    def dispatch(self, path: str, query: Dict[str, List[str]]):
        if path == "/":
            currencies = self.currency_controller.list_currencies()
            body = self.pages.index(self.author_info, currencies)
            return self._response(200, body)

        if path == "/author":
            body = self.pages.author_page(self.author_info)
            return self._response(200, body)

        if path == "/users":
            users = self.user_controller.list_users()
            body = self.pages.users_page(users)
            return self._response(200, body)

        if path == "/user":
            user_id = _first(query, "id", "")
            if not user_id.isdigit():
                return self._text(400, "Bad Request: missing or invalid id")
            user = self.user_controller.get_user(int(user_id))
            if not user:
                return self._text(404, "User not found")
            currencies = self.user_controller.get_user_currencies(int(user_id))
            body = self.pages.user_page(user, currencies)
            return self._response(200, body)

        if path == "/currencies":
            currencies = self.currency_controller.list_currencies()
            body = self.pages.currencies_page(currencies)
            return self._response(200, body)

        if path == "/currency/delete":
            cid = _first(query, "id", "")
            if not cid.isdigit():
                return self._text(400, "Bad Request: missing or invalid id")
            self.currency_controller.delete_currency(int(cid))
            return self._redirect("/currencies")

        if path == "/currency/update":
            if not query:
                return self._text(400, "Bad Request: missing query like ?USD=99.9")

            code = next(iter(query.keys()))
            value_str = _first(query, code, "")
            try:
                value = float(value_str)
            except ValueError:
                return self._text(400, "Bad Request: value must be float")

            self.currency_controller.update_currency(code, value)
            return self._redirect("/currencies")

        if path == "/currency/show":
            currencies = self.currency_controller.list_currencies()
            print("CURRENCIES:", currencies)
            return self._text(200, "OK (printed to console)")

        return self._text(404, "Not Found")
