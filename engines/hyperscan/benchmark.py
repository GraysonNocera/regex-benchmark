"""
Caveat: this uses Vectorscan rather than Hyperscan, but the two are similar. Vectorscan just broadens the available
architectures that can be used with Hyperscan.
should the CLI provide us with BLOCK, STREAM, or VECTOR mode?
Ideally, we would run the native C engine, but python binding is quicker to get up and running.
"""

import sys
import timeit
from typing import Any, Optional

import hyperscan as hs

# A truthy return value signifies to stop matching
matches = 0
def on_match(
    id: int, from_: int, to: int, flags: int, context: Optional[Any] = None
) -> Optional[bool]:
    global matches
    matches += 1

def measure(data, pattern):
    global matches
    matches = 0

    # compile the pattern
    db = hs.Database(mode=hs.HS_MODE_BLOCK)
    patterns = (
        (pattern.encode(), 0),
    )
    expressions, ids = zip(*patterns)
    # print(expressions, file=sys.stderr)
    time_to_compile = timeit.timeit(stmt=lambda: db.compile(expressions=expressions, ids=ids, elements=len(patterns)), number=1)
    # print(f"time to compile: {time_to_compile}", file=sys.stderr)

    # BLOCK MODE
    time_to_search = timeit.timeit(stmt=lambda: db.scan(data.encode(), match_event_handler=on_match), number=1)
    # print(f"time to search: {time_to_search}", file=sys.stderr)

    print(f"{time_to_search * 1e3} - {matches}")


if len(sys.argv) != 4:
    print('Usage: python benchmark.py <input_filename> regex num_iterations')
    sys.exit(1)

pattern = sys.argv[2]
num_iterations = int(sys.argv[3])

with open(sys.argv[1], "r") as f: 
    data = f.read()

    # print(f"length of sys.argv: {len(sys.argv)}", file=sys.stderr)
    for i in range(num_iterations):
        measure(data, pattern)