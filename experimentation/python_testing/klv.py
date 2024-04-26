import sys

"""A simplied version of klv decoding in rebar (https://github.com/BurntSushi/rebar/blob/master/engines/python/main.py#L148)"""

def parse(stdin: bytes):
  config = dict()
  print(stdin)
  while stdin:
    pieces = stdin.split(b':', 2)
    
    (key, value), nread = get_one_klv(pieces)

    stdin = stdin[nread:]
    print(stdin)
    if len(stdin) == 0 or stdin[0:1] != b'\n':
        raise ValueError(f"did not find \\n after value for key '{key}'")

    add_to_config(config, key, value)
    stdin = stdin[1:]
    print()

  return config

def get_one_klv(pieces):
  if len(pieces) < 3:
    raise ValueError("invalid KLV item: not enough pieces")
  
  key = pieces[0].decode('utf-8')
  length = int.from_bytes(pieces[1])
  print(length)
  length = int(pieces[1])
  value = pieces[2]

  if len(value) < length:
    raise ValueError(
      f"not enough bytes remaining for length "
      f"{value} for key '{key}'",
    )
  
  value = value[:length]
  print(f"Read key {key}, length {length}, value {value}")
  nread = len(pieces[0]) + 1 + len(pieces[1]) + 1 + len(value)

  return (key, value), nread


def add_to_config(config, key, value):
  if key in config:
    raise ValueError(f"Duplicate key {key}")
  
  config[key] = value

if __name__ == "__main__":

  stdin = sys.stdin.buffer.read()
  config = parse(stdin)
  print(config)