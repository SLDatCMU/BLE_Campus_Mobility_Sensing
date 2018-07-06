#!/bin/bash


rsync -rvz -Pav -e "ssh -i /home/pi/.ssh/id_rsa" --progress pi@ble-mobility-03.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node03
rsync -rvz -Pav -e "ssh -i /home/pi/.ssh/id_rsa" --progress pi@ble-mobility-04.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node04
rsync -rvz -Pav -e "ssh -i /home/pi/.ssh/id_rsa" --progress pi@ble-mobility-05.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node05
rsync -rvz -Pav -e "ssh -i /home/pi/.ssh/id_rsa" --progress pi@ble-mobility-06.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node06
rsync -rvz -Pav -e "ssh -i /home/pi/.ssh/id_rsa" --progress pi@ble-mobility-07.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node07
rsync -rvz -Pav -e "ssh -i /home/pi/.ssh/id_rsa" --progress pi@ble-mobility-09.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node09
rsync -rvz -Pav -e "ssh -i /home/pi/.ssh/id_rsa" --progress pi@ble-mobility-10.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node10
rsync -rvz -Pav -e "ssh -i /home/pi/.ssh/id_rsa" --progress pi@ble-mobility-11.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node11
rsync -rvz -Pav -e "ssh -i /home/pi/.ssh/id_rsa" --progress pi@ble-mobility-12.wv.cc.cmu.edu:/home/pi/ble_campus_mobility_sensing/passive_ble/data /home/pi/data_collection/node12

