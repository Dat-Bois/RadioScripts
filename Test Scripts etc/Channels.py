import time

class channel:
	
	#-----------------------------------------------
	def __init__(self, name, url, volume):
		self.name = name
		self.url = url
		self.volume = volume
	
	def getUrl(self):
		return self.url
	
	def getName(self):
		return self.name
	
	def getVolume(self):
		return self.volume
#--------------------------------------------------------------------------------------------------
def setVolume(channelNum, newVolume):
	channelList[channelNum].volume = newVolume

channelList = []

channelList.append(channel(
"PLACE HOLDER",
"No Link", 0))

channelList.append(channel(
"Suno FM - Dubai",
"http://50.7.71.27:9693/", 75))

channelList.append(channel(
"Sabras Radio - Dubai",
"http://radio.canstream.co.uk:8025/live.mp3", 75))

channelList.append(channel(
"Hum FM",
"http://209.15.226.17:9016/stream", 75))

channelList.append(channel(
"Evergreen Hits",
"http://192.240.102.133:11454/stream", 75))

channelList.append(channel(
"SADA BHAR",
"http://192.240.102.133:8512/stream", 75))

channelList.append(channel(
"Desi Music Mix",
"http://66.23.234.242:8012/", 75))

channelList.append(channel(
"Channel 93.3", #short gaps in between for some goddamn reason
"https://c13.prod.playlists.ihrhls.com/241/playlist.m3u8", 75))

channelList.append(channel(
"NDTV",
"http://stream1.ndtv.com:8080/on-ndtvindia", 75))

channelList.append(channel(
"Unknown",
"http://16153.live.streamtheworld.com/SAM07AAC081_SC", 75))

channelList.append(channel(
"Z90.3",
"http://17813.live.streamtheworld.com/XHTZFMAAC.aac", 75))

channelList.append(channel(
"Radio Spice",
"http://ice5.securenetsystems.net/1054?playSessionID=180159E0-DA55-EF27-BDA458574AD82E89", 75))

channelList.append(channel(
"Radio Centro",
"http://67.212.179.138:7172/", 75))

print channelList[2].name
length = len(channelList) - 1
print length
#---------------------------------------------------------------------------------------------------------