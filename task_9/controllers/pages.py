from typing import Any


class PagesController:
    def __init__(self, env):
        self.env = env

    def render(self, template_name: str, **context: Any) -> bytes:
        tpl = self.env.get_template(template_name)
        html = tpl.render(**context)
        return html.encode("utf-8")

    def index(self, author: dict, currencies: list) -> bytes:
        return self.render("index.html", author=author, currencies=currencies)

    def author_page(self, author: dict) -> bytes:
        return self.render("author.html", author=author)

    def users_page(self, users: list) -> bytes:
        return self.render("users.html", users=users)

    def user_page(self, user: dict, currencies: list) -> bytes:
        return self.render("user.html", user=user, currencies=currencies)

    def currencies_page(self, currencies: list) -> bytes:
        return self.render("currencies.html", currencies=currencies)
