import sqlite3
from threading import Lock
import logging

logger = logging.getLogger(__name__)

class Database:
    _instance = None
    _lock = Lock()

    def __new__(cls, db="database/staff.db"):
        # 防止多開連線，只會創建一個實例
        with cls._lock:
            if cls._instance is None:
                cls._instance = object.__new__(cls)
                cls._instance.conn = sqlite3.connect(db)
                cls._instance.conn.row_factory = sqlite3.Row
                logger.info("已創建資料庫連線")


        return cls._instance

    def execute(self, sql, params=(), one: bool=False):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        result = cur.fetchone() if one else cur.fetchall()
        return result
    
    def commit(self):
        self.conn.commit()
