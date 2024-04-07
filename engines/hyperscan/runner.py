import hyperscan as hs
from typing import Any, Optional
import timeit

# A truthy return value signifies to stop matching
def on_match(
    id: int, from_: int, to: int, flags: int, context: Optional[Any] = None
) -> Optional[bool]:
    print(f"Matched pattern {id} from {from_} to {to}")
    print(f"Flags: {flags}")
    print(f"Context: {context}")


# Caveat: this uses Vectorscan rather than Hyperscan, but the two are similar
db = hs.Database(mode=hs.HS_MODE_BLOCK)
patterns = (
    (rb"foo", 0),
    (rb"bar", 1),
)

expressions, ids = zip(*patterns)
db.compile(expressions=expressions, ids=ids, elements=len(patterns))
print(db.info().decode())

# BLOCK MODE
print(db.scan(b"foo", match_event_handler=on_match, context="foo"))

print()

# STREAM MODE
db = hs.Database(mode=hs.HS_MODE_STREAM)
db.compile(expressions=expressions, ids=ids, elements=len(patterns))
with db.stream(match_event_handler=on_match, context=2345) as stream:
    stream.scan(b"foo")
    stream.scan(b"bar")

print()

# VECTOR MODE
db = hs.Database(mode=hs.HS_MODE_VECTORED)
buffers = [
    bytearray(b'xxxfooxxx'),
    bytearray(b'xxfoxbarx'),
    bytearray(b'barxxxxxx'),
]
db.compile(expressions=expressions, ids=ids, elements=len(patterns))
db.scan(buffers, match_event_handler=on_match)