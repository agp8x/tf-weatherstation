#!/usr/bin/env python
# -*- coding: utf-8 -*-  

#rev2	:*barometer added (b1:#6) [not physically added!!!]
#	 *lcd disabled
#	 *exception-logging	[dont forget to add empty .xml!]
#rev3	:*generic callbacks	(15.01.2013-??)
#	 *lcd removed
#rev4	 *V2.0
#	 *barometer
#
#
#TODO:
#	*sensorNames=array()...
#	*sensorUIDs=array()?
#
#
#

#HOST = "localhost"
HOST = "192.168.2.30"
PORT = 4223

UID = ["7B5", "8js", "7RY", "8Fw", "8DJ", "bB7"]
NAME = ["temp1", "temp2", "humi1", "ambi1", "ambi2", "baro1"]

tempSensors=2

try:
	from tinkerforge.ip_connection import IPConnection
	from tinkerforge.bricklet_temperature import Temperature
	from tinkerforge.bricklet_humidity import Humidity
	from tinkerforge.bricklet_ambient_light import AmbientLight
	from tinkerforge.bricklet_barometer import Barometer
except ImportError:
	print("package 'tinkerforge' not installed, canceling")
	raise

import time
import string
import os.path
import os
import sys,traceback
import array
from timeFunctions import *


cbtimetemp=30000
cbtimehumi=30000
cbtimeambi=60000
cbtimebaro=60000

tempmaxdiff=200 # 200== 2.0 C
prev_temps=[20000,20000]

logs='logs'
locks='locks'
records='records'

lockname=locks+"/all.lock"
log=open(logs+"/all.log",'a')

def temp_rise(old,new,sensor):
	if(old==20000):
		return True
	if((old-new)>tempmaxdiff or (new-old)>tempmaxdiff):
		log.write('error checking temp '+sensor+';prev('+str(old)+');cur('+str(new)+'); ... @'+time.ctime()+"\n")
		log.flush()
		return False
	else:
		return True
##########################################
# common function to write value to file #
##########################################
def write_value(value,sensor):
	valuename=records+"/"+NAME[sensor]+"_"+preptime()
	valuelog=open(valuename,'a')
	valuelog.write(str(value) + ';' + str(int(time.time())) +"\n")
	valuelog.close()

#########################################
# generic checking of temperature		#
#########################################
def check_and_write_temperature(value,sensor):
	if(sensor>=tempSensors):
		return
	global prev_temps
	if(temp_rise(prev_temps[sensor],value,str(sensor+1))):
		write_value(value,sensor)
		prev_temps[sensor]=value

##########################################
# callbacks for temp1+2					 #
##########################################
def cb_temperature0(value):
	check_and_write_temperature(value,0)
	print(name1+': ' + str(value/100.0) + ' °C,' + str(time.ctime()))
#
def cb_temperature1(value):
	check_and_write_temperature(value,1)
	print(name2+': ' + str(value/100.0) + ' °C,' + str(time.ctime()))
	
###########################################
# callback for humidity1				  #
###########################################
def cb_humidity2(rh):
	write_value(rh,2)
	print(name3 +': '+ str(rh/10.0) + ' %RH,' + str(time.ctime()))
	
###########################################
# callback for ambi-light1+2		  	  #
###########################################
def cb_illuminance3(illuminance):
	write_value(illuminance,3)
	print(name4 +': '+ str(illuminance/10.0) + ' Lux,' + str(time.ctime()))
#
def cb_illuminance4(illuminance):
	write_value(illuminance,4)
	print(name5 +': '+ str(illuminance/10.0) + ' Lux,' + str(time.ctime()))
	
###########################################
# callback for barometer1		  		  #
###########################################
def cb_pressure5(pressure):
	write_value(pressure,5)
	print(name6+": "+str(pressure/1000)+ "mbar"+str(time.ctime()))
	
###########################################
# exception logging						  #
###########################################
def printException(inst):
	global log
	import xml.etree.ElementTree as ET
	tree=ET.parse('logs/exceptions.xml')
	root=tree.getroot()
	new=ET.Element('exception',{'class':str(type(inst)).split("'")[1],'date':str(time.ctime()),'time':str(int(time.time())),'type':str(inst)})
	new.text=traceback.format_exc()
	root.append(new)
	tree.write('logs/exceptions.xml')
	
	log.write('an Exception happen during connection @'+time.ctime()+"\n")
	print('an Exception happen during connection @'+time.ctime()+"\n")
	log.flush()
#end#

if __name__ == "__main__":
	if not os.path.exists(lockname):
		lock=open(lockname,'w')
		lock.write(str(time.time()))
		lock.close()
		# lock obtained
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
		except Exception as inst:
			#connection failed, log and exit
			printException(inst)
		else:
			cb_temperature0(t0.get_temperature())
			cb_temperature1(t1.get_temperature())
			cb_humidity2(h2.get_humidity())
			cb_illuminance3(al3.get_illuminance())
			cb_illuminance4(al4.get_illuminance())
			cb_pressure5(b5.get_air_pressure())
			
			t0.set_temperature_callback_period(cbtimetemp)
			t1.set_temperature_callback_period(cbtimetemp)
			h2.set_humidity_callback_period(cbtimehumi)
			al3.set_illuminance_callback_period(cbtimeambi)
			al4.set_illuminance_callback_period(cbtimeambi)
			b5.set_air_pressure_callback_period(cbtimebaro)
			
			log.write('start logging "all" ... @'+time.ctime()+"\n")
			log.flush()
			
			t0.register_callback(t0.CALLBACK_TEMPERATURE, cb_temperature0)
			t1.register_callback(t1.CALLBACK_TEMPERATURE, cb_temperature1)
			h2.register_callback(h2.CALLBACK_HUMIDITY, cb_humidity2)
			al3.register_callback(al3.CALLBACK_ILLUMINANCE, cb_illuminance3)
			al4.register_callback(al4.CALLBACK_ILLUMINANCE, cb_illuminance4)
			b5.register_callback(b5.CALLBACK_AIR_PRESSURE,cb_pressure5)
			
			raw_input('Press key to exit\n')
			ipcon.disconnect()
		
			log.write('stop logging... @'+time.ctime()+"\n")
		
		os.remove(lockname)
	else:
		print('lock file active!!')
		log.write('lock collision: lock "all" active @ '+time.ctime()+"\n")


