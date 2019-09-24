import RPi.GPIO as GPIO
import socket
import datetime
import time
import subprocess
import urllib2
from shutil import copyfile
from reader import getData
from reader import resetDweet
from buzzer import tune

#            Beeep-bip-bip	
tuneTime = [0.25, 0.1, 0.05, 0.1, 0.05, 0]

#          Long Beep-bip-bip
tuneTime1 = [0.5, 0.1, 0.1, 0.1, 0.1, 0]

tempFile2 = 'TemporaryFile2.txt'
file = open(tempFile2, "w")
file.close()

def timeStamp(stamp):
	log =  str(datetime.datetime.now()) + '  :  ' + str(stamp) + '\r\n'
	file = open(tempFile2, "a")
	file.write(log)
	file.close()
	copyfile (tempFile2, '/home/pi/eesh/garage.txt')
	print log
	

def listenDweet():
	dweet_url = 'https://dweet.io/get/latest/dweet/for/my-garage'
	reset_url = 'https://dweet.io/dweet/for/my-garage?reset=0'
	while 1:
		data = getData(dweet_url)
		#timeStamp(data)
		if data == '{"garage":"open"}':
			tune(tuneTime1)
			resetDweet(reset_url)
			#timeStamp("Tune for Garage Played")
		time.sleep(1)
	return

listenDweet()