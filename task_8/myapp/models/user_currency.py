class UserCurrency:
    def __init__(self, id: int, user_id: int, currency_id: int):
        self.id = id
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("UserCurrency.id must be a positive int")
        self._id = value

    @property
    def user_id(self) -> int:
        return self._user_id

    @user_id.setter
    def user_id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("UserCurrency.user_id must be a positive int")
        self._user_id = value

    @property
    def currency_id(self) -> int:
        return self._currency_id

    @currency_id.setter
    def currency_id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("UserCurrency.currency_id must be a positive int")
        self._currency_id = value
