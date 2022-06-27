#!/bin/bash

cp Python/Integration/Bigfoot.py Python

# Setup Arduino
curl -fsSL https://raw.githubusercontent.com/arduino/arduino-cli/master/install.sh | sh

f=$(pwd)
$PATH=$PATH:$f/arduino-cli
arduino-cli core install arduino:avr
arduino-cli board list


