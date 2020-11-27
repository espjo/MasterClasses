#!/bin/sh

# Create a script that accepts a CSV filename as input ($1 inside your script) and returns the model of the
# aircraft with the highest number of engines. (use it on ~/Data/opentraveldata/optd_aircraft.csv) 

FILENAME=$1

sort -t "^" -k7rn "$1"| head -1 | cut -d"^" -f3
