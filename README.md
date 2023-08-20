# hashfunc32

Search WinAPI func and lib hashes by malware hashfuncs.

## Code examples

```python
from hashfunc32 import HashHandler
from zlib import crc32

def hashfunc(data: str) -> int:
    return crc32(data.encode('utf-8'))

if __name__ == "__main__":
    hash_handler = HashHandler(hashfunc)
    hash_handler.init()
    print(hash_handler.find_hash(1069661581))
    # ['LoadLibraryA']
```

## Commands

Database file gewnerating when called `hash_handler.init()`

Database name will be `<func_name>.sqlite3`. You can change dir by passing second argument to `HashHandler` `.ctor`

`winhash <db_path> <hash_value>`

```
winhash ./hashfunc.sqlite3 1069661581
# ['LoadLibraryA']
```