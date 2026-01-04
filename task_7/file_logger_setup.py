import logging
from logger_decorator import logger
from currencies import get_currencies

file_logger = logging.getLogger("currency_file")
file_logger.setLevel(logging.INFO)

if not any(isinstance(h, logging.FileHandler) for h in file_logger.handlers):
    fh = logging.FileHandler("currency.log", encoding="utf-8")
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    fh.setFormatter(fmt)
    file_logger.addHandler(fh)

get_currencies_file_logged = logger(handle=file_logger)(get_currencies)

if __name__ == "__main__":
    print(get_currencies_file_logged(["USD", "EUR"]))
    print("written to currency.log")
