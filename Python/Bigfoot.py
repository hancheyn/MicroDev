# #################################################
# MicroDev Project: Bigfoot
# Date: May 2, 2022
# Description: Blank for Testing
# Authors:
# Nathan Hanchey
# Dylan
# Connor
# Corey
#
# References:
# raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2
# #################################################

import time
# import RPi.GPIO as GPIO
# import board
# import busio
# import adafruit_ina219

# import smbus

# set_mux_add
# Enable Mux  state = 1
# Disable Mux state = 0
# @parameter state
# @parameter enable
# @parameter add
def set_mux_add(state, enable, add):
	
	print("Mux Address Test")
	return 1


# I2C Communication
# Description:
# Accepts:
# Returns:
def rpi_i2c_config():

	print("config?")
	return 1


# Description:
# Accepts:
# Returns:
def rpi_i2c_adc():

	print("adc i2c test")
	return 1


# Description:
# Accepts:
# Returns:
def rpi_i2c_dac(val):

	print("dac i2c test")
	return 1


# Description:
# Accepts:
# Returns:
# REF: rototron.info/raspberry-pi-ina219-tutorial/
def rpi_i2c_ina219(i):
	print("ina219 test")


# High Current
# GPIO 17
# Enable: state = 1
# Disable: state = 0
def high_current(state):	

	print("high current test")
	return 1


# Low Current
# GPIO 27
# Enable: state = 1
# Disable: state = 0
def low_current(state):

	print("low current test")
	return 1
	
	
# DAC Enable
# GPIO 22
# Enable: state = 1
# Disable: state = 0
def dac_enable(state):

	print("dac test")
	return 1


# ADC with LOAD
# GPIO 10
# Enable: state = 1
# Disable: state = 0
def adc_load(state):

	print("adc load test")
	return 1


# ADC without LOAD
# GPIO 9
# Enable: state = 1
# Disable: state = 0
def adc_enable(state):

	print("adc enable test")
	return 1

print("end of test")
