import RPi.GPIO as GPIO
import time
import serial
import sys
import binascii
import os

TopLimit = 11
LowLimit = 2.5

#RASPBERRY
GPIO.setmode(GPIO.BOARD)
GPIO.setup(23,GPIO.OUT)
inicio = time.time()
p = GPIO.PWM(23,50)
p.start(7.5)

#FILTRADO
buffer = []
i = 0
const = 30
contador = 0
porcion = 30
valores = []
flag = 0
newValue = 0
oldValue = 0
#42 por que son 6 segmentos entre 0 y 252 (252/6)
rango = 36
area = 0

#INICIO DE CAMARA
iniciarCamara = 'sudo motion start'
dev = serial.Serial('/dev/ttyUSB0',baudrate=2400,timeout=5.0)
#os.system(iniciarCamara)
fin = time.time()
tiempo = fin-inicio

def guardar(archivo,info):
	f = open(archivo+'.txt','a')
	f.write(str(info)+'\n')
	f.close()
def calibrar(numero):
	return (((numero+1)*rango)/2)


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
	#p.ChangeDutyCycle(servo)
	if dec is not 255:
		buffer.append(dec)
		if len(buffer) is const:
			#print buffer
			#Valor de retorno del filtro
			valor = (sum(buffer)/len(buffer))
			#print valor
			buffer.remove(buffer[0])
			contador = contador +1
			if contador is porcion:
				print 'Este es el valor  '+str(valor)
				guardar('data',valor)
				valores.append(valor)
				oldValue = newValue
				newValue = int(valor/rango)
				print str(oldValue)+ ' - '+str(newValue)
				if (newValue is not oldValue):
					#motor = calibrar(newValue)
					servo = decToDutyCycle(valores.pop())
					#servo = decToDutyCycle(motor)
					p.ChangeDutyCycle(servo)
					print 'Me cambio'
					print str(valor)+'-'+str(servo)
				else:
					print 'No me cambio'
				contador = 0
				
				#time.sleep(0.8)	
		#time.sleep(1)
		#p.ChangeDutyCycle(servo)
		#print str(servo)+' - '+str(dec)
