import RPi.GPIO as GPIO
import time
import serial
import sys
import binascii
import os

TopLimit = 12.5
LowLimit = 2.5


iniciarCamara = 'sudo motion start'
dev = serial.Serial('/dev/ttyUSB0',baudrate=2400,timeout=5.0)
#dev = serial.Serial('/dev/ttyUSB0',baudrate=2400,bytesize='EIGHTBITS',parity='PARITY_NONE',stopbits='STOPBITS_ONE',timeout=6.0)
os.system(iniciarCamara)

def decToDutyCycle(numberDecimal):
	Duty = TopLimit-((numberDecimal/63.0)*2.5)
	Duty = round(Duty,2)
	if Duty<LowLimit:
		Duty = LowLimit
	if Duty>TopLimit:
		Duty = TopLimit
	return Duty

while True:
	a = bin(ord(dev.read()))
	dec = int(a,2)
	servo = decToDutyCycle(dec)
	print str(servo)+' - '+str(dec)
    
