import subprocess
import os
import re

# Get these from the CLI program via stdin
haystack = "xxxxx=xxxxxx"
pattern = r'x=x'

temp_file = os.path.join(os.path.dirname(__file__), "temp")

if not os.path.exists(temp_file):
  with open(temp_file, "w") as f:
      f.write(haystack)

command = "time grep " + pattern + " " + temp_file
result = subprocess.run(command, capture_output=True, shell=True, cwd=os.path.dirname(__file__), text=True)

pattern = re.compile(r'(real|user|sys)\s+(\d+)m(\d+\.\d+)s')
output = dict()
for line in result.stderr.splitlines():
  match = pattern.search(line)
  if match:
    output[match.group(1)] = float(match.group(2)) * 60 + float(match.group(3))

print(output['user'])

os.remove(temp_file)
  
