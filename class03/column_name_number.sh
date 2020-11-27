#!/bin/bash

# Create a script that will return column names together with their column number from the csv files. The
# first argument should be file name and the second delimiter.

FILENAME=$1
DELIMITER=$2

cat -n <(head -1 "${FILENAME}" | tr "${DELIMITER}" "\n")
