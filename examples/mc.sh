#!/usr/bin/env bash


if [[ $# < 1 ]]; then
	# Goes until interrupted
	while true; do
		echo "0:$RANDOM:$RANDOM:$((16384+$RANDOM))";
	done | wye mc --y 2 3 --last 100 --update-frequency 10 --title "Monte Carlo" --xlabel "Time" --ylabel "Samples" --name Two Three --delimiter :
else
	# Goes until the end
	max=$1
	i=0
	while [[ $i -le $max ]]; do
		echo "$i:$RANDOM:$RANDOM:$((16384+$RANDOM))";
		i=$(($i+1))
	done | wye mc --y 2 3 --title "Monte Carlo" --xlabel "Time" --ylabel "Samples" --name Two Three --delimiter :
fi 
