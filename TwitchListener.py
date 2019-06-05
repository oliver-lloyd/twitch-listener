from socket import socket
import Utils
from time import sleep, time, clock

class twitch(socket):
    
    def __init__(self, nickname, oauth, client_id):
        self.nickname = nickname
        self.oauth = oauth
        self.client_id = client_id
        
        # IRC parameters
        self._server = "irc.chat.twitch.tv"
        self._port = 6667
        self._passString = f"PASS " + oauth + f"\n"
        self._nameString = f"NICK " + nickname + f"\n"
        

    def _join_channels(self, channels):
        self._sockets = {}
        self.joined = []
        self._loggers = {}
        
        # Establish socket connections
        for channel in channels:
            if Utils.is_live(channel, self.client_id):
                self._sockets[channel] = socket()
                self._sockets[channel].connect((self._server, self._port))
                self._sockets[channel].send(self._passString.encode('utf-8'))
                self._sockets[channel].send(self._nameString.encode('utf-8'))
                
                joinString = f"JOIN #" + channel.lower() + f"\n"
                self._sockets[channel].send(joinString.encode('utf-8'))
                self._loggers[channel] = Utils.setup_loggers(channel, channel + '.log')
                
                self.joined.append(channel)
            else:
                print(channel + " is not live right now.")
        
        
    def listen(self, channels, duration = 0, timer = False):
        self._join_channels(channels)

        if timer:
            startTime = time()
        
        # Collect data while duration not exceeded and channels are live
        clock()
        while clock() < duration: 
            
            for channel in self.joined:
                if Utils.is_live(channel, self.client_id):
                    response = self._sockets[channel].recv(1024)
                    
                    if response == "PING :tmi.twitch.tv\r\n":
                        self._sockets[channel].send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                    else:
                        self._loggers[channel].info(response)
                        
                    sleep(60/800) 
                    
                else: # If not utils.is_live()
                    pass
        if timer:
            print("Collected for " + str(time()-startTime) + " seconds")

        # Close sockets once not collecting date
        for channel in self.joined:
            self._sockets[channel].close()

    def parse_logs(self):
        # stuff will go here
        pass
                
        
            

