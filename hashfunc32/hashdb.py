import os
import sqlite3
from typing import Dict, List, Tuple

from .utils import get_logger

logger = get_logger("database")

class HashDB:
    __TABLE_NAME = "hashdb"

    def __init__(self, db_name: str, db_folder: str = "./") -> None:
        self.db_path = os.path.join(db_folder, db_name)
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.__create_table()

    def __create_table(self):
        self.cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{self.__TABLE_NAME}';")
        if (self.cursor.fetchone()[0] == 0):
            self.cursor.execute(f"CREATE TABLE {self.__TABLE_NAME}(id INTEGER PRIMARY KEY, hash_value INTEGER, hash_str TEXT);")
            self.connection.commit()
    
    def close(self):
        self.cursor.close()
        self.connection.close()

    def add_hash_table_to_database(self, hash_table: Dict[int, List[str]]):
        records: List[Tuple[int, str]] = []
        for hash_value, hash_keys in hash_table.items():
            for hash_key in hash_keys:
                records.append((hash_value, hash_key))

        self.cursor.executemany(f"INSERT INTO {self.__TABLE_NAME}(hash_value, hash_str) VALUES(?, ?);", records)
        self.connection.commit()
        logger.debug("Inserted %d values into %s", len(records), self.db_path)

    def fetch_hash_from_table(self, hash_value: int) -> List[str]:
        self.cursor.execute(f"SELECT hash_str FROM {self.__TABLE_NAME} WHERE hash_value=?;", (hash_value,))
        fetched = self.cursor.fetchall()
        logger.debug("Found %d values from %s", len(fetched), self.db_path)
        return [c[0] for c in fetched]
