script_version = "Script Version 2.2" 
script_date    = "Script Date : 1-5-2019"  

import os
print("Hello There!")
print(script_version)
print(script_date)

import pickle
import socket
import datetime
import time
import RPi.GPIO as GPIO
import subprocess
import urllib2
from shutil import copyfile
from threading import Thread
from reader import getData
from reader import resetDweet
from buzzer import tune
import ChannelsCC


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#wait for MPD to come up
time.sleep(10)


Segments = "111111000", "011000000", "110110100", "111100100", "011001100", "101101100", "101111100", "111000000", "111111100", "111101100", \
"111111011", "011000011", "110110111", "111100111", "011001111", "101101111", "101111111", "111000011", "111111111", "111101111", "000000000" 

tuneTime = [0.2, 0]


#GPIO "B2" and "C2" are the number one for two digit numbers on the second seven digit display
GPIO_A = 15
GPIO_B = 18
GPIO_C = 4 
GPIO_D = 17
GPIO_E = 27
GPIO_F = 22
GPIO_G = 14
GPIO_B2 = 8
GPIO_C2 = 7

#12
CHANNEL_UP_PIN = 12
CHANNEL_DOWN_PIN = 10
SHUTDOWN_PIN = 5 #21
LED_PIN = 16 
ARDUINO_PIN = 6 #26
BUZZER_PIN = 9 

ENABLE_WATCH_DOG = 0

GPIO.setup(GPIO_A, GPIO.OUT)
GPIO.setup(GPIO_B, GPIO.OUT)
GPIO.setup(GPIO_C, GPIO.OUT)
GPIO.setup(GPIO_D, GPIO.OUT)
GPIO.setup(GPIO_E, GPIO.OUT)
GPIO.setup(GPIO_F, GPIO.OUT)
GPIO.setup(GPIO_G, GPIO.OUT)
GPIO.setup(GPIO_B2, GPIO.OUT)
GPIO.setup(GPIO_C2, GPIO.OUT)

#GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(CHANNEL_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(CHANNEL_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ARDUINO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(SHUTDOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED_PIN,GPIO.OUT)
GPIO.setup(BUZZER_PIN,GPIO.OUT)

GPIOs = GPIO_A, GPIO_B, GPIO_C, GPIO_D, GPIO_E, GPIO_F, GPIO_G, GPIO_B2, GPIO_C2

#current playing channel (global variable)
c = 1
#Number of Channels
nMaxChannel = 12
#pause or not 
global nPause
nPause = 0
#Delay time for watchdog
global z
z = 0
"""def test():
	a = 0
	while(a <= 9):
		playChannel(a)
		time.sleep(3)
		a = a + 1
	return
"""

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
	GPIO.output(BUZZER_PIN,GPIO.HIGH)
	#timeStamp("Shutdown")
	time.sleep(1)
	os.system ('sudo shutdown -h now')

#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def channelUp():
	global z
	global c 
	global nMaxChannel
	global nPause
	if nPause == 0:
		c = c + 1 
		if c >= nMaxChannel + 1:
			c = 1
		playChannel(c)
		#timeStamp("Channel Up " + str(c))
		time.sleep(0.1)
		z = -3
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
		#timeStamp("Channel Down " + str(c))
		time.sleep(0.1)
		z = -3
	return

#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def playChannel(b):
	#set it to global channel
	global c 
	c = b 
	tune(tuneTime)
	print ('channel changed to :' + str(b))
	print ('mpc play '+str(b))
	displayChannel(Segments[b])
	os.system('mpc play '+str(b))
	if CheckStatus("#"+str(b)) == 0:
		time.sleep(0.1)
		os.system('mpc play '+str(b))
	if b == 2:
		os.system('mpc volume 90')
	else:
		os.system('mpc volume 100')
	transmit(b)
	return

#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def displayChannel(nCh):
	n = 0
	while(n < 9):
		GPIO.output(GPIOs[n],int(nCh[n]))
		n = n + 1
	return

#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def play():
	global nPause 
	nPause = 1
	pausePlay()
	return
#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def pause():
	global nPause 
	nPause = 0
	pausePlay()
	return
#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def pausePlay():
	global z
	global c
	global nPause 
	global pauseTime
	if nPause == 0:
		pauseTime = time.time()
		displayChannel(Segments[20])
		os.system ('mpc stop')
		os.system ('mpc volume 100')
		#disable watchdog
		nPause = 1 
		transmit("stop")
	else:
#		os.system ('sudo systemctl restart mpd')
		os.system ('mpc play')
		os.system ('mpc volume 100')
		displayChannel(Segments[c]) 
		#enable watchdog
		nPause = 0
		transmit("play")
		#Giving longer delay time to watchdog
		z = -3
	return 
#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def timeStamp(stamp):
	log =  str(datetime.datetime.now()) + '  :  ' + str(stamp) + '\r\n'
	file = open(tempFile, "a")
	file.write(log)
	file.close()
	copyfile (tempFile, '/home/pi/eesh/N_reboots.txt')
#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def timeStamp1(stamp):
	log =  str(datetime.datetime.now()) + '  :  ' + str(stamp) + '\r\n'
	file = open(tempFile1, "a")
	file.write(log)
	file.close()
	copyfile (tempFile1, '/home/pi/eesh/data.txt')
	print log
#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def listenDweet():
	
	dweet_url = 'https://dweet.io/get/latest/dweet/for/my-radio'
	reset_url = 'https://dweet.io/dweet/for/my-radio?reset=0'
	
	while 1:
	
		data = getData(dweet_url)
		
		if data == '{"ch":"up"}':
			channelUp()
			resetDweet(reset_url)
						
		if data == '{"ch":"down"}':
			channelDown()
			resetDweet(reset_url)		

		if data == '{"ch":1}':
			playChannel(1)
			resetDweet(reset_url)
			
		if data == '{"ch":5}':
			playChannel(5)
			resetDweet(reset_url)
			
		if data == '{"ch":10}':
			playChannel(10)
			resetDweet(reset_url)
			
		if data == '{"ch":"stop"}':
			pause()
			transmit("stop")
			resetDweet(reset_url)
			
		if data == '{"ch":"play"}':
			play()
			transmit("play")
			resetDweet(reset_url)
			
		if data == '{"ch":"reconnect"}':
			play()
			transmit("reconnect")
			resetDweet(reset_url)
			
		if data == '{"ch":2}':
			playChannel(2)
			resetDweet(reset_url)
			
		if data == '{"ch":3}':
			playChannel(3)
			resetDweet(reset_url)
			
		if data == '{"ch":4}':
			playChannel(4)
			resetDweet(reset_url)
			
		if data == '{"ch":6}':
			playChannel(6)
			resetDweet(reset_url)
			
		if data == '{"ch":7}':
			playChannel(7)
			resetDweet(reset_url)
			
		if data == '{"ch":8}':
			playChannel(8)
			resetDweet(reset_url)
			
		if data == '{"ch":9}':
			playChannel(9)
			resetDweet(reset_url)
			
		if data == '{"ch":11}':
			playChannel(11)
			resetDweet(reset_url)
			
		if data == '{"ch":12}':
			playChannel(12)
			resetDweet(reset_url)
		
		#timeStamp1(data)
		time.sleep(1)
#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------	
#
#--------------------------------------------------------------------------------------------
def transmit(channel):
	
	HOST = '192.168.1.100'
	PORT = 12345
	# Create a socket connection.
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	channel = str(channel)
	
	if channel == "stop":
		variable = ChannelsCC.statusList[1]
	
	elif channel == "play":
		variable = ChannelsCC.statusList[0]
		
	elif channel == "reconnect":
		variable = ChannelsCC.statusList[2]
	
	else:
		channel = int(channel)
		# Create an instance of ProcessData() to send to server.
		variable = ChannelsCC.channelList[channel]
		
	# Pickle the object and send it to the server
	data_string = pickle.dumps(variable)
	s.send(data_string)

	s.close()
	print 'Data Sent to Server'

	return
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

for i in range(1,len(ChannelsCC.channelList)):
	os.system ('mpc add '+ ChannelsCC.channelList[i].getUrl())
	
#-----------------------------------------------------------


os.system ('mpc repeat on')
os.system ('mpc pause')
os.system ('mpc volume 100')
playChannel(1)

thread = Thread(target = listenDweet)
thread.start()

print("LED on")
GPIO.output(LED_PIN,GPIO.HIGH)
#GPIO.setup(18, GPIO.OUT)
#GPIO.output(18, False)
tempFile = 'TemporaryFile.txt'
file = open(tempFile, "w")
file.close()
tempFile1 = 'TemporaryFile1.txt'
file = open(tempFile1, "w")
file.close()
z = 0
x = 0
nReboots = 0
timeStamp("Script Started")
print(datetime.datetime.now())
# The amount of time each duration of whether blank or on 7 segments.
global pauseTime
pauseTime = 0
# This variable tells whether or not the seven segment is blank 
channelBlank = 0
#----------------------------------------------------------------

while 1:
	time.sleep(0.001)

	if nPause == 1:
		global pauseTime
		# = time.time()
		if time.time() - pauseTime >= 1:
			if channelBlank == 1:	
				displayChannel(Segments[20])
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
	if nPause == 0:
	
		if GPIO.input(ARDUINO_PIN):
			#print ("audio")
			z = 0
			
			
		if not GPIO.input(ARDUINO_PIN):
			z = z + 0.1
			time.sleep(0.1)
			#print ("no audio")
			
			#Watch dog
			if z > 2 and ENABLE_WATCH_DOG == 1:
				print ("-----------------------Pause Play-------------------" + str(nReboots))
				print(datetime.datetime.now())	
				os.system('mpc stop')
				os.system('mpc play')
				z = 0
				
				strReboot = "Pause Play " + str(nReboots)
				#timeStamp(strReboot)
				
				nReboots = nReboots + 1
				
				if nReboots == 500:
					os.system ('sudo systemctl restart mpd')
					nReboots = 0
				