#!/usr/bin/env python3
# -*- coding: utf-8 -*-  


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
from settings import SensorType
import settings

def check_dirs_and_files():
	# log
	if not os.path.exists(settings.logs):
		os.mkdir(settings.logs)
	if not os.path.exists(settings.logname):
		open(settings.logname, 'w').close()
	if not os.path.exists(settings.exceptionlog):
		file=open(settings.exceptionlog, 'w')
		file.write("<exceptions></exceptions>")
		file.close()
	# lock
	if not os.path.exists(settings.locks):
		os.mkdir(settings.locks)
	# records
	if not os.path.exists(settings.records):
		os.mkdir(settings.records)

if __name__ == "__main__":
	check_dirs_and_files()
	log=open(settings.logname,'a')
	try:
		while True:
			if not os.path.exists(settings.lockname):
				lock=open(settings.lockname,'w')
				lock.write(str(time.time()))
				lock.close()
				# lock obtained
				logger=Logger(log)
				try:
					ipcon = IPConnection()
					# connect
					ipcon.connect(settings.HOST, settings.PORT)
					log.write('start logging "all" ... @'+time.ctime()+"\n")
					log.flush()
					connected=[]
					for i,sensor in enumerate(settings.SENSORS):
						print("setup device "+sensor[0]+" ("+str(i)+")")
						callback=partial(logger.cb_generic, sensor=i, type=sensor[2])
						cbtime=settings.TIMES[sensor[2]]
						if(sensor[2] == SensorType.temp):
							obj = Temperature(sensor[1], ipcon)
							obj.set_temperature_callback_period(cbtime)
							callback(obj.get_temperature())
							obj.register_callback(obj.CALLBACK_TEMPERATURE, callback)
						elif (sensor[2] == SensorType.humi):
							obj = Humidity(sensor[1], ipcon)
							obj.set_humidity_callback_period(cbtime)
							callback(obj.get_humidity())
							obj.register_callback(obj.CALLBACK_HUMIDITY, callback)
						elif(sensor[2] == SensorType.ambi):
							obj = AmbientLight(sensor[1], ipcon)
							obj.set_illuminance_callback_period(cbtime)
							callback(obj.get_illuminance())
							obj.register_callback(obj.CALLBACK_ILLUMINANCE, callback)
						elif (sensor[2] == SensorType.baro):
							obj = Barometer(sensor[1], ipcon)
							callback(obj.get_air_pressure())
							obj.set_air_pressure_callback_period(cbtime)
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
				os.remove(settings.lockname)
			else:
				print('lock file active!!')
				log.write('lock collision: lock "all" active @ '+time.ctime()+"\n")
		print("something failed, wait for retry ("+settings.waitDelay+")")
		time.sleep(settings.waitDelay)
	except KeyboardInterrupt:
		print("Interrupted")
		log.write("keyboard-interrupt happened @"+time.ctime()+"\n")
		os.remove(settings.lockname)
		ipcon.disconnect()

