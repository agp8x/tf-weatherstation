#!/usr/bin/python3
# -*- coding: utf-8 -*-

from functools import partial
import traceback

try:
	from tinkerforge.ip_connection import IPConnection
	from tinkerforge.bricklet_temperature import Temperature
	from tinkerforge.bricklet_humidity import Humidity
	from tinkerforge.bricklet_ambient_light import AmbientLight
	from tinkerforge.bricklet_barometer import Barometer
	from tinkerforge.bricklet_temperature_ir import BrickletTemperatureIR
except ImportError:
	print("package 'tinkerforge' not installed, canceling")
	raise Exception("package 'tinkerforge' not installed, canceling")

from config import SensorType
from config import settings

class ConnectionSetup(object):
	def __init__(self, log):
		self.log = log
		
	def setupConnection(self, host):
		ipcon = IPConnection()
		ipcon.connect(host['name'], host['port'])
		return (ipcon)
	
	def setupConnectionAndSensors(self, host, sensors, cb_generic):
		hostname = host['name']
		port = host['port']
		ipcon = IPConnection()
		ipcon.connect(hostname, port)
		sensorSetup = SensorSetup(ipcon, sensors, cb_generic, self.log)
		connectedSensors = sensorSetup.setupSensors()
		return (ipcon, connectedSensors)
	
	def disconnectAny(self, connections):
		for connection in connections:
			if not connection.get_connection_state() is IPConnection.CONNECTION_STATE_DISCONNECTED:
				connection.disconnect()

class SensorSetup(object):

	def __init__(self, connection, sensors, cb_generic, log):
		self.connection = connection
		self.sensors = sensors
		self.cb_generic = cb_generic
		self.log = log
		self._previous_sensors={}
		self._configs={
			#SensorType.none: {
			#	'obj': ,
			#	'setcb': ,
			#	'get': ,
			#	'cb': 
			#},
			SensorType.temp: {
				'obj': Temperature,
				'setcb': Temperature.set_temperature_callback_period,
				'get': Temperature.get_temperature,
				'cb': Temperature.CALLBACK_TEMPERATURE
			},
			SensorType.humi: {
				'obj': Humidity,
				'setcb': Humidity.set_humidity_callback_period,
				'get': Humidity.get_humidity,
				'cb': Humidity.CALLBACK_HUMIDITY
			},
			SensorType.ambi: {
				'obj': AmbientLight,
				'setcb': AmbientLight.set_illuminance_callback_period,
				'get': AmbientLight.get_illuminance,
				'cb': AmbientLight.CALLBACK_ILLUMINANCE
			},
			SensorType.baro: {
				'obj': Barometer,
				'setcb': Barometer.get_air_pressure_callback_period,
				'get': Barometer.get_air_pressure,
				'cb': Barometer.CALLBACK_AIR_PRESSURE
			},
			SensorType.iram: {
				'obj': BrickletTemperatureIR,
				'setcb': BrickletTemperatureIR.set_ambient_temperature_callback_period,
				'get': BrickletTemperatureIR.get_ambient_temperature,
				'cb': BrickletTemperatureIR.CALLBACK_AMBIENT_TEMPERATURE
			},
			SensorType.irob: {
				'obj': BrickletTemperatureIR,
				'setcb': BrickletTemperatureIR.set_object_temperature_callback_period,
				'get': BrickletTemperatureIR.get_object_temperature,
				'cb': BrickletTemperatureIR.CALLBACK_OBJECT_TEMPERATURE
			}
		}

	def parametrizedCallback(self, name, type):
		return partial(self.cb_generic, sensor=name, type=type)

	def __setupSensor__(self, callback, id, cbtime, var):
		obj = None
		if id in self._previous_sensors:
			self.log.debug("reusing instance for %s", id)
			obj = self._previous_sensors[id]	# restore instance for another callback
		else:
			self.log.debug("new instance for %s", id)
			obj = var['obj'](id, self.connection)	# construct instance
			self._previous_sensors[id] = obj	# save instance for multiple callbacks
		var['setcb'](obj, cbtime)						# set callback period
		callback(var['get'](obj ), supress=True)	# execute callback with raw getter as value
		obj.register_callback(var['cb'], callback)	# register callback
		return obj

	def genericSensorSetup(self, name, sensor):
		status = "setup device "+ sensor[0] +" ("+ name +"):"
		callback = self.parametrizedCallback(name, type=sensor[1])
		cbtime = settings.sensor_properties[sensor[1]][0]
		obj = None
		if sensor[1] is SensorType.rain:
			self.log.error("rain is not yet implemented (%s, %s)", sensor[0], name)
			return None
		elif not sensor[1] in self._configs:
			self.log.error("%s FAIL (unknown type)", status)
			return None
		try:
			obj = self.__setupSensor__(callback, sensor[0], cbtime, self._configs[sensor[1]])
			self.log.info("%s OK", status)
		except Exception as e:
			self.log.error("%s FAIL:: %s (%s)",status, e,traceback.format_exc())
		return obj

	def setupSensors(self):
		connected=[]
		for name in self.sensors:
			sensor = self.sensors[name]
			obj = self.genericSensorSetup(name, sensor)
			connected.append(obj)
		return connected

