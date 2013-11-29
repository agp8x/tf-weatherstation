#!/usr/bin/env python
# -*- coding: utf-8 -*-  

HOST = "localhost"
PORT = 4223
UID = "c8w" # Change to your UID

from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_temperature_ir import TemperatureIR
obj=0.0
amb=0.0
# Callback functions for object/ambient temperature callbacks 
# (parameters have unit °C/10)
def cb_object(temperature):
    amb=tir.get_ambient_temperature()/10.0
    obj=temperature/10.0
    print('Object Temperature: ' + str(temperature/10.0) + ' °C      '+str(obj-amb))
    print('Ambient Temperature: ' + str(amb) + ' °C      '+str(obj-amb))

def cb_ambient(temperature):
    amb=temperature/10.0
    obj=tir.get_object_temperature()/10.0
    print('Ambient Temperature: ' + str(temperature/10.0) + ' °C      '+str(obj-amb))

if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    tir = TemperatureIR(UID, ipcon) # Create device object

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    # Set Period for temperature callbacks to 1s (1000ms)
    # Note: The callbacks are only called every second if the 
    #       value has changed since the last call!
    tir.set_object_temperature_callback_period(1000)
    tir.set_ambient_temperature_callback_period(1000)

    # Register object temperature callback to function cb_object
    tir.register_callback(tir.CALLBACK_OBJECT_TEMPERATURE, cb_object)
    # Register ambient temperature callback to function cb_ambient
    #tir.register_callback(tir.CALLBACK_AMBIENT_TEMPERATURE, cb_ambient)

    raw_input('Press key to exit\n') # Use input() in Python 3
    ipcon.disconnect()