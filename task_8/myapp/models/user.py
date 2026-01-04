class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("User.id must be a positive int")
        self._id = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("User.name must be a non-empty string")
        self._name = value.strip()
