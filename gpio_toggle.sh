#!/bin/bash

regex='^[0-9]+$'
i=0
spin='-\|/'

gpioPin=$1 

trap ctrl_c INT

function ctrl_c()
{
    echo "** Trapped CTRL-C"
    echo "unexporting GPIO $gpioPin"
    echo $gpioPin > /sys/class/gpio/unexport
    exit 0
}

if ! [[ $gpioPin =~ $regex ]] ; then
    echo "error: need a GPIO number"
    exit 1
fi

# Check if gpio is already exported
if [ ! -d /sys/class/gpio/gpio$gpioPin ]
then
  echo $gpioPin > /sys/class/gpio/export
  sleep 1 ;# Short delay while GPIO permissions are set up
fi

# Set to output
echo out > /sys/class/gpio/gpio$gpioPin/direction

while true; do
    echo 1 >  /sys/class/gpio/gpio$gpioPin/value
#    i=$(( (i+1) %4 ))
#    printf "\r${spin:$i:1}"
    echo 0 >  /sys/class/gpio/gpio$gpioPin/value
done
