#!/bin/sh

# Repeat script 2, but add a second argument to accept number of a column with the number of engines. If
#several planes have the highest number of engines, then the script will only show one of them. (use it on ~/Data/opentraveldata/optd_aircraft.csv) 

FILENAME=$1
COLUMN=$2

sort -t "^" -k${COLUMN}rn "${FILENAME}"| head -1 |cut -d"^" -f3
