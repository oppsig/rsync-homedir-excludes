#!/bin/bash
# This script will use the exclude file to calculate space per folder.
# You can run it like this: ./space.sh | sort -hr
IFS=$'\n'
exclude="exclude"
profile=1


content=$(awk '
!/^($|[:space:]*#)/  && !/^([/])/ { print "/home/kodi/"$0 }
/^([/].*)/ { print }
' $exclude)

#echo $content
for value in $content
do
	find $value -maxdepth 0 -exec du -hs {} \; 2>/dev/null
	#find $value -maxdepth 0 -exec echo {} \;
	#find $value -maxdepth 0 exec echo {} \; 2>/dev/null | xargs -r sh -c 'for file do echo "$file"; done' sh
done
