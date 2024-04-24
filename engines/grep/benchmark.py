import subprocess
import re
import sys

EXIT_FAILURE = 1

def measure(filename, pattern):
    # print(filename, file=sys.stderr)

    # The --count option does not work with -o, in my experimentation, so I have to manually count the lines
    # from stdout
    command = f"time grep -Po \"{pattern}\" {filename}"
    # print(command)
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable='/bin/bash')

    # This assumed bash time command formatting
    pattern = re.compile(r'grep:\s+([^\n]+)')
    match = re.search(pattern, result.stderr.decode())
    if match:
        print(f"Compilation failed: {match.group(1)}")
        exit(EXIT_FAILURE)

    pattern = re.compile(r'(user)\s+(\d+)m(\d+\.\d+)s')
    match = pattern.findall(result.stderr.decode())
    if match:
        output = float(match[0][1]) * 60 + float(match[0][2]) # seconds
        output = output * 1e3 # milliseconds
    else:
        print("No match found, problem with time command", file=sys.stderr)
        exit(EXIT_FAILURE)

    matches = len(result.stdout.decode().splitlines())
    print(str(output) + ' - ' + str(matches))


if len(sys.argv) != 4:
    print('Usage: python3 benchmark.py <input_filename> regex num_iterations')
    sys.exit(1)

num_iterations = int(sys.argv[3])
pattern = sys.argv[2]

for i in range(num_iterations):
    measure(sys.argv[1], pattern)

