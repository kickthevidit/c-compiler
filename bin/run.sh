#!/bin/bash

FILE="compiler.py"
EXAMPLE_PROGRAM="example-programs/return_2.c"
OUT="exec"

clear
python3 $FILE $EXAMPLE_PROGRAM
#gcc -m32 return_2.s -o $OUT
#./$OUT
# echo "Output: $?"
# rm-rf ./$OUT