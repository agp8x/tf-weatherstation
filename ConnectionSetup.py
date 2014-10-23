#!/usr/bin/python3
# -*- coding: utf-8 -*-

try:
	from tinkerforge.ip_connection import IPConnection
except ImportError:
	print("package 'tinkerforge' not installed, canceling")
	raise
from SensorSetup import SensorSetup

class ConnectionSetup(object):
		
	def setupConnection(self, host):
		ipcon = IPConnection()
		ipcon.connect(host['name'], host['port'])
		return (ipcon)
	
	def setupConnectionAndSensors(self, host, sensors, cbtimes, cb_generic):
		hostname = host['name']
		port = host['port']
		ipcon = IPConnection()
		ipcon.connect(hostname, port)
		sensorSetup = SensorSetup(ipcon, sensors, cbtimes, cb_generic)
		connectedSensors = sensorSetup.setupSensors()
		return (ipcon, connectedSensors)
	
	def disconnectAny(self, connections):
		for connection in connections:
			if not connection.get_connection_state() is IPConnection.CONNECTION_STATE_DISCONNECTED:
				connection.disconnect()

