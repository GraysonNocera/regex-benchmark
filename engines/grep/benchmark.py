import subprocess
import re
import sys

if len(sys.argv) < 3:
    print('Usage: python benchmark.py <input_filename> regex1 regex2 ..')
    sys.exit(1)

def measure(filename, pattern):
    print(filename, file=sys.stderr)
    command = "time grep --count " + pattern + " haystacks/" + filename
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable='/bin/bash')

    # This assumed bash time command formatting
    pattern = re.compile(r'(user)\s+(\d+)m(\d+\.\d+)s')
    match = pattern.findall(result.stderr.decode())
    if match:
        output = float(match[0][1]) * 60 + float(match[0][2]) # seconds
        output = output * 1e3 # milliseconds
    else:
        raise Exception("No match found, problem with time command")
    
    matches = int(result.stdout.decode())
    print(str(output) + ' - ' + str(matches))

for regex in sys.argv[2:]:
    measure(sys.argv[1], regex)

