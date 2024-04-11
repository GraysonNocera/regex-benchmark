import re2
import timeit

haystack = "xxxxx=xxxxxx"
pattern = r'x=x'

time_to_compile = timeit.timeit(stmt=lambda: re2.compile(pattern), number=1)
print(f"time to compile: {time_to_compile}")

pattern = re2.compile(pattern)

time_to_search = timeit.timeit(stmt=lambda: pattern.search(haystack), number=1)
print(f"time to search: {time_to_search}")