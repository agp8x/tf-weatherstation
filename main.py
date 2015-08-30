#!/usr/bin/env python3
# -*- coding: utf-8 -*-  

import os
import time

from Logger import Logger
from Setup import ConnectionSetup
from config import settings, setupLogger

log = setupLogger()
lockpath=os.path.join(settings.locks,settings.lockname)

def check_dirs_and_files():
	# log
	if not os.path.exists(settings.logs):
		os.mkdir(settings.logs, 0o000755)
	if not os.path.exists(os.path.join(settings.logs,settings.exceptionlog)):
		file=open(os.path.join(settings.logs,settings.exceptionlog), 'w')
		file.write("<exceptions></exceptions>")
		file.close()
	# lock
	if not os.path.exists(settings.locks):
		os.mkdir(settings.locks, 0o000755)
	# records
	if not os.path.exists(settings.records):
		os.mkdir(settings.records, 0o000755)

def obtainLock():
	if not os.path.exists(lockpath):
		lock = open(lockpath, 'w')
		lock.write( str(time.time()) )
		lock.close()
		return True
	return False

def freeLock():
	if os.path.exists(lockpath):
		os.remove(lockpath)

def formatHost(host):
	return "%s:%d" % (host['name'], host['port'])

if __name__ == "__main__":
	try:
		input = raw_input
	except NameError:
		pass
	check_dirs_and_files()
	conSetup = ConnectionSetup(log)
	connectedSensors = []
	connections = []
	try:
		log.info("setting up all sensors")
		while True:
			if obtainLock():
				logger = Logger(log)
				for con in settings.hosts:
					try:
						log.info("connecting to host '"+str(con)+"'")
						con = settings.hosts[con]
						connection, sensors = conSetup.setupConnectionAndSensors(con['host'], con['sensors'], logger.cb_generic)
						connections.append(connection)
						connectedSensors.append(sensors)
						log.info("started logging at " + formatHost(con['host']))
					except Exception as inst:
						#connection failed, log and exit
						#TODO: logger.printException(inst)
						log.error("connection failed: "+str(inst))
				input("Press key to restart\n")
				log.info("stop logging... @" + time.ctime() + "\n")
				conSetup.disconnectAny(connections)
				freeLock()
			else:
				log.critical("lock collision: lock 'all' active")
			log.info("wait for retry (" + str(settings.waitDelay) + ")")
			time.sleep(settings.waitDelay)
	except KeyboardInterrupt:
		log.info("keyboard-interrupt happened, cleaning up")
		conSetup.disconnectAny(connections)
		freeLock()

