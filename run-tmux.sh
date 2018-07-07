#!/bin/bash

# run the code in deployed node automatically in tmux after reboot, so even if the node is plugged off accidentally, after plugging it on the ble code will run again.

run_tmux () {
	sudo rm tmux_start.sh
	touch tmux_start.sh
	header_cmd="#!/bin/bash"
	tmux_cmd="tmux new-session -d -s ble 'python /home/pi/ble_campus_mobility_sensing/passive_ble/sensing_src/combined_scanner.py'"
	echo $header_cmd >> /home/pi/tmux_start.sh
	echo $tmux_cmd >> /home/pi/tmux_start.sh
	chmod +x tmux_start.sh
	# add command to /etc/rc.local
	# sudo sed -i -e '$i \sudo bash /home/pi/tmux_start.sh &\n' /etc/rc.local
	# sudo reboot
}

if [ $# -eq 1 ]
then
	if [ $1 -gt 9 ]
	then
		number="$1"
	else
		number="0$1"
	fi
else
	echo "No argument supplied!"
	exit 1
fi


# ssh to each deployed node
ssh -i /home/pi/.ssh/id_rsa pi@ble-mobility-${number}.wv.cc.cmu.edu "$(typeset -f run_tmux); run_tmux"

