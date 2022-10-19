#!/bin/bash

# exclude file
exclude="exclude"
# backintime profile number
profile=1

# start from counter
counter=41
echo "counter starting from: $counter"

awk -v counter=$counter '
!/^($|[:space:]*#)/  && !/^([/])/ { counter = ++counter; print "profile1.snapshots.exclude."counter".value=/home/*/"$0}
/^([/].*)/ { counter = ++counter; print "profile1.snapshots.exclude."counter".value="$0}
' $exclude

