#to use bluepy ble submodule rather than pybluez:
#sudo apt-get install libboost-all-dev libbluetooth-dev
#sudo pip install gattool
from gattlib import *

service = DiscoveryService()
devices = service.discover(2)

for address, name in devices.items():
	print("name: {}, address: {}".format(name, address))
