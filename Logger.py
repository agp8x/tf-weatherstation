#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import sys
import traceback
from timeFunctions import *
import xml.etree.ElementTree as ET

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
			self.log.write('error checking temp '+sensor+';prev('+str(old)+');cur('+str(new)+'); ... @'+time.ctime()+"\n")
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

	#########################################
	# generic checking of temperature		#
	#########################################
	def check_and_write_temperature(self,value,sensor):
		if(sensor>=self.temp_sensors):
			return
		if(self.temp_rise(self.prev_temps[sensor],value,str(sensor+1))):
			self.write_value(value,sensor)
			self.prev_temps[sensor]=value

	##########################################
	# callbacks for temp1+2					 #
	##########################################
	def cb_temperature0(self,value):
		sensor=0
		self.check_and_write_temperature(value,sensor)
		print(self.names[sensor] +': ' + str(value/100.0) + ' °C,' + str(time.ctime()))
	#
	def cb_temperature1(self,value):
		sensor=1
		self.check_and_write_temperature(value,sensor)
		print(self.names[sensor] +': ' + str(value/100.0) + ' °C,' + str(time.ctime()))
	
	###########################################
	# callback for humidity1				  #
	###########################################
	def cb_humidity2(self,rh):
		sensor=2
		self.write_value(rh,sensor)
		print(self.names[sensor] +': '+ str(rh/10.0) + ' %RH,' + str(time.ctime()))
	
	###########################################
	# callback for ambi-light1+2		  	  #
	###########################################
	def cb_illuminance3(self,illuminance):
		sensor=3
		self.write_value(illuminance,sensor)
		print(self.names[sensor] +': '+ str(illuminance/10.0) + ' Lux,' + str(time.ctime()))
	#
	def cb_illuminance4(self,illuminance):
		sensor=4
		self.write_value(illuminance,sensor)
		print(self.names[sensor] +': '+ str(illuminance/10.0) + ' Lux,' + str(time.ctime()))
	
	###########################################
	# callback for barometer1		  		  #
	###########################################
	def cb_pressure5(self,pressure):
		sensor=5
		self.write_value(pressure,sensor)
		print(self.names[sensor] +": "+str(pressure/1000)+ "mbar"+str(time.ctime()))
	
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
