#!/usr/bin/env bash

if [[ $# < 1 ]]; then
	max=1000
else
	max=$1
fi

i=0
while [[ $i -le $max ]]; do
	echo $i $RANDOM $RANDOM $RANDOM;
	i=$(($i+1))
done | wye scatter --x 1 --y 2 3 --color red blue --title "Scatter" --xlabel "x" --ylabel "y" --hline 0 8192 16384 24576 32768 --vspan 8192 24576
