#!/usr/bin/env python3
# -*- coding: utf-8 -*-  

import os.path
import os
import time

from Logger import Logger
from ConnectionSetup import ConnectionSetup
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

def formatHost(host):
	return "%s:%d"%(host['name'], host['port'])

if __name__ == "__main__":
	check_dirs_and_files()
	log=open(settings.logname,'a')
	try:
		log.write('setting up "all" ... @'+time.ctime()+"\n")
		while True:
			if obtainLock():
				logger=Logger(log, )
				try:
					connections = []
					connectedSensors = []
					for con in settings.SENSORS:
						con = settings.SENSORS[con]
						conSetup = ConnectionSetup()
						connection, sensors = conSetup.setupConnectionAndSensors(con['host'], con['sensors'], settings.TIMES, logger.cb_generic)
						connections.append(connection)
						connectedSensors.append(sensors)
						log.write("started logging at %s ... @ %s\n"% (formatHost(con['host']), time.ctime()))
					log.flush()
					raw_input('Press key to restart\n')
					log.write('stop logging... @'+time.ctime()+"\n")
					conSetup.disconnectAny(connections)
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
		print(" Interrupted, cleaning up")
		conSetup.disconnectAny(connections)
		log.write("keyboard-interrupt happened @"+time.ctime()+"\n")
		log.close()
		freeLock()

