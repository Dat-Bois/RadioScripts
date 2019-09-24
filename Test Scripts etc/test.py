import ChannelsCC

#ChannelsCC.makeList()
#print(len(ChannelsCC.channelList))

#for i in range(1,len(ChannelsCC.channelList)):
	
#	print(ChannelsCC.channelList[i].getUrl())

import socket, pickle



HOST = '192.168.1.100'
PORT = 12345
# Create a socket connection.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Create an instance of ProcessData() to send to server.
variable = ChannelsCC.channelList[10]
# Pickle the object and send it to the server
data_string = pickle.dumps(variable)
s.send(data_string)

s.close()
print 'Data Sent to Server'