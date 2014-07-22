#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#class SensorType(Enum):
class SensorType:
	none = 0
	temp = 1
	humi = 2
	ambi = 3
	baro = 4
	rain = 5


#HOST = "localhost"
HOST = "192.168.2.34"
PORT = 4223

SENSORS=[
	["temp1", "7B5", SensorType.temp],
	["temp2", "8js", SensorType.temp],
	["humi1", "7RY", SensorType.humi],
	["ambi1", "8Fw", SensorType.ambi],
	["ambi2", "8DJ", SensorType.ambi],
	["baro1", "bB7", SensorType.baro],
]

TIMES={
	SensorType.temp: 30000,
	SensorType.humi: 30000,
	SensorType.ambi: 60000,
	SensorType.baro: 60000,
}

tempmaxdiff=200 # 200== 2.0 C
prev_temps_default=20000

logs='logs'
locks='locks'
records='records'

lockname=locks+"/all.lock"
logname=logs+"/all.log"
exceptionlog=logs+"/exceptions.xml"

waitDelay = 10

########################################
# only change when new sensor is added #
########################################

SENSOR_VALUES=[
	(0,''),
	(100.0, '°C'),
	(10.0, '%RH'),
	(10.0, 'Lux'),
	(1000, 'mbar'),
	(2.5, 'l/qm')
]

###########################
# no manual change needed #
###########################

tempSensors=len(list(filter(lambda a: True if a[2]==SensorType.temp else False,SENSORS)))
NAMES=list(map(lambda a:a[0], SENSORS))

