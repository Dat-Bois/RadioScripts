import time
import RPi.GPIO as GPIO
import os 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

SHUTDOWN_PIN = 21

GPIO.setup(SHUTDOWN_PIN, GPIO.IN)

while 1:
	
	v = 0
	while GPIO.input(SHUTDOWN_PIN):
		time.sleep(0.1)
		v = v + 0.1
#		print (int(v))		
				
		if int(v) == 5:
			os.system ('sudo shutdown -h now')
			break 