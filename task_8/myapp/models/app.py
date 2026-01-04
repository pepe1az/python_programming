from .author import Author

class App:
    def __init__(self, name: str, version: str, author: Author):
        self.name = name
        self.version = version
        self.author = author

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("App.name must be a non-empty string")
        self._name = value.strip()

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("App.version must be a non-empty string")
        self._version = value.strip()

    @property
    def author(self) -> Author:
        return self._author

    @author.setter
    def author(self, value: Author):
        if not isinstance(value, Author):
            raise TypeError("App.author must be an Author")
        self._author = value
