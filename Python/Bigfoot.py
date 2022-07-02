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

# ******************************** Button Interrupts ************************************

# Globals for Buttons
B1_GPIO = 14
B2_GPIO = 15
B3_GPIO = 18
button_state = 0


# Button 1 Interrupt Handler
# Returns : Changes button state global
def b1_release(channel):
	# Extra Comment
	global button_state
	button_state |= 1
	print("B1 Pressed")


# Button 2 Interrupt Handler
# Returns : Changes button state global
def b2_release(channel):
	global button_state
	button_state |= 2
	print("B2 Pressed")


# Button 3 Interrupt Handler
# Returns : Changes button state global
def b3_release(channel):
	global button_state
	button_state |= 4
	print("B3 Pressed")


# Button 1 Interrupt Enable
# Returns : Changes button state global
def b1_enable():
	print("b1 enable")


# Button 1 Interrupt Disable
# Returns : Changes button state global
def b1_disable():
	print("b1 disable")


# Button 2 Interrupt Enable
# Returns : Changes button state global
def b2_enable():
	print("b2 enable")


# Button 2 Interrupt Disable
# Returns : Changes button state global
def b2_disable():
	print("b2 disable")


# Button 3 Interrupt Enable
# Returns : Changes button state global
def b3_enable():
	print("b3 enable")


# Button 3 Interrupt Disable
# Returns : Changes button state global
def b3_disable():

	print("b3 disable")


# Get Function for Buttons State
# Returns: State of Buttons
# (BIT0 = Button 1 | BIT1 = Button 2 |BIT2 = Button 3 )
def get_button_state():
	return 1


print("end of test")
