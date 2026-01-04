# Отчёт по работе
**Тема:** Реализация CRUD с использованием SQLite (:memory:), архитектуры MVC и тестирования с unittest.mock

## 1. Цель работы

Целью данной работы является:

- реализация CRUD (Create, Read, Update, Delete) для сущностей бизнес-логики приложения;
- освоение работы с базой данных SQLite в памяти (`sqlite3.connect(':memory:')`);
- изучение принципов первичных (PRIMARY KEY) и внешних ключей (FOREIGN KEY);
- применение архитектуры MVC (Model–View–Controller);
- разделение ответственности между моделями, контроллерами и представлениями;
- реализация роутера для обработки GET-запросов;
- отображение валют и валют, на которые подписан пользователь;
- тестирование бизнес-логики с использованием `unittest.mock`.

---

## 2. Краткое описание приложения

Разработано веб-приложение на Python с использованием встроенного HTTP-сервера.
Приложение позволяет:

- просматривать список валют;
- обновлять курс валюты по её символьному коду;
- удалять валюты;
- просматривать список пользователей;
- просматривать пользователя и валюты, на которые он подписан.

Все данные хранятся в базе SQLite, размещённой в оперативной памяти.

---

## 3. Структура базы данных

### Таблица `user`

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL
);

Таблица содержит информацию о пользователях.

---

### Таблица `currency`

CREATE TABLE currency (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  num_code TEXT NOT NULL,
  char_code TEXT NOT NULL,
  name TEXT NOT NULL,
  value FLOAT,
  nominal INTEGER
);

Таблица хранит информацию о валютах и их курсах.

---

### Таблица `user_currency`

CREATE TABLE user_currency (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  currency_id INTEGER NOT NULL,
  FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE,
  FOREIGN KEY(currency_id) REFERENCES currency(id) ON DELETE CASCADE
);

Таблица реализует связь многие-ко-многим между пользователями и валютами.

---

## 4. PRIMARY KEY и FOREIGN KEY

### PRIMARY KEY

Первичный ключ (PRIMARY KEY) используется для уникальной идентификации каждой записи в таблице.
В работе применяется поле `id INTEGER PRIMARY KEY AUTOINCREMENT`.

Назначение:
- уникальная идентификация записей;
- ускорение поиска данных;
- возможность связывать таблицы между собой.

---

### FOREIGN KEY

Внешний ключ (FOREIGN KEY) используется для задания связи между таблицами.
В таблице `user_currency` поля `user_id` и `currency_id` ссылаются на таблицы `user` и `currency`.

Назначение:
- обеспечение ссылочной целостности;
- предотвращение удаления используемых данных;
- формирование логических связей между сущностями.

---

## 5. Архитектура MVC

### Model

Модели располагаются в каталоге `models/` и содержат:
- описание сущностей (`Currency`, `User`);
- геттеры и сеттеры;
- валидацию данных.

Модели не содержат SQL-запросов и логики отображения.

---

### Controller

Контроллеры находятся в каталоге `controllers/` и разделены по ответственности:

- `databasecontroller.py` — работа с SQLite и реализация CRUD;
- `currencycontroller.py` — бизнес-логика валют;
- `usercontroller.py` — бизнес-логика пользователей;
- `pages.py` — рендеринг HTML-страниц;
- `router.py` — маршрутизация HTTP-запросов.

---

### View

Представления реализованы с использованием шаблонов Jinja2 и размещены в каталоге `templates/`.

---

## 6. Структура проекта

myapp/
  myapp.py
  controllers/
    databasecontroller.py
    currencycontroller.py
    usercontroller.py
    pages.py
    router.py
  models/
    currency.py
    user.py
  templates/
    index.html
    author.html
    users.html
    user.html
    currencies.html
  tests/
    test_currency_controller.py
    test_user_controller.py

---

## 7. Реализация CRUD для Currency

### Create

INSERT INTO currency(num_code, char_code, name, value, nominal)
VALUES(:num_code, :char_code, :name, :value, :nominal);

---

### Read

SELECT id, num_code, char_code, name, value, nominal
FROM currency;

---

### Update

UPDATE currency SET value = ? WHERE char_code = ?;

---

### Delete

DELETE FROM currency WHERE id = ?;

---

## 8. Маршруты приложения

- `/` — главная страница
- `/author` — информация об авторе
- `/users` — список пользователей
- `/user?id=...` — пользователь и его валюты
- `/currencies` — список валют
- `/currency/update?USD=...` — обновление курса
- `/currency/delete?id=...` — удаление валюты
- `/currency/show` — отладочный вывод

---

## 9. Отображение валют пользователя

SELECT c.*
FROM currency c
JOIN user_currency uc ON uc.currency_id = c.id
WHERE uc.user_id = ?;

---

## 10. Тестирование с unittest.mock

Для тестирования бизнес-логики используются mock-объекты, позволяющие изолировать контроллеры от реальной базы данных.

---

## 11. Скриншоты работы приложения

В отчёт включены скриншоты:
- главной страницы;
- таблицы валют;
- обновления курса валюты;
- удаления валюты;
- страницы пользователя с подписками.

---

## 12. Выводы

В ходе выполнения работы:
- реализован CRUD для сущности `currency`;
- изучена работа с SQLite в памяти;
- реализованы связи между таблицами с использованием PRIMARY KEY и FOREIGN KEY;
- применена архитектура MVC;
- реализован HTTP-роутер для обработки GET-запросов;
- выполнено тестирование бизнес-логики с использованием `unittest.mock`.
