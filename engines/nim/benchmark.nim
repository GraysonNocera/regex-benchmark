import times
import os
import re
import strformat

if paramCount() <= 0:
  echo "Usage: ./benchmark <filename> regex1 regex2 regex3..."
  quit(QuitFailure)

proc measure(data:string, pattern:string) =
  let time = cpuTime()
  let r_pattern = re(pattern)
  let matches: seq[string] = data.findAll(r_pattern)
  let count = len(matches)
  let elapsed_time = cpuTime() - time 
  echo &"{elapsed_time * 1e3} - {count}"

let data = readFile(paramStr(1))


for i in 2..paramCount():
  let pattern = paramStr(i)
  measure(data, pattern)
