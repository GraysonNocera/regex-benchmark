import subprocess
import os

haystack = "xxxxx=xxxxxx"
pattern = r'x=x'

temp_file = os.path.join(os.path.dirname(__file__), "temp")

if not os.path.exists(temp_file):
  with open(temp_file, "w") as f:
      f.write(haystack)

command = "grep " + pattern + " " + temp_file
result = subprocess.run(command, capture_output=True, shell=True, cwd=os.path.dirname(__file__), text=True)
print(result.stderr)
print(result.stdout)

print("here now")
command = "time grep " + pattern + " " + temp_file
result = subprocess.run(command, capture_output=True, shell=True, cwd=os.path.dirname(__file__), text=True)
print(result.returncode)
print(result.stderr)
print(result.stdout)


result = subprocess.run(["time", "grep", pattern, temp_file], capture_output=True, shell=True, cwd=os.path.dirname(__file__), text=True)

print(result.args)
with open(os.path.join(os.path.dirname(__file__), "output"), "w") as f:
    f.write(result.stdout)
    f.write(result.stderr)

output = [line for line in result.stdout.split("\n") if "x=x" not in line]
print(output)
