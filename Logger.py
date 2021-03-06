#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
import xml.etree.ElementTree as ET
import os

from timeFunctions import *
from config import SensorType, setup_data_echo, setup_data_log
from config import settings
from tinkerforge import ip_connection


class Logger(object):
    def __init__(self, log):
        self.temp_prev_default = settings.prev_temps_default
        self.prev_temps = self.__build_prev_temps__()
        self.temp_max_diff = settings.tempmaxdiff
        self.log = log
        self.records = settings.records
        self.dataecho = setup_data_echo()
        self.datalog = setup_data_log()

    def __build_prev_temps__(self):
        prev_temps = {}
        hosts_name = "hosts"
        if hosts_name in settings:
            for i in settings[hosts_name]:
                for j in settings[hosts_name][i]['sensors']:
                    if settings[hosts_name][i]['sensors'][j][1] == SensorType.temp:
                        prev_temps[j] = self.temp_prev_default
        return prev_temps

    def temp_rise(self, new, sensor):
        old = self.prev_temps[sensor]
        if old == self.temp_prev_default:
            return True
        if ((old - new) > self.temp_max_diff) or ((new - old) > self.temp_max_diff):
            self.log.error('error checking ' + sensor + ';prev(' + str(old) + ');cur(' + str(new) + ');')
            return False
        else:
            return True

    # common function to write value to file
    def write_value(self, value, sensor):
        if settings.legacy_record:
            valuename = self.records + "/" + sensor + "_" + preptime()
            valuelog = open(valuename, 'a')
            valuelog.write(str(value) + ';' + str(int(time.time())) + "\n")
            valuelog.close()
        self.datalog.info('%s;%s;%s', value, int(time.time()), sensor)

    # generic callback
    def cb_generic(self, value, sensor, type):
        if type == SensorType.temp:
            if self.temp_rise(value, sensor):
                self.write_value(value, sensor)
                self.prev_temps[sensor] = value
        elif type == SensorType.none:
            return
        else:
            self.write_value(value, sensor)
        unit = settings.sensor_properties[type]
        self.dataecho.info(sensor + ': ' + str(value / unit[1]) + ' ' + unit[2])

    def cb_delta(self, value, name, type, getter):
        try:
            delta = value - getter()
        except ip_connection.Error as e:
            self.log.error(e)
            return
        self.log.debug("DELTA of %s and %s is: %s (base was: %s)", name, getter, delta, value)
        self.cb_generic(delta, name, type)

    # exception logging
    def print_exception(self, inst):
        tree = ET.parse(os.path.join(settings.log, settings.exceptionlog))
        root = tree.getroot()
        new = ET.Element('exception', {'class': str(type(inst)).split("'")[1], 'date': str(time.ctime()),
                                       'time': str(int(time.time())), 'type': str(inst)})
        new.text = traceback.format_exc()
        root.append(new)
        tree.write(settings.exceptionlog)
        message = 'an Exception happend @' + time.ctime() + "\n"
        self.log.error(message)
        print(message)
