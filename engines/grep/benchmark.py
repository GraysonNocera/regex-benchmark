import subprocess
import os
import re
import sys
from timeit import default_timer as timer

# TODO: et these from the CLI program via stdin
haystack = "xxxxx=xxxxxx"
pattern = r'x=x'

temp_file = os.path.join(os.path.dirname(__file__), "temp")

with open(temp_file, "w") as f:
    f.write(haystack)

command = "time grep " + pattern + " " + temp_file
result = subprocess.run(command, capture_output=True, shell=True, cwd=os.path.dirname(__file__), text=True)

pattern = re.compile(r'(real|user|sys)\s+(\d+)m(\d+\.\d+)s')
output = dict()
for line in result.stderr.splitlines():
  match = pattern.search(line)
  if match:
    output[match.group(1)] = float(match.group(2)) * 60 + float(match.group(3)) # seconds

print(output)

os.remove(temp_file)
  

if len(sys.argv) < 3:
    print('Usage: python benchmark.py <input_filename> regex1 regex2 ..')
    sys.exit(1)

def measure(data, pattern):
    start_time = timer()

    regex = re.compile(pattern)
    matches = re.findall(regex, data)

    elapsed_time = timer() - start_time

    print(str(elapsed_time * 1e3) + ' - ' + str(len(matches)))

with open(sys.argv[1]) as file:
    data = file.read()
    # test_regexes = json.loads(sys.argv[2])

    for regex in sys.argv[2:]:
        measure(data, regex)

