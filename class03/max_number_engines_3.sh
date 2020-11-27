#!/bin/sh

# Create a script that accepts as input arguments the name of the CSV file, and a number (number of
# engines) and returns number of aircrafts that have that number of engines. (use it on
# ~/Data/opentraveldata/optd_aircraft.csv)

FILENAME=$1
NB_ENGINES=$2

sort -t "^" -k7rn "${FILENAME}"| cut -d"^" -f7 | grep "${NB_ENGINES}" | wc -l
