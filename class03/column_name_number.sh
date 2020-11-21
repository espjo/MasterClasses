#!/bin/bash

FILENAME=$1
DELIMITER=$2

cat -n <(head -1 "${FILENAME}" | tr "${DELIMITER}" "\n")
