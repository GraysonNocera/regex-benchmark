import sys
import re
import json
from timeit import default_timer as timer

if len(sys.argv) != 4:
    print('Usage: python benchmark.py <input_filename> regex num_iterations')
    sys.exit(1)

def measure(data, pattern):

    regex = re.compile(pattern)

    start_time = timer()
    matches = re.findall(regex, data)
    elapsed_time = timer() - start_time

    print(str(elapsed_time * 1e3) + ' - ' + str(len(matches)))

with open(sys.argv[1]) as file:
    data = file.read()
    pattern = sys.argv[2]
    num_iterations = int(sys.argv[3])

    for i in range(num_iterations):
        measure(data, pattern)

