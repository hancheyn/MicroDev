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

import time
import RPi.GPIO as GPIO
import board
import busio
import adafruit_ina219

import smbus

bus = smbus.SMBus(1)

# BASIC EXAMPLES
GPIO.setwarnings(False)


# GPIO.setmode(GPIO.BCM)
# GPIO.setup(4, GPIO.OUT)
# GPIO.setup(22,GPIO.IN)
# GPIO.output(4,GPIO.input(22))

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

    # conditional for state [on or off]
    if state == 1:
        # convert add to binary
        # conditional for each add bit
        if (add & 1) == 1:
            GPIO.output(20, GPIO.HIGH)
            print("bit0")
        if (add & 2) == 2:
            GPIO.output(16, GPIO.HIGH)
            print("bit1")
        if (add & 4) == 4:
            GPIO.output(26, GPIO.HIGH)
            print("bit2")

        # conditional for enable
        if enable == 1:
            GPIO.output(13, GPIO.HIGH)
        elif enable == 2:
            GPIO.output(19, GPIO.HIGH)
        elif enable == 3:
            GPIO.output(12, GPIO.HIGH)
        elif enable == 4:
            GPIO.output(5, GPIO.HIGH)
        elif enable == 5:
            GPIO.output(0, GPIO.HIGH)
        elif enable == 6:
            GPIO.output(1, GPIO.HIGH)
        elif enable == 7:
            GPIO.output(7, GPIO.HIGH)
        elif enable == 8:
            GPIO.output(8, GPIO.HIGH)

    else:
        print("off")


# I2C Communication
def rpi_i2c_config():
    # ADC set

    # DAC set

    # Current Set
    print("test")


def rpi_i2c_adc():
    # 0xD0 ADDRESS
    # Read 1st byte
    # read second byte with read_i2c block data
    read_block = bus.read_i2c_block_data(0xD0, 0x00)
    read_byte = bus.read_byte(0xD0)

    # combine first and second byte
    read = int(read_byte) + (int(read_block[1]) << 8)

    # Convert into Voltage

    print(read_byte)
    print("adc")


def rpi_i2c_dac(val):
    # 0x46 ADDRESS

    write = bus.write_word_data(0x46, val)

    print(read)
    print("dac")


# REF: rototron.info/raspberry-pi-ina219-tutorial/
def rpi_i2c_ina219(shunt):
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_ina219.INA219(i2c)

    print("Bus Voltage: {} V".format(sensor.bus_voltage))
    print("Shunt Voltage: {} mV".format(sensor.shunt_voltage / 1000))
    print("Current: {} mA".format(sensor.current))

    # Conditional for high or low current shunt

    print("ina219")


# High Current
# GPIO 17
# Enable: state = 1
# Disable: state = 0
def high_current(state):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)

    if state == 1:
        GPIO.output(17, GPIO.HIGH)
    else:
        GPIO.output(17, GPIO.LOW)

    print("high current test")


# Low Current
# GPIO 27
# Enable: state = 1
# Disable: state = 0
def low_current(state):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(27, GPIO.OUT)
    GPIO.output(27, GPIO.LOW)

    if state == 1:
        GPIO.output(27, GPIO.HIGH)
    else:
        GPIO.output(27, GPIO.LOW)


# DAC Enable
# GPIO 22
# Enable: state = 1
# Disable: state = 0
def dac_enable(state):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(22, GPIO.OUT)

    if state == 1:
        GPIO.output(22, GPIO.HIGH)
    else:
        GPIO.output(22, GPIO.LOW)


# ADC with LOAD
# GPIO 10
# Enable: state = 1
# Disable: state = 0
def adc_load(state):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(10, GPIO.OUT)

    if state == 1:
        GPIO.output(10, GPIO.HIGH)
    else:
        GPIO.output(10, GPIO.LOW)


# ADC without LOAD
# GPIO 9
# Enable: state = 1
# Disable: state = 0
def adc_enable(state):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(9, GPIO.OUT)

    if state == 1:
        GPIO.output(9, GPIO.HIGH)
    else:
        GPIO.output(9, GPIO.LOW)


# TESTS
# set_mux_add(0, 1, 7)
# low_current(0)
# high_current(0)
# adc_enable(0)
# adc_load(0)
# dac_enable(0)

# rpi_i2c_ina219()
# rpi_i2c_adc()

print("end of test")