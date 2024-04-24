import subprocess

pattern = r'test*\w'
pattern = r'(x+x+)+y'
pattern = pattern.encode()

haystack = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
haystack = haystack.encode()

stdin = b'name:4:test\n'
stdin += b'model:7:compile\n'
stdin += b'pattern:'
stdin += str(len(pattern)).encode() + b':' + pattern + b'\n'
stdin += b'haystack:' + str(len(haystack)).encode() + b':' + haystack + b'\n'

command = ["python3", "eng-re.py"]
process = subprocess.Popen(command, stdin=subprocess.PIPE)
stdout, stderr = process.communicate(input=stdin)