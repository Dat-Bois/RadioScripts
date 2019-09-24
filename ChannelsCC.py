import time

class channel:
	
	#-----------------------------------------------
	def __init__(self, name, url, volume, type):
		self.name = name
		self.url = url
		self.volume = volume
		self.type = type
	
	def getUrl(self):
		return self.url
	
	def getName(self):
		return self.name
	
	def getVolume(self):
		return self.volume
		
	def getType(self):
		return self.type
		
	def pausePlay(self):
		return self.name
#--------------------------------------------------------------------------------------------------
def setVolume(channelNum, newVolume):
	channelList[channelNum].volume = newVolume

statusList = []

statusList.append(channel(
"play",
"No Link", 0, "N/A"))

statusList.append(channel(
"pause",
"No Link", 0, "N/A"))

statusList.append(channel(
"reconnect",
"No Link", 0, "N/A"))

	


channelList = []

channelList.append(channel(
"PLACE HOLDER",
"No Link", 0, "N/A"))

channelList.append(channel(
"Suno FM - Dubai",
"http://50.7.71.27:9693/;stream/1", 75, "audio/mp3"))

channelList.append(channel(
"Sabras Radio - Dubai",
"http://radio.canstream.co.uk:8025/live.mp3", 75, "audio/mp3"))

channelList.append(channel(
"Hum FM",
"https://ice10.securenetsystems.net/HUMFM?", 75, "audio/mp3"))

channelList.append(channel(
"Evergreen Hits",
"http://192.240.102.133:11454/stream", 75, "audio/mp3"))

channelList.append(channel(
"SADA BHAR",
"http://192.240.102.133:8512/stream", 75, "audio/mp3"))

channelList.append(channel(
"Shuddeh Desi Radio",
"https://streamer.radio.co/se30891e37/low", 75, "audio/mpeg"))

channelList.append(channel(
"Unknown",
"http://16153.live.streamtheworld.com/SAM07AAC081_SC", 75, "audio/mp3"))

channelList.append(channel(
"TuneIn Top 40 Pop",
"http://rfcmedia.streamguys1.com/newpophits.mp3", 75, "audio/mp3"))

channelList.append(channel(
"Power 106 (Rap)",
"http://20813.live.streamtheworld.com/KPWRAAC.aac", 75, "audio/mp3"))

channelList.append(channel(
"TuneIn Today's Hits",
"http://rfcmedia.streamguys1.com/MusicPulse.mp3", 75, "audio/mp3"))

channelList.append(channel(
"TuneIn Rap Unclean",
"http://tunein4.streamguys1.com/hhbeafree5 ", 75, "audio/mp3"))

channelList.append(channel(
"Radio Centro",
"http://67.212.179.138:7172/stream", 75, "audio/mp3"))

#---------------------------------------------------------------------------------------------------------