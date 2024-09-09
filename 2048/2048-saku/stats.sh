#!/bin/usr/env bash

TEMP_FILE="$PWD/2048/2048-saku/tmp"
N=10
if [ $# -eq 1 ]; then
  N=$1
fi

touch $TEMP_FILE

for run in $(seq 1 $N);
  do python3 2048/2048-saku/puzzle.py >> $TEMP_FILE && tail -n 1 $TEMP_FILE
done

# get the high score
cat $TEMP_FILE | awk '{ if($NF > max) { max=$NF; max_line=$0 } } END { print "high score: " max}'
# get the average score
cat $TEMP_FILE | awk '{ sum += $NF } END { print "Average: " sum/NR }'

rm $TEMP_FILE
