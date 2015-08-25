#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import os

class SensorType:
	none = 0
	temp = 1 # temperature bricklet
	humi = 2 # humidity bricklet
	ambi = 3 # ambient light bricklet
	baro = 4 # barometer bricklet
	rain = 5 # IO4 #TODO
	iram = 6 # temperature ir bricklet, ambient
	irob = 7 # temperature ir bricklet, object

DEFAULTS ={
	"hosts":{
		"HOSTDESC_i":{
			"host":{"name":"HOSTNAME_OR_IP","port":4223},
			"sensors":{
				"NAME":["UID", "SensorType.TYPE"]}
			}
	},
	"sensor_properties":{
		"SensorType.none": [0, 0, ""],
		"SensorType.temp": [30000, 100.0, "°C"],
		"SensorType.humi": [30000, 10.0, "%RH"],
		"SensorType.ambi": [60000, 10.0, "Lux"],
		"SensorType.baro": [60000, 1000, "mbar"],
		"SensorType.rain": [0, 2.5, "l/qm"],
		"SensorType.iram": [1000, 10.0, "°C"],
		"SensorType.irob": [1000, 10.0, "°C"]},
	"tempmaxdiff":200,
	"prev_temps_default":20000,
	"logs":'logs',
	"locks":'locks',
	"records":'records',
	"arch":'arch',
	"lockname":"all.lock",
	"logname":"logging.log",
	"exceptionlog":"exceptions.xml",
	"recordlog":"record.log",
	"movelog":"move.log",
	"movelock":"last_move",
	"waitDelay":10,
	"tempSensors":0,
	"loglevel": "info",
	"datalog": "info",
	"dataecho": "info"
}
class Settings(dict):
	def __getattr__(self,name):
		if name in self:
			return self[name]
		return DEFAULTS[name]
	def __setattr__(self,name,value):
		self[name]=value
	def __delattr__(self,name):
		del self[name]
def load_json(filename="set.json"):
	values=json.load(open('set.json'), object_hook=Settings)
	sensors_name="hosts"
	if sensors_name in values:
		for host in values[sensors_name]:
			for sensor in values[sensors_name][host]["sensors"]:
				sensor = values[sensors_name][host]["sensors"][sensor]
				sensor[1] = eval(sensor[1])
	sensor_props = "sensor_properties"
	if sensor_props in values:
		new_units={}
		for unit in values[sensor_props]:
			new_units[eval(unit)] = values[sensor_props][unit]
		values[sensor_props] = new_units
	return values
def setupLogger():
	level = getattr(logging, settings.loglevel.upper(), logging.INFO)
	log = logging.getLogger("weatherstation")
	log.setLevel(level)
	ch = logging.StreamHandler()
	#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	formatter = logging.Formatter('%(asctime)s:[%(levelname)s] - %(message)s')
	ch.setFormatter(formatter)
	log.addHandler(ch)
	fh = logging.FileHandler(os.path.join(settings.logs, settings.logname))
	fh.setFormatter(formatter)
	log.addHandler(fh)
	return log

def setup_data_log():
	level = getattr(logging, settings.datalog.upper(), logging.INFO)
	log = logging.getLogger("weatherstation.datalog")
	log.setLevel(level)
	fh = logging.FileHandler(os.path.join(settings.records, settings.recordlog))
	fformat = logging.Formatter()
	fh.setFormatter(fformat)
	log.addHandler(fh)
	log.propagate = False
	return log

def setup_data_echo():
	level = getattr(logging, settings.dataecho.upper(), logging.INFO)
	log = logging.getLogger("weatherstation.data")
	log.setLevel(level)
	ch = logging.StreamHandler()
	formatter = logging.Formatter('%(asctime)s:[DATA] - %(message)s')
	ch.setFormatter(formatter)
	log.addHandler(ch)
	log.propagate = False
	return log

settings=load_json()
hosts_name = "hosts"
if hosts_name in settings:
	tempSensors=0
	for i in settings[hosts_name]:
		for j in settings[hosts_name][i]['sensors']:
			if settings[hosts_name][i]['sensors'][j][1] == SensorType.temp:
				tempSensors+=1
	settings.tempSensors=tempSensors
"""
	0: {
		"host": {
			"name": "192.168.2.60",
			"port": 4223
		},
		"sensors": {
			"temp1": ["7B5", SensorType.temp],
			"temp2": ["8js", SensorType.temp],
			"humi1": ["7RY", SensorType.humi],
			"ambi1": ["8Fw", SensorType.ambi],
			"ambi2": ["8DJ", SensorType.ambi],
			"baro1": ["bB7", SensorType.baro],
			"temp3": ["8ms", SensorType.temp],
			"humi2": ["9V5", SensorType.humi],
		}
	},"""

