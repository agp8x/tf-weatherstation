#!/usr/bin/python3
# -*- coding: utf-8 -*-

from functools import partial
import traceback

try:
    from tinkerforge.ip_connection import IPConnection
except ImportError:
    print("package 'tinkerforge' not installed, canceling")
    raise Exception("package 'tinkerforge' not installed, canceling")

from config import SensorType, settings, SENSOR_CONFIGS


class ConnectionSetup(object):
    def __init__(self, log):
        self.log = log
        self.__connections__ = []

    def setup_connection(self, host):
        ipcon = IPConnection()
        try:
            ipcon.connect(host['name'], host['port'])
            self.log.info("connection to '%s:%s' established", host['name'], host['port'])
        except ConnectionError:
            self.log.error("connection to '%s:%s' failed", host['name'], host['port'])
        self.__connections__.append(ipcon)
        return ipcon

    def setup_connection_and_sensors(self, host, sensors, logger):
        ipcon = self.setup_connection(host)
        sensor_setup = SensorSetup(ipcon, sensors, logger, self.log)
        connected_sensors = sensor_setup.setup_sensors()
        return ipcon, connected_sensors

    def disconnect_any(self, connections):
        if connections is None:
            connections = self.__connections__
        for connection in connections:
            if not connection.get_connection_state() is IPConnection.CONNECTION_STATE_DISCONNECTED:
                self.log.debug("disconnecting (%s)", connection)
                connection.disconnect()


class SensorSetup(object):
    def __init__(self, connection, sensors, logger, log):
        self.connection = connection
        self.sensors = sensors
        self.logger = logger
        self.log = log
        self._previous_sensors = {}

    def parametrized_callback(self, name, type):
        return partial(self.logger.cb_generic, sensor=name, type=type)

    def parametrized_callback_delta(self, name, type, getter):
        return partial(self.logger.cb_delta, name=name, type=type, getter=getter)

    def __setupSensor__(self, name, sensor):
        sensor_id = sensor[0]
        sensor_type = sensor[1]
        var = SENSOR_CONFIGS[sensor_type]
        if sensor_id in self._previous_sensors:
            self.log.debug("reusing instance for %s", sensor_id)
            obj = self._previous_sensors[sensor_id]  # restore instance for another callback
        else:
            self.log.debug("new instance for %s", sensor_id)
            obj = var['obj'](sensor_id, self.connection)  # construct instance
            self._previous_sensors[sensor_id] = obj  # save instance for multiple callbacks
        cbtime = settings.sensor_properties[sensor_type][0]
        if 'delta' in var:
            callback = self.parametrized_callback_delta(name, sensor_type, partial(var['get'], obj))
        else:
            callback = self.parametrized_callback(name, type=sensor_type)
        var['setcb'](obj, cbtime)  # set callback period
        callback(var['get'](obj))  # execute callback with raw getter as value
        obj.register_callback(var['cb'], callback)  # register callback
        return obj

    def generic_sensor_setup(self, name, sensor):
        status = "setup device " + sensor[0] + " (" + name + "):"
        obj = None
        if sensor[1] is SensorType.rain:
            self.log.error("rain is not yet implemented (%s, %s)", sensor[0], name)
            return None
        elif not sensor[1] in SENSOR_CONFIGS:
            self.log.error("%s FAIL (unknown type)", status)
            return None
        try:
            obj = self.__setupSensor__(name, sensor)
            self.log.info("%s OK", status)
        except Exception as e:
            self.log.error("%s FAIL:: %s (%s)", status, e, traceback.format_exc())
        return obj

    def setup_sensors(self):
        connected = []
        for name in self.sensors:
            sensor = self.sensors[name]
            obj = self.generic_sensor_setup(name, sensor)
            connected.append(obj)
        return connected
