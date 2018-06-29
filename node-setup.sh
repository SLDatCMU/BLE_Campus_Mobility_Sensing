#!/bin/bash


if [ $# -eq 1 ]
then
	if [ $1 -gt 9 ]
	then
		nodename="node$1"
		number="$1"
	else
		nodename="node0$1"
		number="0$1"
	fi
	echo "Setting data collection with hostname $nodename"
	sudo mkdir -p /home/pi/data_collection/"$nodename"
else
	echo "No argument supplied!"
	exit 1
fi

echo "Synchronizing data"
echo "This may take a while..."
rsync_cmd="sshpass -p \"bleSense&Mobility\" rsync -rvz -e 'ssh -o StrictHostKeyChecking=no -p 22' --progress --ignore-existing pi@ble-mobility-${number}.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/${nodename}"
echo $rsync_cmd >> /home/pi/collect-daily.sh

