from controllers.databasecontroller import CurrencyRatesCRUD


class CurrencyController:
    def __init__(self, db_controller: CurrencyRatesCRUD):
        self.db = db_controller

    def list_currencies(self):
        return self.db._read()

    def update_currency(self, char_code: str, value: float):
        code = str(char_code).upper()
        return self.db._update({code: float(value)})

    def delete_currency(self, currency_id: int):
        return self.db._delete(int(currency_id))
