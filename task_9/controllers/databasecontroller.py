import sqlite3
from typing import Any, Dict, List, Optional


def init_db(conn: sqlite3.Connection) -> None:

    conn.execute("PRAGMA foreign_keys = ON;")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS currency (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        num_code TEXT NOT NULL,
        char_code TEXT NOT NULL,
        name TEXT NOT NULL,
        value FLOAT,
        nominal INTEGER
    );
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS user_currency (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        currency_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE,
        FOREIGN KEY(currency_id) REFERENCES currency(id) ON DELETE CASCADE
    );
    """)
    conn.commit()


def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    return {k: row[k] for k in row.keys()}


class CurrencyRatesCRUD:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def _create_many(self, data: List[Dict[str, Any]]) -> None:
        sql = """
        INSERT INTO currency(num_code, char_code, name, value, nominal)
        VALUES(:num_code, :char_code, :name, :value, :nominal)
        """
        cur = self.conn.cursor()
        cur.executemany(sql, data)
        self.conn.commit()

    def _create_one(self, data: Dict[str, Any]) -> int:
        sql = """
        INSERT INTO currency(num_code, char_code, name, value, nominal)
        VALUES(:num_code, :char_code, :name, :value, :nominal)
        """
        cur = self.conn.cursor()
        cur.execute(sql, data)
        self.conn.commit()
        return int(cur.lastrowid)

    def _read(self) -> List[Dict[str, Any]]:
        sql = "SELECT id, num_code, char_code, name, value, nominal FROM currency ORDER BY id"
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return [_row_to_dict(r) for r in rows]

    def _read_by_char_code(self, char_code: str) -> Optional[Dict[str, Any]]:
        sql = "SELECT id, num_code, char_code, name, value, nominal FROM currency WHERE char_code = ?"
        cur = self.conn.cursor()
        cur.execute(sql, (char_code,))
        row = cur.fetchone()
        return _row_to_dict(row) if row else None

    def _update(self, mapping: Dict[str, float]) -> int:
        """
        mapping вида {"USD": 99.9}
        Возвращает количество обновлённых строк.
        """
        updated = 0
        sql = "UPDATE currency SET value = ? WHERE char_code = ?"
        cur = self.conn.cursor()
        for code, value in mapping.items():
            cur.execute(sql, (float(value), str(code).upper()))
            updated += cur.rowcount
        self.conn.commit()
        return updated

    def _delete(self, currency_id: int) -> int:
        """
        Возвращает количество удалённых строк.
        """
        cur = self.conn.cursor()
        cur.execute("DELETE FROM currency WHERE id = ?", (int(currency_id),))
        self.conn.commit()
        return cur.rowcount


class UsersCRUD:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def _create(self, name: str) -> int:
        cur = self.conn.cursor()
        cur.execute("INSERT INTO user(name) VALUES(?)", (name,))
        self.conn.commit()
        return int(cur.lastrowid)

    def _read(self) -> List[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, name FROM user ORDER BY id")
        return [_row_to_dict(r) for r in cur.fetchall()]

    def _read_one(self, user_id: int) -> Optional[Dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, name FROM user WHERE id = ?", (int(user_id),))
        row = cur.fetchone()
        return _row_to_dict(row) if row else None


class UserCurrencyCRUD:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def _subscribe(self, user_id: int, currency_id: int) -> int:
        """
        Добавляет подписку user->currency.
        """
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO user_currency(user_id, currency_id) VALUES(?, ?)",
            (int(user_id), int(currency_id))
        )
        self.conn.commit()
        return int(cur.lastrowid)

    def _get_user_currencies(self, user_id: int) -> List[Dict[str, Any]]:
        sql = """
        SELECT c.id, c.num_code, c.char_code, c.name, c.value, c.nominal
        FROM currency c
        JOIN user_currency uc ON uc.currency_id = c.id
        WHERE uc.user_id = ?
        ORDER BY c.id
        """
        cur = self.conn.cursor()
        cur.execute(sql, (int(user_id),))
        return [_row_to_dict(r) for r in cur.fetchall()]
