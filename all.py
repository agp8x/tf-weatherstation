#!/usr/bin/env python
# -*- coding: utf-8 -*-  


import os.path
import os
import time

from Logger import Logger

#HOST = "localhost"
HOST = "192.168.2.30"
PORT = 4223

UID = ["7B5", "8js", "7RY", "8Fw", "8DJ", "bB7"]
NAMES = ["temp1", "temp2", "humi1", "ambi1", "ambi2", "baro1"]


try:
	from tinkerforge.ip_connection import IPConnection
	from tinkerforge.bricklet_temperature import Temperature
	from tinkerforge.bricklet_humidity import Humidity
	from tinkerforge.bricklet_ambient_light import AmbientLight
	from tinkerforge.bricklet_barometer import Barometer
except ImportError:
	print("package 'tinkerforge' not installed, canceling")
	raise

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



if __name__ == "__main__":
	if not os.path.exists(lockname):
		lock=open(lockname,'w')
		lock.write(str(time.time()))
		lock.close()
		# lock obtained
		logger=Logger(NAMES, (tempSensors, prev_temps_default, tempmaxdiff), log, records)
		try:
			ipcon = IPConnection()
			t0 = Temperature(UID[0], ipcon)
			t1 = Temperature(UID[1], ipcon)
			h2 = Humidity(UID[2], ipcon)
			al3 = AmbientLight(UID[3], ipcon)
			al4 = AmbientLight(UID[4], ipcon)
			b5 = Barometer(UID[5], ipcon)
			# connect
			ipcon.connect(HOST, PORT)
			# ensure all sensors are present
			logger.cb_temperature0(t0.get_temperature())
			logger.cb_temperature1(t1.get_temperature())
			logger.cb_humidity2(h2.get_humidity())
			logger.cb_illuminance3(al3.get_illuminance())
			logger.cb_illuminance4(al4.get_illuminance())
			logger.cb_pressure5(b5.get_air_pressure())
			
			t0.set_temperature_callback_period(cbtimetemp)
			t1.set_temperature_callback_period(cbtimetemp)
			h2.set_humidity_callback_period(cbtimehumi)
			al3.set_illuminance_callback_period(cbtimeambi)
			al4.set_illuminance_callback_period(cbtimeambi)
			b5.set_air_pressure_callback_period(cbtimebaro)
			
			log.write('start logging "all" ... @'+time.ctime()+"\n")
			log.flush()
			
			t0.register_callback(t0.CALLBACK_TEMPERATURE, logger.cb_temperature0)
			t1.register_callback(t1.CALLBACK_TEMPERATURE, logger.cb_temperature1)
			h2.register_callback(h2.CALLBACK_HUMIDITY, logger.cb_humidity2)
			al3.register_callback(al3.CALLBACK_ILLUMINANCE, logger.cb_illuminance3)
			al4.register_callback(al4.CALLBACK_ILLUMINANCE, logger.cb_illuminance4)
			b5.register_callback(b5.CALLBACK_AIR_PRESSURE,logger.cb_pressure5)
			
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

