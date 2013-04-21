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
UID1 = "7B5" 
name1="temp1"#not used
UID2 = "8js"
name2="temp2"#not used
UID3 = "7RY"
name3="humi1"
UID4="8Fw"
name4="ambi1"
UID5="8DJ"
name5="ambi2"
UID6="bB7"
name6="baro1"

tempSensors=2

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_temperature import Temperature
from tinkerforge.bricklet_humidity import Humidity
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.bricklet_barometer import Barometer

import time
import string
import os.path
import os
import sys,traceback
import array
cbtimetemp=30000
cbtimehumi=30000
cbtimeambi=60000
cbtimebaro=30000

tempmaxdiff=200 # 200== 2.0 C

logs='logs'
locks='locks'
records='records'

lockname=locks+"/all.lock"
log=open(logs+"/all.log",'a')

def preptime():
	now=time.localtime()
	day=now.tm_mday
	month=now.tm_mon
	year=str(now.tm_year)
	if(day<10):
		day="0"+str(day)
	else:
		day=str(day)
	if(month<10):
		month="0"+str(month)
	else:
		month=str(month)
	return month+"."+day+"."+year

def temp_rise(old,new,sensor):
	if(old==20000):
		return True
	if((old-new)>tempmaxdiff or (new-old)>tempmaxdiff):
		log.write('error checking '+sensor+';prev('+str(old)+');cur('+str(new)+'); ... @'+time.ctime()+"\n")
		log.flush()
		return False
	else:
		return True
##########################################
# common function to write value to file #
##########################################
def write_value(value,name):
	valuename=records+"/"+name+"_"+preptime()
	valuelog=open(valuename,'a')
	valuelog.write(str(value) + ';' + str(int(time.time())) +"\n")
	valuelog.close()
#end#

prev_temps=[20000,20000]

#########################################
# generic callback for temp#		#
#########################################
def callback_temperature(value,sensor):
	if(sensor>=tempSensors):
		return
	global prev_temps
	name="temp"+str(sensor+1)
	if(temp_rise(prev_temps[sensor],value,name)):
		write_value(value,name)
		prev_temps[sensor]=value
#end#

##########################################
# callbacks for temp1+2			 #
##########################################
def cb_temperature1(value):
	callback_temperature(value,0)
	print(name1+': ' + str(value/100.0) + ' °C,' + str(time.ctime()))
#
def cb_temperature2(value):
	callback_temperature(value,1)
	print(name2+': ' + str(value/100.0) + ' °C,' + str(time.ctime()))
#end#
	
###########################################
# callback for humidity1		  #
###########################################
def cb_humidity3(rh):
	write_value(rh,name3)
	print(name3 +': '+ str(rh/10.0) + ' %RH,' + str(time.ctime()))
#end#
	
###########################################
# callback for ambi-light1+2		  #
###########################################
def cb_illuminance4(illuminance):
	write_value(illuminance,name4)
	print(name4 +': '+ str(illuminance/10.0) + ' Lux,' + str(time.ctime()))
#
def cb_illuminance5(illuminance):
	write_value(illuminance,name5)
	print(name5 +': '+ str(illuminance/10.0) + ' Lux,' + str(time.ctime()))
#end#
	
###########################################
# callback for barometer1		  #
###########################################
def cb_pressure6(pressure):
	write_value(pressure,name6)
	print(name6+": "+str(pressure/1000)+ "mbar"+str(time.ctime()))
#end#
	
###########################################
# exception logging			  #
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

if not os.path.exists(lockname):
	if __name__ == "__main__":
		lock=open(lockname,'w')
		lock.write(str(time.time()))
		lock.close()
		#
		try:
			ipcon = IPConnection()
			t1 = Temperature(UID1, ipcon)
			t2 = Temperature(UID2, ipcon)
			h3 = Humidity(UID3, ipcon)
			al4 = AmbientLight(UID4, ipcon)
			al5 = AmbientLight(UID5, ipcon)
			b6 = Barometer(UID6, ipcon)
			
			
			ipcon.connect(HOST, PORT)
		except Exception as inst:
			printException(inst)
		else:
			cb_temperature1(t1.get_temperature())
			cb_temperature2(t2.get_temperature())
			cb_humidity3(h3.get_humidity())
			cb_illuminance4(al4.get_illuminance())
			cb_illuminance5(al5.get_illuminance())
			cb_pressure6(b6.get_air_pressure())
			
			t1.set_temperature_callback_period(cbtimetemp)
			t2.set_temperature_callback_period(cbtimetemp)
			h3.set_humidity_callback_period(cbtimehumi)
			al4.set_illuminance_callback_period(cbtimeambi)
			al5.set_illuminance_callback_period(cbtimeambi)
			b6.set_air_pressure_callback_period(cbtimebaro)
			
			log.write('start logging "all" ... @'+time.ctime()+"\n")
			log.flush()
			
			t1.register_callback(t1.CALLBACK_TEMPERATURE, cb_temperature1)
			t2.register_callback(t2.CALLBACK_TEMPERATURE, cb_temperature2)
			h3.register_callback(h3.CALLBACK_HUMIDITY, cb_humidity3)
			al4.register_callback(al4.CALLBACK_ILLUMINANCE, cb_illuminance4)
			al5.register_callback(al5.CALLBACK_ILLUMINANCE, cb_illuminance5)
			b6.register_callback(b6.CALLBACK_AIR_PRESSURE,cb_pressure6)
			
			raw_input('Press key to exit\n')
			ipcon.disconnect()
		
			log.write('stop logging... @'+time.ctime()+"\n")
		
		os.remove(lockname)
else:
	print('lock file active!!')
	log.write('lock collision: lock "all" active @ '+time.ctime()+"\n")


