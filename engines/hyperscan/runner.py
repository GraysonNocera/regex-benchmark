"""
Caveat: this uses Vectorscan rather than Hyperscan, but the two are similar. Vectorscan just broadens the available
architectures that can be used with Hyperscan.
should the CLI provide us with BLOCK, STREAM, or VECTOR mode?
Ideally, we would run the native C engine, but python binding is quicker to get up and running.
"""

import hyperscan as hs
from typing import Any, Optional
import timeit

haystack = "xxxxx=xxxxxx"
pattern = r'x=x'

# A truthy return value signifies to stop matching
def on_match(
    id: int, from_: int, to: int, flags: int, context: Optional[Any] = None
) -> Optional[bool]:
    pass

def setup_to_timeit(pattern: str):
    import hyperscan as hs
    db = hs.Database(mode=hs.HS_MODE_BLOCK)
    patterns = (
        (pattern.encode(), 0),
    )
    expressions, ids = zip(*patterns)
    return db, expressions, ids

# compile the pattern
db = hs.Database(mode=hs.HS_MODE_BLOCK)
patterns = (
    (pattern.encode(), 0),
)
expressions, ids = zip(*patterns)
time_to_compile = timeit.timeit(stmt=lambda: db.compile(expressions=expressions, ids=ids, elements=len(patterns)), number=1)
print(f"time to compile: {time_to_compile}")

# BLOCK MODE
time_to_search = timeit.timeit(stmt=lambda: db.scan(haystack.encode(), match_event_handler=on_match), number=1)
print(f"time to search: {time_to_search}")

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