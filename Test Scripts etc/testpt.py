import socket, pickle
import ChannelsCC


HOST = 'localhost'
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr

data = conn.recv(4096)
data_variable = pickle.loads(data)
conn.close()
print data_variable
# Access the information by doing data_variable.process_id or data_variable.task_id etc..,
print data_variable.getUrl()
print 'Data received from client'