# #################################################
# MicroDev Project: Bigfoot
# Date: May 2, 2022
# Description: Handles GPIO's
# Authors:
# Nathan Hanchey
# Dylan
# Connor
# Corey
#
# References:
# raspberry-projects.com/pi/programming-in-python/i2c-programming-in-python/using-the-i2c-interface-2
# #################################################

import sys
import signal
import time
import RPi.GPIO as GPIO


#import smbus

#bus = smbus.SMBus(1)
#GPIO.setwarnings(False)


# ********************************** SET BIGFOOT ADC *****************************************
# Description: SET ADC value
# Accepts: Voltage for DAC Output
# Returns: NA
VOUT = 3.3


def set_vout(vout):
    global VOUT
    VOUT = vout


# ******************************** Set for Subject Board Mux  ************************************
# set_mux_add
# Enable Mux  state = 1
# Disable Mux state = 0
# @parameter state
# @parameter enable
# @parameter add
def set_mux_add(state, enable, add):
	print("gpios off")
	

# I2C Communication Config
# Parameters: NA
# Returns: NA
def rpi_i2c_config():
	# GPIO reset
	set_mux_add(0, 1, 7)
	
	# ADC reset
	adc_enable(0)
	adc_load(0)
	#bus.write_byte(0x48, 0x1c)
	
	# DAC reset
	dac_enable(0)
	#rpi_i2c_dac(0x00)
	
	# Current Set
	#GPIO.setwarnings(False)
	low_current(0)
	high_current(0)
	# rpi_i2c_ina219(0)
	print("i2c config complete")


# ADC Capture
# Parameters: NA
# Returns: adc value (volts)
def rpi_i2c_adc():

	return 0


# DAC Set
# Parameters: DAC value to set (4 bit value)
# Returns: NA
def rpi_i2c_dac():
	# 0x0D ADDRESS
	global VOUT

	print("dac set")


# REF: rototron.info/raspberry-pi-ina219-tutorial/
# INA219 Capture
# Parameters: shunt type ( 0 = high current | 1 = low current )
# Returns: current value in amps
def rpi_i2c_ina219(shunt):
	

	
	#print("ina219 current: " + str(current))
	return 0


# ******************************** Peripheral Enables ************************************

# High Current
# GPIO 17
# Enable: state = 1
# Disable: state = 0
def high_current(state):	
	print("high current test")


# Low Current
# GPIO 27
# Enable: state = 1
# Disable: state = 0
def low_current(state):	
	print("low current")


# DAC Enable
# GPIO 22
# Enable: state = 1
# Disable: state = 0
def dac_enable(state):
	
	print("dac")


# ADC with LOAD
# GPIO 10
# Enable: state = 1
# Disable: state = 0
def adc_load(state):
	
	print("load")


# ADC without LOAD
# GPIO 9
# Enable: state = 1
# Disable: state = 0
def adc_enable(state):
	
	print("adc")


# ******************************** Button Interrupts ************************************
def signal_handler(sig, frame):
	print("handler")


# Globals for Buttons
B1_GPIO = 14
B2_GPIO = 15
B3_GPIO = 18
button_state = 0


# Button 1 Interrupt Handler
# Returns : Changes button state global
def b1_release(channel):
	# Extra Comment
	global button_state, B1_GPIO

	print("B1 Pressed")


# Button 2 Interrupt Handler
# Returns : Changes button state global
def b2_release(channel):

	print("B2 Pressed")


# Button 3 Interrupt Handler
# Returns : Changes button state global
def b3_release(channel):
	global button_state, B3_GPIO

	print("B3 Pressed")


# Button 1 Interrupt Enable
# Returns : Changes button state global
def b1_enable():
	global B1_GPIO

	print("b1 enable")


# Button 1 Interrupt Disable
# Returns : Changes button state global
def b1_disable():
	global button_state

	print("b1 disable")


# Button 2 Interrupt Enable
# Returns : Changes button state global
def b2_enable():
	global B2_GPIO

	print("b2 enable")


# Button 2 Interrupt Disable
# Returns : Changes button state global
def b2_disable():
	global button_state

	print("b2 disable")


# Button 3 Interrupt Enable
# Returns : Changes button state global
def b3_enable():

	print("b3 enable")


# Button 3 Interrupt Disable
# Returns : Changes button state global
def b3_disable():
	global button_state

	print("b3 disable")


# Get Function for Buttons State
# Returns: State of Buttons
# (BIT0 = Button 1 | BIT1 = Button 2 |BIT2 = Button 3 )
def get_button_state():
	global button_state
	return button_state


print("End of Bigfoot Init")

