"""
Trying to successfully run the re2 engine in C++ was a huge pain, so I just pip installed 'google-re2' and used the Python bindings.
Ideally, we would run the native C++ engine, but this is a good enough solution for now.
"""

import re2
import timeit

haystack = "xxxxx=xxxxxx"
pattern = r'x=x'

time_to_compile = timeit.timeit(stmt=lambda: re2.compile(pattern), number=1)
print(f"time to compile: {time_to_compile}")

pattern = re2.compile(pattern)

time_to_search = timeit.timeit(stmt=lambda: pattern.search(haystack), number=1)
print(f"time to search: {time_to_search}")