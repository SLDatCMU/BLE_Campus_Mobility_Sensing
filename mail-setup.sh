#!/bin/bash

mail_setup () {
	sudo apt-get install ssmtp
	sudo apt-get install mailutils
	sudo sh -c "echo 'root=postmaster\nmailhub=smtp.gmail.com:587\nhostname=raspberrypi\nAuthUser=cpsmobility651@gmail.com\nAuthPass=bleSensing&M0bility\nFromLineOverride=YES\nUseSTARTTLS=YES' >> /etc/ssmtp/ssmtp.conf"
}


if [ $# -eq 1 ]
then
	if [ $1 -gt 9 ]
	then
		nodename="ble-mobility-$1.wv.cc.cmu.edu"
		number="$1"
	else
		nodename="ble-mobility-0$1.wv.cc.cmu.edu"
		number="0$1"
	fi
	echo "Nodename set!"
else
	echo "No argument supplied!"
	exit 1
fi

sshpass -p "bleSense&Mobility" ssh -o StrictHostKeyChecking=no pi@${nodename} "$(typeset -f mail_setup); mail_setup" 
