"""
Trying to successfully run the re2 engine in C++ was a huge pain, so I just pip installed 'google-re2' and used the Python bindings.
Ideally, we would run the native C++ engine, but this is a good enough solution for now.
"""

import re2
import timeit
import sys

if len(sys.argv) < 3:
    print('Usage: python benchmark.py <input_filename> regex1 regex2 ..')
    sys.exit(1)

def measure(data, pattern):

  time_to_compile = timeit.timeit(stmt=lambda: re2.compile(pattern), number=1)
  print(f"time to compile: {time_to_compile}", file=sys.stderr)

  pattern = re2.compile(pattern)

  re2.purge()
  start = timeit.default_timer()
  matches = pattern.findall(data)
  time_to_search = timeit.default_timer() - start
  print(f"time to search: {time_to_search}", file=sys.stderr)

  print(f"{time_to_search * 1e3} - {len(matches)}")

with open(sys.argv[1], "r") as f: 
  data = f.read()

  for regex in sys.argv[2:]:
      measure(data, regex)