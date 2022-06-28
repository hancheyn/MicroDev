#!/bin/bash

cp Python/Integration/Bigfoot.py Python

# Setup Arduino
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

f=$(pwd)
export PATH=$PATH:$f/bin/
arduino-cli core install arduino:avr
arduino-cli board list


