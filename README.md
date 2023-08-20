# hashfunc32

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