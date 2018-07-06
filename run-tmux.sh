#!/bin/bash

# run the code in deployed node automatically
run_tmux () {
	touch tmux_start.sh
	header_cmd="#!/bin/bash"
	tmux_cmd="tmux new-session -d -s ble 'python /home/pi/ble_campus_mobility_sensing/passive_ble/sensing_src/ble_passive_sniffer.py'"
	echo $header_cmd >> /home/pi/tmux_start.sh
	echo $tmux_cmd >> /home/pi/tmux_start.sh
	chmod +x tmux_start.sh
	sudo sed -i -e '$i \sudo bash /home/pi/tmux_start.sh &\n' /etc/rc.local
	# start_cmd="sudo -u pi bash /home/pi/tmux_start.sh &"
	# echo $start_cmd >> /etc/rc.local
	sudo reboot
	# tmux 
	# cd ble_campus_mbility_sensing/passive_ble/sensing_src/
	# sudo ./ble_passive_sniffer.py 
	# nohup sudo ./ble_passive_sniffer.py &
    	# nohup sudo ./ble_passive_sniffer.py > /dev/null 2>&1 &
	# tmux detach
	# builtin exit

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


# run code in tmux
ssh -i /home/pi/.ssh/id_rsa pi@ble-mobility-${number}.wv.cc.cmu.edu "$(typeset -f run_tmux); run_tmux"

