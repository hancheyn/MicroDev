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



GPIO.setwarnings(False)


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
	GPIO.setmode(GPIO.BCM)
	
	# Reset mux GPIO's to off state
	GPIO.setup(20, GPIO.OUT)
	GPIO.output(20, GPIO.LOW)
	
	GPIO.setup(16, GPIO.OUT)
	GPIO.output(16, GPIO.LOW)
	
	GPIO.setup(26, GPIO.OUT)
	GPIO.output(26, GPIO.LOW)
	
	GPIO.setup(13, GPIO.OUT)
	GPIO.output(13, GPIO.LOW)	
	
	GPIO.setup(19, GPIO.OUT)
	GPIO.output(19, GPIO.LOW)
	
	GPIO.setup(12, GPIO.OUT)
	GPIO.output(12, GPIO.LOW)
	
	GPIO.setup(5, GPIO.OUT)
	GPIO.output(5, GPIO.LOW)
	
	GPIO.setup(0, GPIO.OUT)
	GPIO.output(0, GPIO.LOW)

	GPIO.setup(1, GPIO.OUT)
	GPIO.output(1, GPIO.LOW)	
	
	GPIO.setup(7, GPIO.OUT)
	GPIO.output(7, GPIO.LOW)
	
	GPIO.setup(8, GPIO.OUT)
	GPIO.output(8, GPIO.LOW)
		
	# Conditional for state [on or off]
	if state==1:
		# convert add to binary
		# conditional for each add bit
		if (add & 1) == 1:
			GPIO.output(16, GPIO.HIGH)
			#print("bit0")
		if (add & 2) == 2:
			GPIO.output(26, GPIO.HIGH)
			#print("bit1")
		if (add & 4) == 4:
			GPIO.output(20, GPIO.HIGH)
			#print("bit2")
	
		# Conditional for enable
		if enable==1:
			GPIO.output(8, GPIO.HIGH)
		elif enable==2:
			GPIO.output(7, GPIO.HIGH)
		elif enable==3:
			GPIO.output(1, GPIO.HIGH)
		elif enable==4:
			GPIO.output(0, GPIO.HIGH)
		elif enable==5:
			GPIO.output(5, GPIO.HIGH)
		elif enable==6:
			GPIO.output(12, GPIO.HIGH)
		elif enable==7:
			GPIO.output(19, GPIO.HIGH)
		elif enable==8:
			GPIO.output(13, GPIO.HIGH)
			
	else:
		print("gpios off")
	

# I2C Communication Config
# Parameters: NA
# Returns: NA
def rpi_i2c_config():
	# GPIO reset
	print("")


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

	print("dac set")


# REF: rototron.info/raspberry-pi-ina219-tutorial/
# INA219 Capture
# Parameters: shunt type ( 0 = high current | 1 = low current )
# Returns: current value in amps
def rpi_i2c_ina219(shunt):
	print("")
	
	# print("ina219 current: " + str(current))
	return 1


# ******************************** Peripheral Enables ************************************

# High Current
# GPIO 17
# Enable: state = 1
# Disable: state = 0
def high_current(state):	
	print("")
	# print("high current test")


# Low Current
# GPIO 27
# Enable: state = 1
# Disable: state = 0
def low_current(state):	
	print("")


# DAC Enable
# GPIO 22
# Enable: state = 1
# Disable: state = 0
def dac_enable(state):
	
	print("")


# ADC with LOAD
# GPIO 10
# Enable: state = 1
# Disable: state = 0
def adc_load(state):
	
	print("")


# ADC without LOAD
# GPIO 9
# Enable: state = 1
# Disable: state = 0
def adc_enable(state):
	
	print("")


# ******************************** Button Interrupts ************************************
def signal_handler(sig, frame):
    print("")
    sys.exit(0)


# Globals for Buttons
B1_GPIO = 14
B2_GPIO = 15
B3_GPIO = 18
button_state = 0


# Button 1 Interrupt Handler
# Returns : Changes button state global
def b1_release(channel):
	# Extra Comment

	print("B1 Pressed")


# Button 2 Interrupt Handler
# Returns : Changes button state global
def b2_release(channel):

	print("B2 Pressed")


# Button 3 Interrupt Handler
# Returns : Changes button state global
def b3_release(channel):

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
	global button_state
	return button_state


print("End of Bigfoot Init")

