#!/bin/sh

SERVER="$(sed -n 1,1p cuckoo.conf)"
PORT="$(sed -n 2,2p cuckoo.conf)"

if [ "$1" = "-s" ]
then
	DIR="$2"
	echo "Submitting Files to Cuckoo from $DIR/*"
	for file in $DIR/*
	do
		echo "FILE: $file"
  		curl -k --connect-timeout 10 -F file=@"$file" https://$SERVER:$PORT/api/tasks/create/file/
 		sleep 32
	done
elif [ "$1" = "-p" ]
then
	if [ -z "$2" ] || [ -z "$3" ]
	then
		echo "usage: -p STARTID STOPID"
	else
		echo "Download PCAPS from ID: $2 - $3"
		CWD=$(pwd)
		COUNTER=$2
		while [ $COUNTER -le $3 ]
		do
			echo "PCAP ID: $COUNTER"
			curl -k --connect-timeout 10 -O -L  https://$SERVER:$PORT/api/tasks/get/pcap/$COUNTER
			mv $CWD/$COUNTER $CWD/$COUNTER.pcap
			COUNTER=$((COUNTER+1))
			sleep 3
		done
		mergecap -w MERGED.pcap *
	fi
elif [ "$1" = "-i" ]
then
	if [ -z "$2" ] || [ -z "$3" ]
	then
		echo "usage: -i STARTID STOPID"
	else
		echo "Output IOCS from ID: $2 - $3"
		COUNTER=$2
		while [ $COUNTER -le $3 ]
		do
			echo "IOC ID: $COUNTER"
			curl -k --connect-timeout 10 https://$SERVER:$PORT/api/tasks/get/iocs/$COUNTER/detailed/
			COUNTER=$((COUNTER+1))
			sleep 17
		done
	fi
elif [ "$1" = "-status" ]
then 
	curl -k --connect-timeout 10 https://$SERVER:$PORT/api/cuckoo/status/
else
	echo "usage: ./cuckoo_submit.sh <-s <directory> submits files in a directory to cuckoo | -p STARTID STOPID downloads pcaps from start id to stop id | -i STARTID STOPID outputs detailed potential IOCs | -status Get Cuckoo status >"
fi
