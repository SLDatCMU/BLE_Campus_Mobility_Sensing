#!/bin/bash
 
sshpass -p "bleSense&Mobility" rsync -rvz -e 'ssh -o StrictHostKeyChecking=no -p 22' --progress --ignore-existing pi@ble-mobility-06.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node06
sshpass -p "bleSense&Mobility" rsync -rvz -e 'ssh -o StrictHostKeyChecking=no -p 22' --progress --ignore-existing pi@ble-mobility-07.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node07
sshpass -p "bleSense&Mobility" rsync -rvz -e 'ssh -o StrictHostKeyChecking=no -p 22' --progress --ignore-existing pi@ble-mobility-09.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node09
sshpass -p "bleSense&Mobility" rsync -rvz -e 'ssh -o StrictHostKeyChecking=no -p 22' --progress --ignore-existing pi@ble-mobility-11.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node11
sshpass -p "bleSense&Mobility" rsync -rvz -e 'ssh -o StrictHostKeyChecking=no -p 22' --progress --ignore-existing pi@ble-mobility-03.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node03
sshpass -p "bleSense&Mobility" rsync -rvz -e 'ssh -o StrictHostKeyChecking=no -p 22' --progress --ignore-existing pi@ble-mobility-04.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node04
sshpass -p "bleSense&Mobility" rsync -rvz -e 'ssh -o StrictHostKeyChecking=no -p 22' --progress --ignore-existing pi@ble-mobility-05.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node05
sshpass -p "bleSense&Mobility" rsync -rvz -e 'ssh -o StrictHostKeyChecking=no -p 22' --progress --ignore-existing pi@ble-mobility-10.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node10
sshpass -p "bleSense&Mobility" rsync -rvz -e 'ssh -o StrictHostKeyChecking=no -p 22' --progress --ignore-existing pi@ble-mobility-12.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node12
sshpass -p "bleSense&Mobility" rsync -rvz -e 'ssh -o StrictHostKeyChecking=no -p 22' --progress --ignore-existing pi@ble-mobility-01.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node01
