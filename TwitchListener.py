from socket import socket
from time import time, sleep
import Utils
import pandas as pd

class twitch(socket):
    
    def __init__(self, nickname, oauth, client_id):
        self.nickname = nickname
        
        self.client_id = client_id
        if oauth.startswith('oauth:'):
            self.oauth = oauth
        else:
            self.oauth = 'oauth:' + oauth
            
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
        
        if type(channels) is str:
            channels = [channels]
            
        self._join_channels(channels)
        
        
        
        startTime = time()
        
        # Collect data while duration not exceeded and channels are live
        while (time() - startTime) < duration: 
            
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
            

    def parse_logs(self, timestamp = False, channels = None):

        if channels == None:
            channels = self.joined
        
        for channel in channels:
            
            filename = channel + ".log"
            
            with open(filename) as f:
                raw_text = f.read()
                
            drop_garbage = raw_text.split('End of /NAMES list')[-1]
            
            raw_messages = drop_garbage[10:]
                
            lines = raw_messages.split('\\r\\n')[:-1]
            
            #lines = []
            
            # Drop duplicate observations
            split_messages = []
            for line in lines:
                if line not in split_messages:
                    split_messages.append(line)
                    
                
                
            data = []
            
            for ind, message in enumerate(split_messages):
                username = None
                datetime = None
                message_text = None
                row = {}
                
                # Parse message text
                hash_channel_point = message.find("PRIVMSG #" + channel)
                slice_ = message[hash_channel_point:]
                slice_point = slice_.find(":") + 1
                message_text = slice_[slice_point:]
                row['text'] = message_text
                
                case_check = message.find("20") # Normal messages should have datetime at the beginning (note, this will break in the year 2100 lol)
                
                
                if -1 < case_check < 5: # case when: normal messages
                    
                    # Parse username
                    b = message.find("b")
                    exclam = message.find("!")
                    username = message[b:exclam][3:]
                    row['username'] = username
                    
                    # Parse timestamp
                    if timestamp:
                        datetime = message[case_check: case_check + 18] # Dates are in weirdo American format
                        row['timestamp'] = datetime
                    
                elif message.startswith(":"): # case when: messages are sent at the exact same timestamp (usually bots)
                    
                    # Parse username
                    exclam = message.find("!")
                    username = message[1:exclam]
                    row['username'] = username
                    
                     # Parse timestamp
                    if timestamp:
                        datetime = data[ind-1]['timestamp']
                        row['timestamp'] = datetime
                
                data.append(row)
                
            pd.DataFrame(data).to_csv(channel + ".csv", index = False)
                    
            
                
    
