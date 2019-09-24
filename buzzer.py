import RPi.GPIO as GPIO
import datetime
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PIEZO_PIN = 26

GPIO.setup(PIEZO_PIN,GPIO.OUT)

#            Beeep-bip-bip	
tuneTime = [0.25, 0.1, 0.05, 0.1, 0.05, 0]

#          Long Beep-bip-bip
tuneTime1 = [0.5, 0.1, 0.1, 0.1, 0.1, 0]
	
def buzz(delay):
	GPIO.output(PIEZO_PIN,GPIO.HIGH)
	time.sleep(delay)
	GPIO.output(PIEZO_PIN,GPIO.LOW)
	return
	
def wait(t):
	time.sleep(t)
	return
	
def tune(tuneTime):	
	counter = 0
	numTuneTime = len(tuneTime)
	while counter < numTuneTime:
		buzz(tuneTime[counter])
		counter = counter + 1
		wait(tuneTime[counter])
		counter = counter + 1
	return
