#!/bin/bash

sudo apt-get update && apt-get upgrade

sudo apt-get remove --purge wolfram-engine triggerhappy anacron logrotate dphys-swapfile xserver-common lightdm

sudo systemctl disable x11-common

sudo apt-get autoremove --purge

sudo systemctl disable bootlogs
sudo systemctl disable console-setup

sudo apt-get install busybox-syslogd
sudo dpkg --purge rsyslog

# Disable Swap and filesystem check
# FIX: Change Line in /boot/cmdline.txt tofastboot noswap ro
echo "Manually Disable Swap"
read -p "Ready to Proceed? (press enter)" yn

# Move from /var to /tmp
sudo rm -rf /var/lib/dhcp /var/lib/dhcpcd5 /var/run /var/spool /var/lock /etc/resolv.conf
sudo ln -s /tmp /var/lib/dhcp
sudo ln -s /tmp /var/lib/dhcpcd5
sudo ln -s /tmp /var/run
sudo ln -s /tmp /var/spool
sudo ln -s /tmp /var/lock
sudo touch /tmp/dhcpcd.resolv.conf
sudo ln -s /tmp/dhcpcd.resolv.conf /etc/resolv.conf

# Move Lock Files
# FIX
echo "Manually Edit Lock File"
read -p "Ready to Proceed? (press enter)" yn

# Readonly Random Seed
sudo rm /var/lib/systemd/random-seed
sudo ln -s /tmp/random-seed /var/lib.systemd/random-seed

# Edit Service Config File
# FIX; 
echo "Manually Edit Service Configuration File"
read -p "Ready to Proceed? (press enter)" yn

sudo systemctl daemon-reload

# Make the file-system read-only
# FIX
echo "Manually Edit File System Configuration"
read -p "Ready to Proceed? (press enter)" yn

# RO to RW Switch
sudo cat set_bash >> /etc/bash.bashrc
sudo cat set_logout >> /etc/bash.bash_logout


echo "Restart Raspi when Ready"

