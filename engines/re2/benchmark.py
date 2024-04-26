"""
Trying to successfully run the re2 engine in C++ was a huge pain, so I just pip installed 'google-re2' and used the Python bindings.
Ideally, we would run the native C++ engine, but this is a good enough solution for now.
"""

import sys
import timeit

import re2

EXIT_FAILURE = 1

if len(sys.argv) != 4:
    print('Usage: python benchmark.py <input_filename> regex num_iterations')
    sys.exit(EXIT_FAILURE)

def measure(data, pattern):

  try:
    re2.purge()
    start = timeit.default_timer()
    pattern = re2.compile(pattern)
    time_to_compile = timeit.default_timer() - start

    start = timeit.default_timer()
    matches = pattern.findall(data)
    time_to_search = timeit.default_timer() - start

    print(f"{time_to_search * 1e3} - {len(matches)}")
  except Exception as e:
    print(f"compilation error: {e}", file=sys.stderr)
    sys.exit(EXIT_FAILURE)

with open(sys.argv[1]) as file:
    data = file.read()
    pattern = sys.argv[2]
    num_iterations = int(sys.argv[3])

    for i in range(num_iterations):
        measure(data, pattern)