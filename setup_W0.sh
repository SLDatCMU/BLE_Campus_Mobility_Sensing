if [ $# -eq 1 ]
then
	if [ $1 -gt 9 ]
	then
		nodename="ble_mobility_$1"
	else
		nodename="ble_mobility_0$1"
	fi
	echo "Setting Pi W0 up with hostname $nodename"
	hostname $nodename
else
	echo "No argument supplied!"
	echo "Run as: `basename "$0"` <number of BLE sensing node>"
	exit 1
fi

echo "Updating system with required packages."
echo "This may take a while..."
sudo apt-get update
sudo apt-get install -y vim tmux python-dev python-pip libglib2.0-dev python-numpy python-scipy
sudo -H pip install bluepy==1.1.4
echo "Done installing packages!"

# Todo: Add sensing script to /etc/rc.local so logging starts on startup
# Todo: Add periodic upload to collection server in crontab or similar
# Todo: Detect if node is outdoor node based on presence of ADC on SPI bus
# Todo: Add power management (auto sleep, wakeup, shutdown) if node is outdoor node
#		This may include frequency governor and increased polling period for BLE sensing.
