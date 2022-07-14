from socket import socket, AddressFamily, SocketKind


class TwitchConnector:
    def __init__(self, nickname, oauth):
        self.nickname = nickname
        self.oauth = oauth

        # IRC parameters
        self._server = 'irc.chat.twitch.tv'
        self._port = 6667

        self.list_chatter_boxs = []

    def create_dictionary_channel_socket(self, channels):
        _sockets = {}
        # Establish socket connections
        for channel in channels:
            _sockets[channel] = TwitchChatterbox(self._server, self._port, self.nickname, self.oauth, channel)

        return _sockets

    def connect_channels(self, channels):
        chatter_boxes = self.create_dictionary_channel_socket(channels)

        for channel, chatterbox in chatter_boxes.items():
            self.list_chatter_boxs.append(chatterbox)

    def get_list_chatter_boxs(self):
        return self.list_chatter_boxs


class TwitchChatterbox(socket):
    def __init__(self, server, port, nickname, oauth, channel):
        self._server = server
        self._port = port
        self.nickname = nickname
        self.channel_name = channel
        if oauth.startswith('oauth:'):
            self.oauth = oauth
        else:
            self.oauth = 'oauth:' + oauth
        self._passString = f"PASS " + self.oauth + f"\n"
        self._nameString = f"NICK " + self.nickname + f"\n"
        socket.__init__(self, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM)
        self.connect((self._server, self._port))
        self.send(self._passString.encode('utf-8'))
        self.send(self._nameString.encode('utf-8'))
        join_string = f"JOIN #" + channel.lower() + f"\n"
        self.send(join_string.encode('utf-8'))

        #self.settimeout(5.0)
        self.isAuthenticated = False

    def __del__(self):
        self.close()

    def set_name(self, name):
        self.nickname = name

    def set_password(self, password):
        self.oauth = password

    def set_channel_name(self, channel_name):
        self.channel_name = channel_name

    def send_PRIVMSG(self, post_chat_message):
        print(f"PRIVMSG #{self.channel_name} :{post_chat_message} \n")
        self.send(f"PRIVMSG #{self.channel_name} :{post_chat_message} \n".encode('utf-8'))

    def send_NICK(self):
        self.send(f'NICK {self.nickname}\n'.encode('utf-8'))

    def send_PASS(self):
        self.send(f"PASS {self.oauth}\n".encode('utf-8'))

    def send_PONG(self, text_from_ping):
        self.send(f'PONG {text_from_ping}\n'.encode('utf-8'))

    def send_JOIN(self):
        self.send(f'JOIN #{self.channel_name }\n'.encode('utf-8'))

    def read(self):
        read_msg = ''
        try:
            read_msg = self.recv(16384)
        except TimeoutError:
            print("timeout occurred")
        except ConnectionResetError:
            print("An existing connection was forcibly closed by the remote host")
        return read_msg

    def is_authenticated(self):
        return self.isAuthenticated
