class Currency:
    def __init__(self, id: int, num_code: str, char_code: str, name: str, value: float, nominal: int = 1):
        self.id = id
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Currency.id must be a positive int")
        self._id = value

    @property
    def num_code(self) -> str:
        return self._num_code

    @num_code.setter
    def num_code(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Currency.num_code must be a non-empty string")
        self._num_code = value.strip()

    @property
    def char_code(self) -> str:
        return self._char_code

    @char_code.setter
    def char_code(self, value: str):
        if not isinstance(value, str) or not value.strip() or len(value.strip()) != 3:
            raise ValueError("Currency.char_code must be a 3-letter code")
        self._char_code = value.strip().upper()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Currency.name must be a non-empty string")
        self._name = value.strip()

    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Currency.value must be int/float")
        if float(value) <= 0:
            raise ValueError("Currency.value must be > 0")
        self._value = float(value)

    @property
    def nominal(self) -> int:
        return self._nominal

    @nominal.setter
    def nominal(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Currency.nominal must be a positive int")
        self._nominal = value
