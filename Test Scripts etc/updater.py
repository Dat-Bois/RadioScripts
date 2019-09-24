import time
import os 
import urllib2
from shutil import copyfile


def UpdatePythonScript():
#Downloads script from internet and if scuccessful,  replaces current script with downloaded version

	tempFile = 'DownloadedContent.html'
	try:
		response = urllib2.urlopen('http://www.rohitleena.com/radio2/radio.py')
		html = response.read()
		html2 = html[0:100]
	
		
		file = open('/home/pi/eesh/radio.py', "r")
		firstLineofRadio = file.read()
		file.close();
		firstLineofRadio = firstLineofRadio[0:100]


		if firstLineofRadio == html2 :
			print(firstLineofRadio)
			print("----------------------------------------------------")
			print(html2)
			print("update not required")
		else:
			file = open(tempFile, "w")
			file.write(html)
			file.close();
			copyfile (tempFile, '/home/pi/eesh/radio.py')
			print("!!!!!! update completed!!!!!")
			print('Previous : '+ firstLineofRadio)
			print('Current  : '+ html2)
			os.system('sudo reboot')
	except :
		print("update failed")

	return

# Letting song run	
time.sleep(5)

# Running function to overwrite old script and update with new one
UpdatePythonScript()