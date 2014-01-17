#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import traceback
from timeFunctions import *
import xml.etree.ElementTree as ET

#class SensorType(Enum):
class SensorType:
	none = 0
	temp = 1
	humi = 2
	ambi = 3
	baro = 4
	rain = 5

sensorValues=[
	(0,''),
	(100.0, '°C'),
	(10.0, '%RH'),
	(10.0, 'Lux'),
	(1000, 'mbar'),
	(2.5, 'l/qm')
]

class Logger(object):
	def __init__(self,names, temperature_config, log, records):
		self.names = names
		self.temp_sensors = temperature_config[0]
		self.temp_prev_default=temperature_config[1]
		self.prev_temps =[]
		for i in range(self.temp_sensors):
			self.prev_temps.append(temperature_config[1])
		self.temp_max_diff = temperature_config[2]
		self.log = log
		self.records = records
	
	def temp_rise(self,old,new,sensor):
		if(old==self.temp_prev_default):
			return True
		if((old-new)>self.temp_max_diff or (new-old)>self.temp_max_diff):
			self.log.write('error checking '+self.names[sensor]+';prev('+str(old)+');cur('+str(new)+'); ... @'+time.ctime()+"\n")
			self.log.flush()
			return False
		else:
			return True
	
	##########################################
	# common function to write value to file #
	##########################################
	def write_value(self,value,sensor):
		valuename=self.records+"/"+self.names[sensor]+"_"+preptime()
		valuelog=open(valuename,'a')
		valuelog.write(str(value) + ';' + str(int(time.time())) +"\n")
		valuelog.close()

	##########################################
	# generic callback	 					 #
	##########################################
	def cb_generic(self,value, sensor, type):
		if(type == SensorType.temp):
			if(self.temp_rise(self.prev_temps[sensor],value,sensor)):
				self.write_value(value,sensor)
				self.prev_temps[sensor]=value
		elif (type == SensorType.none):
			return
		else:
			self.write_value(value,sensor)
		unit=sensorValues[type]
		print(self.names[sensor] +': ' + str(value/unit[0]) + ' '+unit[1]+', ' + str(time.ctime()))
	
	###########################################
	# exception logging						  #
	###########################################
	def printException(self,inst):
		tree=ET.parse('logs/exceptions.xml')
		root=tree.getroot()
		new=ET.Element('exception',{'class':str(type(inst)).split("'")[1],'date':str(time.ctime()),'time':str(int(time.time())),'type':str(inst)})
		new.text=traceback.format_exc()
		root.append(new)
		tree.write('logs/exceptions.xml')
	
		self.log.write('an Exception happen during connection @'+time.ctime()+"\n")
		self.log.flush()
		print('an Exception happen during connection @'+time.ctime()+"\n")
	#end#
