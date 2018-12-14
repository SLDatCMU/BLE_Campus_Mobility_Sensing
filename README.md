# BLE_Campus_Mobility_Sensing
Summer 2018 project using Raspeberry Pi 0Ws distributed across campus to determine population mobility patterns by tracking Bluetooth device signatures.

The shell scripts(the following 1 to 5) are meant to be executed on server node(Node 00)

Note: If number is from 1 to 9, type number instead of 0number(for example when deploy number 9 node, type 9 instead of 09). 

1.node-setup.sh

function: Let each new deployed node synchronize its data to server each day,send alert emails(when memory is low or shutdown) if necessary, and automatically run combined_scanner.py every time the deployed node is on.

format: sudo ./node-setup.sh $x 
($x: the number of deployed node)

2. mail-setup.sh

function: Let deployed node send emails if necessary,part of node-setup.sh

format: sudo ./mail-setup.sh $x 
($x: the number of deployed node)

3. run-tmux.sh

function: run combined_scanner.py every time the deployed node turns on, part of node-setup.sh

format: sudo ./run-tmux.sh $x 
($x: the number of deployed node)

4. collect-daily.sh

function: enables server to collect data from each deployed node daily from each deployed node, and keeps the data in their own folders, the script has already placed in crontab

5. alert.sh

function: check if each deployed node has alert situations

format: sudo ./alert.sh 
(it will scan all deployed nodes for alert situations, if such situation exist, the deployed node will send emails)

Suppose a new node(number $x) is about to deploy, the setup steps are as follows:

1.copy the latest raspberry pi image to the sd card of the node

2.ssh on the new node, and execute "sudo ./setup_W0.sh $x"

3.ssh on the server, execute "ssh-copy-id -i /home/pi/.ssh/id_rsa pi@ble-mobility-$x.wv.cc.cmu.edu"

4.Stay on the server, execute execute "sudo ./node-setup.sh $x"

5.change the variable $max and $listVar accordingly in the alert.sh to ensure that alert.sh covers the node $x
