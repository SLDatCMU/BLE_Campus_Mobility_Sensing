#!/bin/bash

# check memory function
check_memory () {
	free=$(free -mt | grep Total | awk '{print $4}')
	if [[ "$free" -le 100 ]]; then
		echo "`hostname`.wv.cc.cmu.edu has low memory" | mail -s "Node memory low alert" pengc1@andrew.cmu.edu
	fi
}

# check if tmux has active sessions
check_tmux () {
	tmux list-panes -F '#{pane_active} #{pane_pid}' > /dev/null 2>&1
	if [[ "$?" -ne 0 ]]; then
		echo "`hostname`.wv.cc.cmu.edu is not running tmux code" | mail -s "Node not running tmux alert" pengc1@andrew.cmu.edu
	fi
}

max=13
for i in `seq 1 $max`
do 
	if [[ "$i" -gt 9 ]]; then
		nodename="ble-mobility-$i.wv.cc.cmu.edu"
	else
		nodename="ble-mobility-0$i.wv.cc.cmu.edu"
	fi
	ping -c 3 $nodename > /dev/null 2>&1
	if [[ "$?" -ne 0 ]]; then 
		echo "Node ${nodename} is off" | mail -s "Node off alert" pengc1@andrew.cmu.edu
	else 
		sshpass -p "bleSense&Mobility" ssh -o StrictHostKeyChecking=no pi@${nodename} "$(typeset -f check_memory); check_memory" 
		sshpass -p "bleSense&Mobility" ssh -o StrictHostKeyChecking=no pi@${nodename} "$(typeset -f check_tmux); check_tmux"
	fi
done

