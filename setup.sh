#!/bin/bash

cp Python/Integration/Bigfoot.py Python

# ########################################################################################
# Setup Arduino
# The instructions below initialize the Arduino Command Line Interface.
# These instructions are required for testing the Arduino Uno Development Board on
# the MicroDev device.
# ########################################################################################

# Uncomment below to install latest arduino-cli
#curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh
f=$(pwd)
export PATH=$PATH:$f/bin/
sudo cp $f/bin/arduino-cli /bin
arduino-cli core install arduino:avr
arduino-cli board list

# ########################################################################################
# Setup the I2C / Bigfoot Libraries
# The instructions below initialize the I2C communication to the required sensors.
# These instructions are required for all testing on the MicroDev device.
# The ADC, Current Sensor, and DAC are controlled through these libraries.
# ########################################################################################
sudo pip3 install smbus
sudo pip3 install board
sudo pip3 install adafruit-circuitpython-ina219


# ########################################################################################
# BOOT UP to GUI
# The instructions below initialize the autostart functions for the GUI
# on the Raspberry Pi.
# ########################################################################################
sudo mkdir /home/microdev/.config/autostart/
sudo cp MyApp.desktop1 /home/microdev/.config/autostart/MyApp.desktop
# cd /home/microdev/.config/autostart/
sudo chmod +x /home/microdev/.config/autostart/MyApp.desktop