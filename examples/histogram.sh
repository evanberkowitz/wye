#!/usr/bin/env bash

if [[ $# < 1 ]]; then
	max=1000
else
	max=$1
fi

i=0
while [[ $i -le $max ]]; do
	echo $i $RANDOM $RANDOM $((16384+$RANDOM));
	i=$(($i+1))
done | wye histogram --field 2 3 --color red blue --title "Histogram" --xlabel "Values" --normalize --bins 21 51 --hline 0.0000305176
