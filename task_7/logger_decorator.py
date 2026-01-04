import sys
import logging
import functools
from datetime import datetime
from dataclasses import dataclass
from typing import Any, Optional


@dataclass(frozen=True)
class LogResult:
    level: str         
    value: Any
    message: Optional[str] = None


def logger(func=None, *, handle=sys.stdout):
    """
    Параметризуемый декоратор.

    - handle is logging.Logger -> uses info/warning/error/critical
    - else -> uses handle.write()

    Логирует:
      INFO: start + args/kwargs
      INFO: success + result
      ERROR: exception type + text, then re-raise

    Дополнительно:
      если функция вернула LogResult(level=..., value=..., message=...),
      то уровень берём из LogResult.level (например WARNING/CRITICAL),
      а наружу возвращаем LogResult.value.
    """
    def is_logging_logger(obj) -> bool:
        return isinstance(obj, logging.Logger)

    def emit(level: str, msg: str):
        ts = datetime.now().isoformat(timespec="seconds")
        line = f"{ts} {level} {msg}\n"

        if is_logging_logger(handle):
            if level == "INFO":
                handle.info(msg)
            elif level == "WARNING":
                handle.warning(msg)
            elif level == "ERROR":
                handle.error(msg)
            elif level == "CRITICAL":
                handle.critical(msg)
            else:
                handle.info(msg)
        else:
            handle.write(line)

    def decorator(target_func):
        @functools.wraps(target_func)
        def wrapper(*args, **kwargs):
            emit("INFO", f"CALL {target_func.__name__} args={args} kwargs={kwargs}")
            try:
                result = target_func(*args, **kwargs)
                if isinstance(result, LogResult):
                    lvl = result.level.upper()
                    msg = result.message or f"{target_func.__name__} returned LogResult"
                    emit(lvl, f"{target_func.__name__}: {msg} value={result.value!r}")
                    return result.value

                emit("INFO", f"OK   {target_func.__name__} result={result!r}")
                return result
            except Exception as e:
                emit("ERROR", f"FAIL {target_func.__name__} {type(e).__name__}: {e}")
                raise
        return wrapper

    if func is None:
        return decorator
    return decorator(func)
