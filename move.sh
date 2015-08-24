#!/bin/bash
cd records
#echo $1
for f in {temp,humi,ambi,baro}*
do
	#echo $f
	day=`echo $f|cut -d"_" -f2`
	if [ "$day" == "$1" ]; then
		echo "$f today"
	else
		echo "$f old, -->move"
		mv $f ../arch
	fi
done
cd ..
