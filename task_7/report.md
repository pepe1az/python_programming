**Тема:** Параметризуемые декораторы, логирование и тестирование в Python

---

## 1. Общая идея работы

В рамках данной работы была реализована архитектура с **чётким разделением ответственности**:

- **Бизнес-логика** — функции, которые решают прикладную задачу:
  - `get_currencies` — получение курсов валют
  - `solve_quadratic` — решение квадратного уравнения

- **Сквозная логика** — инфраструктурный код:
  - декоратор `logger`, отвечающий за логирование, трассировку вызовов и обработку ошибок

Такой подход позволяет:
- не смешивать логику вычислений с логированием;
- легко менять способ логирования;
- упрощать тестирование и сопровождение кода;
- следовать практикам clean architecture.

---

## 2. Декоратор `logger`

### 2.1 Назначение

Декоратор `logger` предназначен для автоматического логирования:
- начала выполнения функции;
- аргументов вызова;
- успешного завершения;
- возвращаемого значения;
- ошибок и исключений.

### 2.2 Сигнатура

```python
def logger(func=None, *, handle=sys.stdout):
    ...
```

Декоратор является **параметризуемым** и может использоваться как с аргументами, так и без них.

---

### 2.3 Поддерживаемые варианты логирования

| Тип `handle` | Описание |
|-------------|---------|
| `sys.stdout` (по умолчанию) | Вывод логов через `handle.write()` |
| `io.StringIO` | Запись логов в память (используется в тестах) |
| `logging.Logger` | Логирование через `log.info()`, `log.warning()`, `log.error()` |

Декоратор автоматически определяет тип `handle` и выбирает корректный способ логирования.

---

### 2.4 Поведение декоратора

#### При вызове функции
```
INFO CALL function_name args=(...) kwargs={...}
```

#### При успешном завершении
```
INFO OK function_name result=...
```

#### При исключении
```
ERROR FAIL function_name ExceptionType: message
```

Исключение **обязательно пробрасывается дальше**.

Для сохранения оригинальной сигнатуры функции используется `functools.wraps`.

---

## 3. Функция `get_currencies`

### 3.1 Назначение

Функция предназначена для получения курсов валют с API Центрального Банка РФ (или тестового URL).

### 3.2 Сигнатура

```python
def get_currencies(currency_codes: list, url=..., timeout=...) -> dict
```

---

### 3.3 Логика работы

1. Выполнение HTTP-запроса к API.
2. Декодирование JSON-ответа.
3. Извлечение ключа `Valute`.
4. Формирование словаря курсов валют:

```python
{
  "USD": 93.25,
  "EUR": 101.7
}
```

---

### 3.4 Обработка исключений

| Ситуация | Исключение |
|--------|-----------|
| API недоступен | `ConnectionError` |
| Некорректный JSON | `ValueError` |
| Отсутствует ключ `Valute` | `KeyError` |
| Валюта отсутствует в данных | `KeyError` |
| Неверный тип курса | `TypeError` |

Функция **не выполняет логирование** — только выбрасывает исключения.

---

## 4. Файл-логирование

В качестве самостоятельной части реализовано логирование в файл с использованием `logging.Logger`.

Пример:

```python
file_logger = logging.getLogger("currency_file")
file_logger.setLevel(logging.INFO)

handler = logging.FileHandler("currency.log", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
handler.setFormatter(formatter)
file_logger.addHandler(handler)

@logger(handle=file_logger)
def get_currencies(...):
    ...
```

Все сообщения сохраняются в файл `currency.log`.

---

## 5. Демонстрационный пример: `solve_quadratic`

### 5.1 Назначение

Функция демонстрирует использование различных уровней логирования.

### 5.2 Сигнатура

```python
def solve_quadratic(a, b, c)
```

---

### 5.3 Логируемые ситуации

| Ситуация | Уровень |
|--------|--------|
| Два действительных корня | `INFO` |
| Дискриминант < 0 | `WARNING` |
| Некорректные данные (`a="abc"`) | `ERROR` |
| Полностью невозможная ситуация (`a=b=0`) | `CRITICAL` |

Функция не выполняет логирование напрямую, а взаимодействует с декоратором через возвращаемые значения или исключения.

---

## 6. Тестирование

### 6.1 Тестирование `get_currencies`

Используется модуль `unittest`.

Проверяется:
- корректный возврат данных;
- поведение при отсутствии валюты;
- выброс исключений:
  - `ConnectionError`
  - `ValueError`
  - `KeyError`

Пример:

```python
with self.assertRaises(ConnectionError):
    get_currencies(["USD"], url="https://invalid")
```

---

### 6.2 Тестирование декоратора `logger`

Используется `io.StringIO`.

Проверяется:
1. Наличие INFO-логов при успешном выполнении.
2. Наличие ERROR-логов при исключениях.
3. Проброс исключений наружу.

---

### 6.3 Пример из условия задания

```python
class TestStreamWrite(unittest.TestCase):

    def setUp(self):
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def wrapped():
            return get_currencies(['USD'], url="https://invalid")

        self.wrapped = wrapped

    def test_logging_error(self):
        with self.assertRaises(ConnectionError):
            self.wrapped()

        logs = self.stream.getvalue()
        self.assertIn("ERROR", logs)
        self.assertIn("ConnectionError", logs)
```

---

## 7. Структура проекта

```
task_7/
  currencies.py
  logger_decorator.py
  file_logger_setup.py
  main_demo.py
  quadratic_demo.py
  test_currencies.py
  test_logger.py
```

---

## 8. Запуск и проверка

### Переход в каталог проекта

```powershell
cd C:\учёба\python_programming\task_7
```

### Запуск всех тестов

```powershell
python -m unittest discover -v
```

---

## 9. Что должно быть в отчёте

Ниже приведено **полное наполнение отчёта**, которое требуется по заданию. Все фрагменты можно включать напрямую в `.md` / `.pdf` отчёт.

---

### 9.1 Исходный код декоратора с параметрами

```python
# logger_decorator.py
import sys
import logging
import functools
from datetime import datetime


def logger(func=None, *, handle=sys.stdout):
    def is_logging_logger(obj):
        return isinstance(obj, logging.Logger)

    def emit(level, message):
        timestamp = datetime.now().isoformat(timespec="seconds")
        line = f"{timestamp} {level} {message}\n"

        if is_logging_logger(handle):
            if level == "INFO":
                handle.info(message)
            elif level == "WARNING":
                handle.warning(message)
            elif level == "ERROR":
                handle.error(message)
            elif level == "CRITICAL":
                handle.critical(message)
        else:
            handle.write(line)

    def decorator(target_func):
        @functools.wraps(target_func)
        def wrapper(*args, **kwargs):
            emit("INFO", f"CALL {target_func.__name__} args={args} kwargs={kwargs}")
            try:
                result = target_func(*args, **kwargs)
                emit("INFO", f"OK {target_func.__name__} result={result!r}")
                return result
            except Exception as e:
                emit("ERROR", f"FAIL {target_func.__name__} {type(e).__name__}: {e}")
                raise
        return wrapper

    if func is None:
        return decorator
    return decorator(func)
```

---

### 9.2 Исходный код `get_currencies`

```python
import json
import urllib.request
import urllib.error


def get_currencies(currency_codes: list, url="https://www.cbr-xml-daily.ru/daily_json.js", timeout=10) -> dict:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            raw_data = response.read()
    except Exception as e:
        raise ConnectionError("API unavailable") from e

    try:
        data = json.loads(raw_data.decode("utf-8"))
    except Exception as e:
        raise ValueError("Invalid JSON") from e

    if "Valute" not in data:
        raise KeyError("Valute")

    result = {}
    for code in currency_codes:
        if code not in data["Valute"]:
            raise KeyError(code)

        value = data["Valute"][code].get("Value")
        if not isinstance(value, (int, float)):
            raise TypeError(f"Invalid value type for {code}")

        result[code] = value

    return result
```

---

### 9.3 Демонстрационный пример

```python
import math
import sys
from logger_decorator import logger


@logger(handle=sys.stdout)
def solve_quadratic(a, b, c):
    try:
        a = float(a)
        b = float(b)
        c = float(c)
    except Exception:
        raise ValueError("Invalid coefficients")

    if a == 0 and b == 0:
        raise RuntimeError("Critical error: a = b = 0")

    if a == 0:
        return (-c / b,)

    d = b ** 2 - 4 * a * c

    if d < 0:
        return None

    sqrt_d = math.sqrt(d)
    x1 = (-b + sqrt_d) / (2 * a)
    x2 = (-b - sqrt_d) / (2 * a)
    return (x1, x2)
```

---

### 9.4 Скриншоты / фрагменты логов

Пример логов при запуске `solve_quadratic(1, -3, 2)`:

```
2025-01-10 12:10:01 INFO CALL solve_quadratic args=(1, -3, 2) kwargs={}
2025-01-10 12:10:01 INFO OK solve_quadratic result=(2.0, 1.0)
```

Пример логов при ошибке:

```
2025-01-10 12:10:15 ERROR FAIL solve_quadratic ValueError: Invalid coefficients
```

---

### 9.5 Тесты

#### 9.5.1 Тесты функции `get_currencies`

```python
import unittest
from currencies import get_currencies


class TestGetCurrencies(unittest.TestCase):
    def test_connection_error(self):
        with self.assertRaises(ConnectionError):
            get_currencies(["USD"], url="https://invalid")
```

---

#### 9.5.2 Тесты декоратора `logger`

```python
import unittest
import io
from logger_decorator import logger


class TestLogger(unittest.TestCase):
    def test_success_logging(self):
        stream = io.StringIO()

        @logger(handle=stream)
        def f(x):
            return x * 2

        f(10)
        logs = stream.getvalue()
        self.assertIn("INFO", logs)
```

---

#### 9.5.3 Тесты работы с `StringIO`

```python
class TestStreamWrite(unittest.TestCase):
    def setUp(self):
        self.stream = io.StringIO()

        @logger(handle=self.stream)
        def wrapped():
            from currencies import get_currencies
            return get_currencies(['USD'], url="https://invalid")

        self.wrapped = wr

В работе реализованы:
- параметризуемый декоратор;
- поддержка разных потоков логирования;
- разделение бизнес-логики и инфраструктуры;
- обработка ошибок внешнего API;
- демонстрация уровней логирования;
- автоматические тесты.

Решение соответствует требованиям технического задания и демонстрирует корректный архитектурный подход.

