# BLE_Campus_Mobility_Sensing
Summer 2018 project using Raspeberry Pi 0Ws distributed across campus to determine population mobility patterns by tracking Bluetooth device signatures.

All the shell scripts are meant to be executed on server node(Node 00)
1.node-setup.sh

function: Let each new deployed node synchronize its data to server each day,send alert emails(when memory is low or shutdown) if necessary, and automatically run combined_scanner.py every time the deployed node is on.

format: sudo ./node-setup.sh x 
(x: the number of deployed node)

2. mail-setup.sh

function: Let deployed node send emails if necessary,part of node-setup.sh

format: sudo ./mail-setup.sh x 
(x: the number of deployed node)

3. run-tmux.sh

function: run combined_scanner.py every time the deployed node turns on, part of node-setup.sh

format: sudo ./run-tmux.sh x 
(x: the number of deployed node)

4. collect-daily.sh

function: enables server to collect data from each deployed node daily from each deployed node, and keeps the data in their folders, has already set in crontab

5. alert.sh

function: check if each deployed node has alert situations

format: sudo ./alert.sh 
(it will scan all deployed nodes for alert situations, if such situation exist, the deployed node will send emails)



