import times
import os
import strformat

import pkg/regex

if paramCount() <= 0:
  echo "Usage: ./benchmark <filename> regex1 regex2 ... regexN"
  quit(QuitFailure)

proc measure(data: string, pattern: string) =
  let r_pattern = re2(pattern)

  let time = cpuTime()
  let matches = data.findAll(r_pattern)
  let count = len(matches)
  let elapsed_time = cpuTime() - time 
  echo &"{elapsed_time * 1e3} - {count}"

let data = readFile(paramStr(1))

for i in 2..paramCount():
  let pattern = paramStr(i)
  measure(data, pattern)
