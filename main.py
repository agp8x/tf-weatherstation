#!/usr/bin/env python3
# -*- coding: utf-8 -*-  

import os.path
import os
import time
import logging

from Logger import Logger
from Setup import ConnectionSetup
import settings

def setupLogger():
	log = logging.getLogger("weatherstation")
	log.setLevel(logging.INFO)
	ch = logging.StreamHandler()
	ch.setLevel(logging.DEBUG)
	#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	formatter = logging.Formatter('%(asctime)s:[%(levelname)s] - %(message)s')
	ch.setFormatter(formatter)
	log.addHandler(ch)
	fh = logging.FileHandler(os.path.join(settings.logs, "logging.log"))
	fh.setFormatter(formatter)
	log.addHandler(fh)
	return log

logi = setupLogger()

def check_dirs_and_files():
	# log
	if not os.path.exists(settings.logs):
		os.mkdir(settings.logs, 0000755)
	#if not os.path.exists(settings.logname):
	#	open(settings.logname, 'w').close()
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
		lock = open(lockfile, 'w')
		lock.write( str(time.time()) )
		lock.close()
		return True
	return False

def freeLock(lockfile = settings.lockname):
	if os.path.exists(lockfile):
		os.remove(lockfile)

def formatHost(host):
	return "%s:%d" % (host['name'], host['port'])

if __name__ == "__main__":
	check_dirs_and_files()
	try:
		logi.info("setting up all sensors")
		while True:
			if obtainLock():
				logger = Logger(logi)
				connections = []
				connectedSensors = []
				for con in settings.SENSORS:
					try:
						logi.info("connecting to host '"+str(con)+"'")
						con = settings.SENSORS[con]
						conSetup = ConnectionSetup(logi)
						connection, sensors = conSetup.setupConnectionAndSensors(con['host'], con['sensors'], settings.TIMES, logger.cb_generic)
						connections.append(connection)
						connectedSensors.append(sensors)
						logi.info("started logging at " + formatHost(con['host']))
					except Exception as inst:
						#connection failed, log and exit
						#TODO: logger.printException(inst)
						logi.error("connection failed: "+str(inst))
				raw_input("Press key to restart\n")
				logi.info("stop logging... @" + time.ctime() + "\n")
				conSetup.disconnectAny(connections)
				freeLock()
			else:
				logi.critical("lock collision: lock 'all' active")
			logi.info("wait for retry (" + str(settings.waitDelay) + ")")
			time.sleep(settings.waitDelay)
	except KeyboardInterrupt:
		logi.info("keyboard-interrupt happened, cleaning up")
		conSetup.disconnectAny(connections)
		freeLock()

