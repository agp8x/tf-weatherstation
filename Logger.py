#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import traceback
import xml.etree.ElementTree as ET

from timeFunctions import *
from settings import SensorType
import settings

class Logger(object):
	def __init__(self, log):
		self.names = settings.NAMES
		self.temp_sensors = settings.tempSensors
		self.temp_prev_default=settings.prev_temps_default
		self.prev_temps =[]
		for i in range(self.temp_sensors):
			self.prev_temps.append(self.temp_prev_default)
		self.temp_max_diff = settings.tempmaxdiff
		self.log = log
		self.records = settings.records
	
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
		unit=settings.SENSOR_VALUES[type]
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
