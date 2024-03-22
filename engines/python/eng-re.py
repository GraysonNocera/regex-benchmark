import klv
import sys
import timeit
import re
import cProfile

if __name__ == "__main__":

  stdin = sys.stdin.buffer.read()
  config = klv.parse(stdin)
  print(config)

  if config['model'] == b'compile':
    re.purge()
    execution_time = timeit.timeit(lambda: re.compile(config['pattern']))
    print(execution_time)

    with cProfile.Profile() as pr:
      re.compile(config['pattern'])

      # pr.print_stats()

    with cProfile.Profile() as pr:
      re.findall(config['pattern'], config['haystack'])

      pr.print_stats()
