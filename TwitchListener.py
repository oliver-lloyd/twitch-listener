import socket
import Utils
import time

class twitch(socket.socket):
    
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
        # Establish connection
        self._sockets = {}
        self.channels = channels
        self._loggers = {}
        
        for channel in channels:
            self._sockets[channel] = socket.socket()
            self._sockets[channel].connect((self._server, self._port))
            self._sockets[channel].send(self._passString.encode('utf-8'))
            self._sockets[channel].send(self._nameString.encode('utf-8'))
            
            joinString = f"JOIN #" + channel.lower() + f"\n"
            self._sockets[channel].send(joinString.encode('utf-8'))
            self._loggers[channel] = Utils.setup_loggers(channel, channel + '.log')
        
    def listen(self, channels, duration = 0):
        # Need to change while loop--- "while (currentTime - startTime) < duration"
        
        self._join_channels(channels)
        
        while True: 
            for channel in self.connected_channels:
                if Utils.is_live(channel, self.client_id):
                    response = self._sockets[channel].recv(1024).decode("utf-8") 
                    if response == "PING :tmi.twitch.tv\r\n":
                        self._sockets[channel].send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                    else:
                        self._loggers[channel].info(response)
                    time.sleep(31/20)
                else:
                    pass
        for channel in self.connected_channels:
            self._sockets[channel].close()
                
        
            

