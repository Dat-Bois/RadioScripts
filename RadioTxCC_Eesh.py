import time
import datetime
from threading import Thread

import pychromecast
from threading import Thread
import socket, pickle
import ChannelsCC

cast = None
mc = None

def keepMCAlive():
    global mc
    global cast
    while(1):
        timeNow = str(datetime.datetime.now().time())+": "
        print(timeNow+"keeping alive: Playing "+ str(mc.status.content_id))
        time.sleep(120)# every 2 minutes
        
    
    
    
def getMc():
    global mc
    global cast
    chromecastName = 'All'
    print("looking for chromecasts: " + chromecastName);
    chromecasts = pychromecast.get_chromecasts(tries=3)
    [cc.device.friendly_name for cc in chromecasts]

    cast = next(cc for cc in chromecasts if cc.device.friendly_name == chromecastName)

    print("Wait for chromecastName: '"+ chromecastName+ "' to be ready...\n")
    cast.wait()
    print("Ready...\n")

    mc = cast.media_controller	
	
def rcv():
    
    global cast 
    global mc
    
    HOST = '192.168.1.100'
    PORT = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))

	
    while True:
        print ('Listening at '+HOST)
        s.listen(1)
        conn, addr = s.accept()
        #print ('Connected by ' + addr)

        data = conn.recv(4096)
        data_variable = pickle.loads(data)
        conn.close()
        print (data_variable)
        # Access the information by doing data_variable.process_id or data_variable.task_id etc..,
        print (data_variable.pausePlay())
        print (data_variable.getUrl())
        print (data_variable.getType())
        print ('Data received from client')
        #-----------------------------------------------
                
        if data_variable.pausePlay() == "pause":
            #getMc()
            #mc.play_media("sfkls", mime, stream_type="LIVE")
            #mc.block_until_active(timeout=2)
            #mc.play()
            mc.pause()
            print("PAUSED")
        elif data_variable.pausePlay() == "play":
            #getMc()
            #mc.play_media(URL, mime, stream_type="LIVE")
            #mc.block_until_active()
            #mc.play()
            mc.play()
            print("PLAYING")
        elif data_variable.pausePlay() == "reconnect":
            cast.disconnect(None, False)
            getMc()
            print("reset")
        else:
            #-----------------------------------------------------------------------------#
            #getMc()
            URL = data_variable.getUrl()
            mime = data_variable.getType()
            print("start stream...")
            x=0
            while (x==0):
                try:
                    mc.play_media(URL, mime, stream_type="LIVE")
                    print (cast.status.volume_level)
                    x=1
                except:
                    print("...........exception occured.......")
                    x=0
                    getMc()


            if(x==1):
                print("block till active...")
                mc.block_until_active()
                mc.play()
                time.sleep(2)
                print("content ID " + str(mc.status.content_id));


            
        
getMc()
thread = Thread(target = keepMCAlive)
thread.start()

#now start listening
rcv()
