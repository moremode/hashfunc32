import os
from typing import Callable, Dict, List, Set, Tuple

from .utils import open_sys32, get_logger
from .hashdb import HashDB

logger = get_logger("handler")

class HashHandler:
    def __init__(self, hash_func: Callable[[str], int], db_dir: str = "./") -> None:
        self.hash_func = hash_func
        self.hash_table: Dict[int, Set[Tuple[str, str]]] = {}
        self.db_path = os.path.join(db_dir, hash_func.__name__ + ".sqlite3")
        logger.debug("Database path: %s", self.db_path)

    @property
    def hash_list(self) -> Dict[int, List[int]]:
        return {c1: list(c2) for c1, c2 in self.hash_table.items()}

    def __add_hash_to_table(self, namehash: int, name: Tuple[str, str]):
        if namehash not in self.hash_table:
            self.hash_table[namehash] = set()
        self.hash_table[namehash].add(name)

    def generate_hash_table(self):
        sys32 = open_sys32()
        for dllname, funcnames in sys32.items():
            dll_hash = self.hash_func(dllname)
            self.__add_hash_to_table(dll_hash, (dllname, "dllnames"))
            for funcname in funcnames:
                func_hash = self.hash_func(funcname)
                self.__add_hash_to_table(func_hash, (funcname, dllname))

    def has_database(self) -> bool:
        return os.path.isfile(self.db_path)

    def __get_database(self) -> HashDB:
        db_dir, db_name = os.path.split(self.db_path)
        return HashDB(db_name, db_dir)

    def create_db(self, rewrite: bool = False):
        if self.has_database():
            if not rewrite:
                logger.debug("Database already exists: Skiped")
                return
            os.remove(self.db_path)
            logger.debug("Database already exists: Rewriting")
        hash_db = self.__get_database()
        hash_db.add_hash_table_to_database(self.hash_list)
        hash_db.close()

    def find_hash(self, hash_value: int) -> Tuple[str, str]:
        if self.has_database():
            hash_db = self.__get_database()
            hash_strs = hash_db.fetch_hash_from_table(hash_value)
            hash_db.close()
            return hash_strs
        if hash_value in self.hash_table:
            return list(self.hash_table[hash_value])
        return []
    
    def __get_hashes_from_local_table(self):
        local_hashes: List[Tuple[str, str, str]] = []
        for hash_value, names in self.hash_table:
            local_hashes.append((hash_value, names[0], names[1]))
        return local_hashes

    def get_all_hashes(self):
        if self.has_database():
            hash_db = self.__get_database()
            hash_strs = hash_db.fetch_hashes_from_table()
            hash_db.close()
            return hash_strs
        return self.__get_hashes_from_local_table()
    
    def init(self):
        if not self.has_database():
            self.generate_hash_table()
            self.create_db()