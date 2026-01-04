class User:
    def __init__(self, name: str):
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, val: str):
        if not isinstance(val, str) or not val.strip():
            raise ValueError("Имя пользователя не может быть пустым")
        self.__name = val.strip()
