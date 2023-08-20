import os
import click
from .hashdb import HashDB

def get_database(db_path) -> HashDB:
        db_dir, db_name = os.path.split(db_path)
        return HashDB(db_name, db_dir)

@click.argument("database_path")
@click.argument("hash_value", type=int)
def __winhash(database_path, hash_value):
    if not os.path.isfile(database_path):
        return
    hash_db = get_database(database_path)
    print(hash_db.fetch_hash_from_table(hash_value))
    hash_db.close()

def winhash():
    click.command(__winhash)()