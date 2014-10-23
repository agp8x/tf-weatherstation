#!/usr/bin/python3
# -*- coding: utf-8 -*-

try:
	from tinkerforge.ip_connection import IPConnection
	from tinkerforge.bricklet_temperature import Temperature
	from tinkerforge.bricklet_humidity import Humidity
	from tinkerforge.bricklet_ambient_light import AmbientLight
	from tinkerforge.bricklet_barometer import Barometer
except ImportError:
	print("package 'tinkerforge' not installed, canceling")
	raise
from functools import partial
import traceback
from settings import SensorType

class Setup(object):

	def __init__(self, connection, sensors, cbtimes, cb_generic):
		self.connection = connection
		self.sensors = sensors
		self.cbtimes = cbtimes
		self.cb_generic = cb_generic

	def parametrizedCallback(self, name, type):
		return partial(self.cb_generic, sensor=name, type=type)
		
	def setupTemp(self, callback, id, cbtime):
		obj = Temperature(id, self.connection)
		obj.set_temperature_callback_period(cbtime)
		callback(obj.get_temperature())
		obj.register_callback(obj.CALLBACK_TEMPERATURE, callback)
		return obj
		
	def setupHumi(self, callback, id, cbtime):
		obj = Humidity(id, self.connection)
		obj.set_humidity_callback_period(cbtime)
		callback(obj.get_humidity())
		obj.register_callback(obj.CALLBACK_HUMIDITY, callback)
		return obj
		
	def setupAmbi(self, callback, id, cbtime):
		obj = AmbientLight(id, self.connection)
		obj.set_illuminance_callback_period(cbtime)
		callback(obj.get_illuminance())
		obj.register_callback(obj.CALLBACK_ILLUMINANCE, callback)
		return obj
		
	def setupBaro(self, callback, id, cbtime):
		obj = Barometer(id, self.connection)
		callback(obj.get_air_pressure())
		obj.set_air_pressure_callback_period(cbtime)
		obj.register_callback(obj.CALLBACK_AIR_PRESSURE,callback)
		return obj
	
	def setupNone(self, callback, id, cbtime):
		obj = "None " + str(id)
		return obj

	def genericSensorSetup(self, name, sensor):
		status = "setup device "+ sensor[0] +" ("+ name +"): "
		callback = self.parametrizedCallback(name, type=sensor[1])
		cbtime = self.cbtimes[sensor[1]]
		try:
			if sensor[1] is SensorType.temp:
				obj = self.setupTemp(callback, sensor[0], cbtime)
			elif sensor[1] is SensorType.humi:
				obj = self.setupHumi(callback, sensor[0], cbtime)
			elif sensor[1] is SensorType.ambi:
				obj = self.setupAmbi(callback, sensor[0], cbtime)
			elif sensor[1] is SensorType.baro:
				obj = self.setupBaro(callback, sensor[0], cbtime)
			status += "OK"
		except Exception as e:
			status += "FAIL"
			#print(e)
			#print(traceback.format_exc())
		print(status)
		obj = self.setupNone(callback, sensor[0] + name, cbtime)
		return obj
		
	def setupSensors(self):
		connected=[]
		for name in self.sensors:
			sensor = self.sensors[name]
			obj = self.genericSensorSetup(name, sensor)
			connected.append(obj)
		return connected

	
