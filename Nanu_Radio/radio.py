script_version = "Script Version 8 FINAL Nanu" 
script_date    = "Script Date : 11-25-2017"  

import os
print("Hello There!")
print(script_version)
print(script_date)

from threading import Thread
import urllib
import re
import datetime
import time
import RPi.GPIO as GPIO
import subprocess

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#wait for MPD to come up
time.sleep(10)


Segments = "1111110", "0110000", "1101101", "1111001", "0110011", "1011011", "1011111", "1110000", "1111111", "1111011", "0000000"

GPIO_A = 15
GPIO_B = 18
GPIO_C = 4 
GPIO_D = 17
GPIO_E = 27
GPIO_F = 22
GPIO_G = 14

#12
CHANNEL_UP_PIN = 12
CHANNEL_DOWN_PIN = 10
SHUTDOWN_PIN = 5 #21
LED_PIN = 16 
ARDUINO_PIN = 6 #26

GPIO.setup(GPIO_A, GPIO.OUT)
GPIO.setup(GPIO_B, GPIO.OUT)
GPIO.setup(GPIO_C, GPIO.OUT)
GPIO.setup(GPIO_D, GPIO.OUT)
GPIO.setup(GPIO_E, GPIO.OUT)
GPIO.setup(GPIO_F, GPIO.OUT)
GPIO.setup(GPIO_G, GPIO.OUT)

GPIO.setup(CHANNEL_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(CHANNEL_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ARDUINO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SHUTDOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED_PIN,GPIO.OUT)

GPIOs = GPIO_A, GPIO_B, GPIO_C, GPIO_D, GPIO_E, GPIO_F, GPIO_G

#current playing channel (global variable)
c = 1
#Number of Channels
nMaxChannel = 9
#pause or not (1 means watchdog on, 0 means watchdog off)
global nPause
nPause = 0

#--------------------------------------------------------------------------------------------
# sends command (strCmd) and strCheck outout for string(strCheck). If 'strCheck' is present, function returns 1 otherwise 0.
#--------------------------------------------------------------------------------------------
def CheckStatus(strCheck):
	strCmd = "mpc status"
	proc = subprocess.Popen([strCmd], stdout=subprocess.PIPE, shell=True)
	(MPC_out, err) = proc.communicate()
	
	if strCheck in MPC_out: 
		return 1
	else:
		return 0
	return
	
	
#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def shutDown():
	os.system ('mpc clear')  
	os.system ('mpc add SDCARD/shutdown')
	os.system ('mpc repeat off')
	os.system ('mpc play')
	time.sleep(3) 
	os.system ('mpc clear')
	os.system ('sudo shutdown -h now')

#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def channelUp():
	global c 
	global nMaxChannel
	global nPause
	if nPause == 0:
		c = c + 1 
		if c >= nMaxChannel + 1:
			c = 1
		playChannel(c)
	return

#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def channelDown():
	global c
	global nMaxChannel
	global nPause
	if nPause == 0:
		c = c - 1
		if c <= 0:
			c = nMaxChannel
		playChannel(c)
	return

#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def playChannel(b):
	print ('channel changed to :' + str(b))
	print ('mpc play '+str(b))
	displayChannel(Segments[b])
	os.system('mpc play '+str(b))
	if CheckStatus("#"+str(b)) == 0:
		time.sleep(0.1)
		os.system('mpc play '+str(b))
	return

#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def displayChannel(nCh):
	n = 0
	while(n < 7):
		GPIO.output(GPIOs[n],int(nCh[n]))
		n = n + 1
	return

#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def pausePlay():
	global c
	global nPause 
	global pauseTime
	if nPause == 0:
		pauseTime = time.time()
		displayChannel(Segments[10])
		os.system ('mpc stop')
		#disable watchdog
		nPause = 1 
	else:
		os.system ('sudo systemctl restart mpd')
		os.system ('mpc play')
		displayChannel(Segments[c])
		nPause = 0 
		#enable watchdog
	return 
#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def NewsChannelUpdater():

 #-----------------Sets Morning, Noon, and Night----------------------
	morning = 0000
	noon = 1159
	nightime = 1930
	midnight = 2359
 #---------------------FINDS LINK--------------------------------------
	
	print("Finding Link")
	fbhandle = urllib.urlopen('http://www.newsonair.com/')
	pattern = "(/writereaddata/broadcast/Hindi-Main-Bulletins-......mp3)" 
	m = re.findall(pattern , fbhandle.read())
	fbhandle.close()
	newsURL = m
	
 #--------------------FINDS TIME--------------------------------------
	
	print("Finding Time")
	currentTM = str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute)
	currentTM = int(currentTM)
	time = currentTM
	
 #----------FINDS COMPLETE LINK ACCORDING TO TIME---------------------
	
	print("Finding Complete Link According To Time")
	m = newsURL
	URL =  ("http://www.newsonair.com"  + m[3]) #hourly
	if time >= morning and time <= noon: #For Morning
		URL = ("http://www.newsonair.com"  + m[0]) #Morning
	if time >= noon and time <= nightime: #For Noon
		URL = ("http://www.newsonair.com"  + m[1]) #Noon
	if time >= nightime and time <= midnight: #For Nightime
		URL = ("http://www.newsonair.com"  + m[2]) #Nightime

 #------------REPLACES CHANNEL WITH NEW LINK--------------------------
	print (time)
	print (URL)
	os.system ('mpc del 9')
	os.system ('mpc add ' + str(URL))
	
	print("Finalized and put URL into Moode")	
	return
#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def threadTimer():

	while 1:
	
		thread = Thread(target = NewsChannelUpdater)
		thread.start()
		time.sleep(60*60)
	
	return 
#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
#                                   END OF FUNCTIONS
#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
os.system ('clear')
os.system ('mpc clear')

#---- play startup message -------------------------------------
#os.system ('mpc add http://www.rohitleena.com/rohitleena/song.mp3')
os.system ('mpc add SDCARD/start')
os.system ('mpc play')
time.sleep(3) 
os.system ('mpc clear')
#---------------------------------------------------------
#---- Adding radio stations ------------------------------
#1 Suno FM - Dubai
os.system ('mpc add http://50.7.71.27:9693/')

#2 Sabras Radio - UK
os.system ('mpc add http://radio.canstream.co.uk:8025/live.mp3')

#3 HUM FM - Dubai 
os.system ('mpc add  http://icy1.abacast.com:80/humfm-humfmmp3-64')

#4 Hindi Desi Bollywood Evergreen Hits
os.system ('mpc add http://50.7.77.114:8296')

#5 Hindi SADA BHAR  Hits
os.system ('mpc add http://192.240.102.133:8512/stream')

#6 DesiMusicMix - hindi and punjabi
os.system ('mpc add http://66.23.234.242:8012/')

#7 Dhol Radio - Unknown 
os.system ('mpc add http://5.9.86.167:8000/')

#8 NDTV - hindi - New Delhi
os.system ('mpc add http://stream1.ndtv.com:8080/on-ndtvindia')

#9 AIR news - hindi - India 
os.system ('mpc add http://stream1.ndtv.com:8080/on-ndtvindia')
#-----------------------------------------------------------
thread = Thread(target = threadTimer)
thread.start()
os.system ('mpc repeat on')
os.system ('mpc pause')
os.system ('mpc volume 100')
playChannel(1)


print("LED on")
GPIO.output(LED_PIN,GPIO.HIGH)
#GPIO.setup(18, GPIO.OUT)
#GPIO.output(18, False)
z = 0
x = 0
nReboots = 1
print(datetime.datetime.now())
# The amount of time each duration of whether blank or on 7 segments.
global pauseTime
pauseTime = 0
# This variable tells whether or not the seven segment is blank 
channelBlank = 0
#----------------------------------------------------------------

while 1:

	if nPause == 1:
		global pauseTime
		# = time.time()
		if time.time() - pauseTime >= 1:
			if channelBlank == 1:	
				displayChannel(Segments[10])
				channelBlank = 0
				pauseTime = time.time()
			else:
				global c 
				displayChannel(Segments[c])
				channelBlank = 1
				pauseTime = time.time()
				
	v = 0
	
	while GPIO.input(SHUTDOWN_PIN):
		time.sleep(0.1)
		v = v + 0.1
#		print (int(v))		
				
		if int(v) == 2:
			shutDown()
			break 
	
	if v < 2 and v > 0.1:
		pausePlay()
	
	p = 0
	while GPIO.input(CHANNEL_UP_PIN):
		time.sleep(0.1)
		p = p + 0.1
#		print (int(p))
		
		if p < 2 and p > 0.1:
			channelUp()
			break

	j = 0
	while GPIO.input(CHANNEL_DOWN_PIN):
		time.sleep(0.1)
		j = j + 0.1
#		print (int(j))
		
		if j < 2 and j > 0.1:
			channelDown()
			break 
	
	#print(" x = "+ str(x))

	global nPause 
	if nPause == 1:
	
		if GPIO.input(ARDUINO_PIN):
			#print ("audio")
			z = 0
			
			
		if not GPIO.input(ARDUINO_PIN):
			z = z + 0.1
			time.sleep(0.1)
			#print ("no audio")
			
			#Watch dog
			if z > 3:
				print ("-----------------------Pause Play-------------------" + str(nReboots))
				print(datetime.datetime.now())	
				os.system('mpc stop')
				os.system('mpc play')
				z = 0
				nReboots = nReboots + 1
	
	
	
	