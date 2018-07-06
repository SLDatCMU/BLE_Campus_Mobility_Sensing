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

echo "Adding new node to record"
echo "This may take a while..."

# rsync daily data

#ssh_cmd="ssh pi@ble-mobility-${number}.wv.cc.cmu.edu"
rsync_cmd="rsync -rvz -Pav -e \"ssh -i /home/pi/.ssh/id_rsa\" --progress pi@ble-mobility-${number}.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/${nodename}"
#echo $ssh_cmd >> /home/pi/ble_campus_mobility_sensing/collect-daily.sh 
echo $rsync_cmd >> /home/pi/ble_campus_mobility_sensing/collect-daily.sh

# setup mail function for each deployed node
sudo ./mail-setup.sh $1

# run tmux
sudo ./run-tmux.sh $1

