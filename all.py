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

from Logger import Logger
from Setup import Setup
from settings import SensorType
import settings

def check_dirs_and_files():
	# log
	if not os.path.exists(settings.logs):
		os.mkdir(settings.logs, 0000755)
	if not os.path.exists(settings.logname):
		open(settings.logname, 'w').close()
	if not os.path.exists(settings.exceptionlog):
		file=open(settings.exceptionlog, 'w')
		file.write("<exceptions></exceptions>")
		file.close()
	# lock
	if not os.path.exists(settings.locks):
		os.mkdir(settings.locks, 0000755)
	# records
	if not os.path.exists(settings.records):
		os.mkdir(settings.records, 0000755)

def obtainLock(lockfile = settings.lockname):
	if not os.path.exists(lockfile):
		lock=open(lockfile,'w')
		lock.write(str(time.time()))
		lock.close()
		return True
	return False
def freeLock(lockfile = settings.lockname):
	if os.path.exists(lockfile):
		os.remove(lockfile)
def disconnect(connection):
	if not connection.get_connection_state() is IPConnection.CONNECTION_STATE_DISCONNECTED:
		connection.disconnect()

if __name__ == "__main__":
	check_dirs_and_files()
	log=open(settings.logname,'a')
	try:
		while True:
			if obtainLock():
				logger=Logger(log, )
				try:
					ipcon = IPConnection()
					# connect
					ipcon.connect(settings.HOST, settings.PORT)
					log.write('start logging "all" ... @'+time.ctime()+"\n")
					log.flush()
					setup = Setup(ipcon, settings.SENSORS, settings.TIMES, logger.cb_generic)
					connected = setup.setupSensors()
					raw_input('Press key to restart\n')
					disconnect(ipcon)
					log.write('stop logging... @'+time.ctime()+"\n")
				except Exception as inst:
					#connection failed, log and exit
					logger.printException(inst)
					print(inst)
				freeLock()
			else:
				print('lock file active!!')
				log.write('lock collision: lock "all" active @ '+time.ctime()+"\n")
			print("wait for retry ("+str(settings.waitDelay)+")")
			time.sleep(settings.waitDelay)
	except KeyboardInterrupt:
		print("Interrupted, cleaning up")
		disconnect(ipcon)
		log.write("keyboard-interrupt happened @"+time.ctime()+"\n")
		freeLock()

