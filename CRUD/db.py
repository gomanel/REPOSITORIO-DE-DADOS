import os
from contextlib import contextmanager
from typing import Any, Dict, Iterable, List, Optional, Tuple

import mysql.connector
from mysql.connector import MySQLConnection, Error
from dotenv import load_dotenv

load_dotenv()  

class Database:
    def __init__(self,
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 user: Optional[str] = None,
                 password: Optional[str] = None,
                 database: Optional[str] = None):
        self.host = host or os.getenv("DB_HOST", "127.0.0.1")
        self.port = int(port or os.getenv("DB_PORT", 3306))
        self.user = user or os.getenv("DB_USER", "root")
        self.password = password or os.getenv("DB_PASSWORD", "")
        self.database = database or os.getenv("DB_NAME", "biblioteca")
        self._conn: Optional[MySQLConnection] = None

    def connect(self) -> None:
        if self._conn and self._conn.is_connected():
            return
        self._conn = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            autocommit=False,
        )

    def disconnect(self) -> None:
        if self._conn and self._conn.is_connected():
            self._conn.close()
            self._conn = None

    @property
    def conn(self) -> MySQLConnection:
        if not self._conn or not self._conn.is_connected():
            self.connect()
        assert self._conn is not None
        return self._conn

    def execute(self, sql: str, params: Optional[Tuple[Any, ...]] = None) -> int:
        """Executa INSERT/UPDATE/DELETE. Retorna número de linhas afetadas."""
        cur = self.conn.cursor()
        cur.execute(sql, params or ())
        affected = cur.rowcount
        cur.close()
        return affected

    def executemany(self, sql: str, seq_of_params: Iterable[Tuple[Any, ...]]) -> int:
        cur = self.conn.cursor()
        cur.executemany(sql, list(seq_of_params))
        affected = cur.rowcount
        cur.close()
        return affected

    def query(self, sql: str, params: Optional[Tuple[Any, ...]] = None) -> List[Tuple]:
        cur = self.conn.cursor()
        cur.execute(sql, params or ())
        rows = cur.fetchall()
        cur.close()
        return rows

    def lastrowid(self) -> int:
        cur = self.conn.cursor()
        cur.execute("SELECT LAST_INSERT_ID()")
        last_id = cur.fetchone()[0]
        cur.close()
        return last_id

    @contextmanager
    def transaction(self):
        try:
            yield self
            self.conn.commit()
        except Exception:
            self.conn.rollback()
            raise
