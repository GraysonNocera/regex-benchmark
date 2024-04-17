import times
import os
import re
import strformat
import std/strutils

if paramCount() != 3:
  echo "Usage: ./benchmark <filename> regex numIterations"
  quit(QuitFailure)

proc measure(data:string, pattern:string) =
  let r_pattern = re(pattern)

  let time = cpuTime()
  let matches: seq[string] = data.findAll(r_pattern)
  let count = len(matches)
  let elapsed_time = cpuTime() - time 
  echo &"{elapsed_time * 1e3} - {count}"

let data = readFile(paramStr(1))
let pattern = paramStr(2)
let numIterations = parseInt(paramStr(3))

for i in 1..numIterations:
  measure(data, pattern)
