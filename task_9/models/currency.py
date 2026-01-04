class Currency:
    def __init__(self, num_code: str, char_code: str, name: str, value: float, nominal: int):
        self.__num_code = num_code
        self.char_code = char_code  
        self.__name = name
        self.value = value          
        self.__nominal = nominal

    @property
    def num_code(self):
        return self.__num_code

    @property
    def char_code(self):
        return self.__char_code

    @char_code.setter
    def char_code(self, val: str):
        if not isinstance(val, str) or len(val.strip()) != 3:
            raise ValueError("Код валюты должен состоять из 3 символов")
        self.__char_code = val.strip().upper()

    @property
    def name(self):
        return self.__name

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val: float):
        if val is None:
            self.__value = None
            return
        v = float(val)
        if v < 0:
            raise ValueError("Курс валюты не может быть отрицательным")
        self.__value = v

    @property
    def nominal(self):
        return self.__nominal
