#!/bin/bash
# Put your command below to execute your program.
# Replace "./my-program" with the command that can execute your program.
# Remember to preserve " $@" at the end, which will be the program options we give you.

Usage () {
	echo "Usage"
	echo "execute.sh [-r] -i <query_file> -o <ranked-list> -m <model-dir> -d <NTCIR-dir>"
}

Usage


python3 test.py $@