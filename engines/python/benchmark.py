import sys
import re
import json
from timeit import default_timer as timer

if len(sys.argv) < 3:
    print('Usage: python benchmark.py <input_filename> regex1 regex2 ..')
    sys.exit(1)

def measure(data, pattern):

    regex = re.compile(pattern)

    start_time = timer()
    matches = re.findall(regex, data)

    elapsed_time = timer() - start_time

    print(str(elapsed_time * 1e3) + ' - ' + str(len(matches)))

with open(sys.argv[1]) as file:
    data = file.read()
    # test_regexes = json.loads(sys.argv[2])

    for regex in sys.argv[2:]:
        measure(data, regex)

