import times
import os
import strformat
import std/strutils

import pkg/regex

if paramCount() != 3:
  echo "Usage: ./benchmark <filename> regex numIterations"
  quit(QuitFailure)

proc measure(data: string, pattern: string) =
  try:
    let r_pattern = re2(pattern)

    let time = cpuTime()
    let matches = data.findAll(r_pattern)
    let count = len(matches)
    let elapsed_time = cpuTime() - time 
    echo &"{elapsed_time * 1e3} - {count}"
  except CatchableError as e:
    stderr.writeLine("compilation failed: ", e.msg)
    quit(QuitFailure)

let data = readFile(paramStr(1))
let pattern = paramStr(2)
let numIterations = parseInt(paramStr(3))

for i in 1..numIterations:
  measure(data, pattern)
