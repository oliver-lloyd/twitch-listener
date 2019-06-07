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
        """
        Method for scraping chat data from Twitch channels.

        Parameters:
            channels (string or list) - Channel(s) to connect to.
            duration (int)            - Length of time to listen for.
            timer (bool)              - Debugging feature, will likely be removed in later version. 
        """

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
     
        
    def _split_line(self, line, firstLine = False):
        prefix = line[:28]
        
        if firstLine:
            line = line.split('End of /NAMES list\\r\\n')[1]
            
        splits = [message for message in line.split('\\r\\n') if 'PRIVMSG' in message]
        
        for i, case in enumerate(splits):
            if firstLine or i != 0:
                splits[i] = prefix + splits[i]
                
        return splits

    def parse_logs(self, timestamp = True, channels = []):
        """
        Method for converting raw data from text logs into .CSV format.

        Parameters:
            timestamp (boolean, optional) - Whether or not to include the timestamp of chat messages. 
                                            (Note: timestamps represent when message was retrieved, not sent)
            channels (list, optional)     - List of channel usernames for whom the text logs will be parsed into csv format.
                                            If none are specified, the channels that are currently joined will be parsed
        """

        # Check if specific list of channels is given
        if len(channels) == 0:
            try:
                channels = self.joined
            except:
                print("Please either connect to channels, or specify a list of log files to parse.")
        for channel in channels:
            filename = channel + ".log"
            lines = []
            with open(filename) as f:
                for line in f:
                    if line not in lines:
                        lines.append(line)
                        
            # Separate the raw strings into separate messages 
            split_messages = []
            for line in lines:
                count = line.count('.tmi.twitch.tv PRIVMSG #')
                                   
                if 'Your host is tmi.twitch.tv' in line:
                    if 'PRIVMSG' in line:
                        for msg in self._split_line(line, firstLine = True):
                            split_messages.append(msg)
                    else:      
                        pass
                                
                elif count == 0:
                    pass
                    
                elif count == 1:
                    if line.endswith('\\r\\n\'\n'):
                        split_messages.append(line[:-6])
                    else:
                        split_messages.append(line)
                        
                else:
                    for msg in self._split_line(line):
                        split_messages.append(msg)
            
            # Parse username, message text and (optional) datetime
            data = []          
            for ind, message in enumerate(split_messages):
                username = None
                message_text = None
                datetime = None
                
                row = {}
                
                # Parse message text
                hash_channel_point = message.find("PRIVMSG #" + channel)
                slice_ = message[hash_channel_point:]
                slice_point = slice_.find(":") + 1
                message_text = slice_[slice_point:]
                row['text'] = message_text
                
                # Parse username
                b = message.find("b")
                exclam = message.find("!")
                username = message[b:exclam][3:]
                row['username'] = username
                
                # Parse timestamp (note: dates are in weirdo American format)
                if timestamp:
                    datetime = message[:23] 
                    row['timestamp'] = datetime
            
                # Store observations
                data.append(row)
            
            # Write data to file
            pd.DataFrame(data).to_csv(channel + ".csv", index = False)
                                        
                                
                                    
                        
