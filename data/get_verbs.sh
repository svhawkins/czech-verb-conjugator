#!/bin/bash

# sed -i -r "/[A-Z][a-z]?/d" verbs.txt
# sed -i -r "/([A-za-z] )/d" verbs.txt
vregex=$(cat irregular.txt | awk -F"," '{print $1}' | sed "s/ /)|(/g")
vregex=$(echo $vregex | sed "s/ /)|(/g")
vregex="((${vregex}))"