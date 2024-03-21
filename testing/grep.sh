#!/bin/bash

echo "Starting"
echo $1
echo $2
ts=$(date +%s%N)
echo $ts
START=$(date +%s)
result=$(time grep $1 $2)
END=$(date +%s)
ts=$(date +%s%N)
echo $ts
echo "Ending"

echo "$(($END-$START))"
echo $result