#!/bin/bash

# check memory function
check_memory () {
	free=$(free -mt | grep Total | awk '{print $4}')
	if [[ "$free" -le 100 ]]; then
		echo "`hostname`.wv.cc.cmu.edu has low memory" | mail -s "Node memory low alert" blemobility651@gmail.com
	fi
}

# check if tmux has active sessions
check_tmux () {
	tmux list-panes -F '#{pane_active} #{pane_pid}' > /dev/null 2>&1
	if [[ "$?" -ne 0 ]]; then
		echo "`hostname`.wv.cc.cmu.edu is not running tmux code" | mail -s "Node not running tmux alert" blemobility651@gmail.com
	fi
}


# max=13
listVar="3 4 5 6 7 9 10 11 12"
# for i in `seq 1 $max`
for i in $listVar; do 
	if [[ "$i" -gt 9 ]]; then
		nodename="ble-mobility-$i.wv.cc.cmu.edu"
	else
		nodename="ble-mobility-0$i.wv.cc.cmu.edu"
	fi
	ping -c 3 $nodename > /dev/null 2>&1
	if [[ "$?" -ne 0 ]]; then 
		echo "Node ${nodename} is off" | mail -s "Node off alert" blemobility651@gmail.com
	else 
		ssh -i /home/pi/.ssh/id_rsa pi@${nodename} "$(typeset -f check_memory); check_memory" 
		# ssh -i /home/pi/.ssh/id_rsa pi@${nodename} "$(typeset -f check_tmux); check_tmux"
	fi
done
