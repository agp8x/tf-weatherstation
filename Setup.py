#!/usr/bin/python3
# -*- coding: utf-8 -*-

try:
	from tinkerforge.ip_connection import IPConnection
	from tinkerforge.bricklet_temperature import Temperature
	from tinkerforge.bricklet_humidity import Humidity
	from tinkerforge.bricklet_ambient_light import AmbientLight
	from tinkerforge.bricklet_barometer import Barometer
	from tinkerforge.bricklet_temperature_ir import BrickletTemperatureIR
except ImportError:
	print("package 'tinkerforge' not installed, canceling")
	raise
from functools import partial
import traceback
from settings import SensorType

class ConnectionSetup(object):
	def __init__(self, log):
		self.log = log
		
	def setupConnection(self, host):
		ipcon = IPConnection()
		ipcon.connect(host['name'], host['port'])
		return (ipcon)
	
	def setupConnectionAndSensors(self, host, sensors, cbtimes, cb_generic):
		hostname = host['name']
		port = host['port']
		ipcon = IPConnection()
		ipcon.connect(hostname, port)
		sensorSetup = SensorSetup(ipcon, sensors, cbtimes, cb_generic, self.log)
		connectedSensors = sensorSetup.setupSensors()
		return (ipcon, connectedSensors)
	
	def disconnectAny(self, connections):
		for connection in connections:
			if not connection.get_connection_state() is IPConnection.CONNECTION_STATE_DISCONNECTED:
				connection.disconnect()

class SensorSetup(object):

	def __init__(self, connection, sensors, cbtimes, cb_generic, log):
		self.connection = connection
		self.sensors = sensors
		self.cbtimes = cbtimes
		self.cb_generic = cb_generic
		self.log = log
		self._previous_sensors={}

	def parametrizedCallback(self, name, type):
		return partial(self.cb_generic, sensor=name, type=type)

	def getTemp(self):
		obj = Temperature
		setcb = obj.set_temperature_callback_period
		get = obj.get_temperature
		cb = Temperature.CALLBACK_TEMPERATURE
		return obj, setcb, get, cb

	def getHumi(self):
		obj = Humidity
		setcb = obj.set_humidity_callback_period
		get = obj.get_humidity
		cb = Humidity.CALLBACK_HUMIDITY
		return obj, setcb, get, cb

	def getAmbi(self):
		obj = AmbientLight
		setcb = obj.set_illuminance_callback_period
		get = obj.get_illuminance
		cb = AmbientLight.CALLBACK_ILLUMINANCE
		return obj, setcb, get, cb

	def getBaro(self):
		obj = Barometer
		setcb = obj.set_air_pressure_callback_period
		get = obj.get_air_pressure
		cb = Barometer.CALLBACK_AIR_PRESSURE
		return obj, setcb, get, cb

	def getIram(self):
		obj = BrickletTemperatureIR						# Object
		setcb = obj.set_ambient_temperature_callback_period	# set-callback-period-method-pointer
		get = obj.get_ambient_temperature					# value-get-method-pointer
		cb = BrickletTemperatureIR.CALLBACK_AMBIENT_TEMPERATURE			# callback identifier
		return obj, setcb, get, cb

	def getIrob(self):
		obj = BrickletTemperatureIR						# Object
		setcb = obj.set_object_temperature_callback_period	# set-callback-period-method-pointer
		get = obj.get_object_temperature					# value-get-method-pointer
		cb = BrickletTemperatureIR.CALLBACK_OBJECT_TEMPERATURE			# callback identifier
		return obj, setcb, get, cb

	#def getNew(self):
	#	obj = Bricklet						# Object
	#	setcb = obj.set_XXX_callback_period	# set-callback-period-method-pointer
	#	get = obj.get_XXX					# value-get-method-pointer
	#	cb = Bricklet.CALLBACK_XXX			# callback identifier
	#	return obj, setcb, get, cb

	def __setupSensor__(self, callback, id, cbtime, var):
		obj = None
		if id in self._previous_sensors:
			self.log.debug("reusing instance for %s", id)
			obj = self._previous_sensors[id]	# restore instance for another callback
		else:
			self.log.debug("new instance for %s", id)
			obj = var[0](id, self.connection)	# construct instance
			self._previous_sensors[id] = obj	# save instance for multiple callbacks
		var[1](obj, cbtime)						# set callback period
		callback(var[2](obj ), supress=True)	# execute callback with raw getter as value
		obj.register_callback(var[3], callback)	# register callback
		return obj

	def genericSensorSetup(self, name, sensor):
		status = "setup device "+ sensor[0] +" ("+ name +"):"
		callback = self.parametrizedCallback(name, type=sensor[1])
		cbtime = self.cbtimes[sensor[1]]
		obj = None
		if sensor[1] is SensorType.temp:
			var = self.getTemp()
		elif sensor[1] is SensorType.humi:
			var = self.getHumi()
		elif sensor[1] is SensorType.ambi:
			var = self.getAmbi()
		elif sensor[1] is SensorType.baro:
			var = self.getBaro()
		elif sensor[1] is SensorType.rain:
			self.log.error("rain is not yet implemented (%s, %s)", sensor[0], name)
			return None
		elif sensor[1] is SensorType.iram:
			var = self.getIram()
		elif sensor[1] is SensorType.irob:
			var = self.getIrob()
		else:
			self.log.error("%s FAIL (unknown type)", status)
			return None
		try:
			obj = self.__setupSensor__(callback, sensor[0], cbtime, var)
			self.log.info("%s OK", status)
		except Exception as e:
			self.log.error("%s FAIL:: %s",status, e)
		return obj

	def setupSensors(self):
		connected=[]
		for name in self.sensors:
			sensor = self.sensors[name]
			obj = self.genericSensorSetup(name, sensor)
			connected.append(obj)
		return connected

