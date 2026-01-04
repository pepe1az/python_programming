import sys
import io
import logging

from logger_decorator import logger
from currencies import get_currencies

get_currencies_stdout = logger(handle=sys.stdout)(get_currencies)
stream = io.StringIO()
get_currencies_stream = logger(handle=stream)(get_currencies)
log = logging.getLogger("L1")
log.setLevel(logging.INFO)
log.addHandler(logging.StreamHandler(sys.stdout))
get_currencies_logging = logger(handle=log)(get_currencies)


if __name__ == "__main__":
    print(get_currencies_stdout(["USD", "EUR"]))
    print("---- StringIO logs ----")
    get_currencies_stream(["USD"])
    print(stream.getvalue())
    print("---- logging.Logger ----")
    print(get_currencies_logging(["USD"]))
