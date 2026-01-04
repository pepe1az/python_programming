class Author:
    def __init__(self, name: str, group: str):
        self.name = name
        self.group = group

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Author.name must be a non-empty string")
        self._name = value.strip()

    @property
    def group(self) -> str:
        return self._group

    @group.setter
    def group(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Author.group must be a non-empty string")
        self._group = value.strip()
