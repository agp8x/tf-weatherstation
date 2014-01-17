#!/usr/bin/env python3
# -*- coding: utf-8 -*-  

#class SensorType(Enum):
class SensorType:
	none = 0
	temp = 1
	humi = 2
	ambi = 3
	baro = 4
	rain = 5

try:
	from tinkerforge.ip_connection import IPConnection
	from tinkerforge.bricklet_temperature import Temperature
	from tinkerforge.bricklet_humidity import Humidity
	from tinkerforge.bricklet_ambient_light import AmbientLight
	from tinkerforge.bricklet_barometer import Barometer
except ImportError:
	print("package 'tinkerforge' not installed, canceling")
	raise

import os.path
import os
import time
from functools import partial

from Logger import Logger

#HOST = "localhost"
HOST = "192.168.2.30"
PORT = 4223

SENSORS=[
	["temp1", "7B5", SensorType.temp],
	["temp2", "8js", SensorType.temp],
	["humi1", "7RY", SensorType.humi],
	["ambi1", "8Fw", SensorType.ambi],
	["ambi2", "8DJ", SensorType.ambi],
	["baro1", "bB7", SensorType.baro],
]
names=[]
for x in SENSORS:
	names.append(x[0])

cbtimetemp=30000
cbtimehumi=30000
cbtimeambi=60000
cbtimebaro=60000

tempSensors=2
tempmaxdiff=200 # 200== 2.0 C
prev_temps_default=20000

logs='logs'
locks='locks'
records='records'

lockname=locks+"/all.lock"
log=open(logs+"/all.log",'a')
noop_cb = lambda value,sensor:0

if __name__ == "__main__":
	if not os.path.exists(lockname):
		lock=open(lockname,'w')
		lock.write(str(time.time()))
		lock.close()
		# lock obtained
		logger=Logger(names, (tempSensors, prev_temps_default, tempmaxdiff), log, records)
		callbacks=[noop_cb, logger.cb_temperature, logger.cb_humidity, logger.cb_illuminance, logger.cb_pressure, noop_cb]
		try:
			ipcon = IPConnection()
			# connect
			ipcon.connect(HOST, PORT)
			log.write('start logging "all" ... @'+time.ctime()+"\n")
			log.flush()
			connected=[]
			for i,sensor in enumerate(SENSORS):
				callback=partial(callbacks[sensor[2]], sensor=i)
				if(sensor[2] == SensorType.temp):
					obj = Temperature(sensor[1], ipcon)
					obj.set_temperature_callback_period(cbtimetemp)
					callback(obj.get_temperature())
					obj.register_callback(obj.CALLBACK_TEMPERATURE, callback)
				elif (sensor[2] == SensorType.humi):
					obj = Humidity(sensor[1], ipcon)
					callback(obj.get_humidity())
					obj.set_humidity_callback_period(cbtimehumi)
					obj.register_callback(obj.CALLBACK_HUMIDITY, callback)
				elif(sensor[2] == SensorType.ambi):
					obj = AmbientLight(sensor[1], ipcon)
					obj.set_illuminance_callback_period(cbtimeambi)
					callback(obj.get_illuminance())
					obj.register_callback(obj.CALLBACK_ILLUMINANCE, callback)
				elif (sensor[2] == SensorType.baro):
					obj = Barometer(sensor[1], ipcon)
					callback(obj.get_air_pressure())
					obj.set_air_pressure_callback_period(cbtimebaro)
					obj.register_callback(obj.CALLBACK_AIR_PRESSURE,callback)
				else:
					continue
				connected.append(obj)
			raw_input('Press key to exit\n')
			ipcon.disconnect()
			log.write('stop logging... @'+time.ctime()+"\n")
		except Exception as inst:
			#connection failed, log and exit
			logger.printException(inst)
		os.remove(lockname)
	else:
		print('lock file active!!')
		log.write('lock collision: lock "all" active @ '+time.ctime()+"\n")

