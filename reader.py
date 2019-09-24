import time
import os 
import urllib2
from shutil import copyfile


def getData(dweet_url):
#Downloads data from Dweet

	try:
		response = urllib2.urlopen(dweet_url)
		html = response.read()
		st = html.find("{", 100)
		html2 = html[st:200]
		en = html2.find("}")
		en = en + 1
		html3 = html2[0:en]
		#print(html3)
		return html3
	
	
	except :
		print("read failed")

	return "no data"

def resetDweet(reset_url):
	#Resets dweet data to "reset=0"
	try:
		urllib2.urlopen(reset_url)
	
	except:
		print("Reset Failed")
	
	return

