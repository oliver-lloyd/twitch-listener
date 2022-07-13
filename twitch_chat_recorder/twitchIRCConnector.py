from socket import socket, AddressFamily, SocketKind


class TwitchConnector:
    def __init__(self, nickname, oauth):
        self.nickname = nickname

        if oauth.startswith('oauth:'):
            self.oauth = oauth
        else:
            self.oauth = 'oauth:' + oauth

        # IRC parameters
        self._server = 'irc.chat.twitch.tv'
        self._port = 6667

        self._passString = f"PASS " + self.oauth + f"\n"
        self._nameString = f"NICK " + self.nickname + f"\n"

    def create_dictionary_channel_socket(self, channels):
        _sockets = {}
        # Establish socket connections
        for channel in channels:
            _sockets[channel] = TwitchChatterbox()

        return _sockets

    def connect_channels(self, channels):
        sock_list = self.create_dictionary_channel_socket(channels)

        for channel, sock in sock_list.items():
            sock.connect((self._server, self._port))
            sock.send(self._passString.encode('utf-8'))
            sock.send(self._nameString.encode('utf-8'))
            join_string = f"JOIN #" + channel + f"\n"
            sock.send(join_string.encode('utf-8'))
            self.is_successful_authenticated(sock)


    @staticmethod
    def is_successful_authenticated(chatter_sock):
        auth_twitch_response = chatter_sock.read()
        if 'tmi.twitch.tv NOTICE' in str(auth_twitch_response) and \
                'failed' not in str(auth_twitch_response):
            chatter_sock.isAuthenticated = True
            print(chatter_sock.channel_name, " is connected\n")


class TwitchChatterbox(socket):
    def __init__(self):
        socket.__init__(self, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM)
        self.settimeout(2.0)
        self.family
        self.isAuthenticated = False
        self.name = ''
        self.password = ''
        self.channel_name = ''

    def __del__(self):
        self.close()

    def set_name(self, name):
        self.name = name

    def set_password(self, password):
        self.password = password

    def set_channel_name(self, channel_name):
        self.channel_name = channel_name

    def send_PRIVMSG(self, post_chat_message):
        self.send(f'PRIVMSG '+post_chat_message+f"\n")

    def send_NICK(self):
        self.send(f'NICK {self.name}\n')
        #self.send(b'1')

    def send_PASS(self):
        self.send(f"PASS " + self.password + f"\n")

    def send_PONG(self, text_from_ping):
        self.send(f'PONG ' + text_from_ping + f"\n")

    def send_JOIN(self):
        self.send(f'JOIN #'+self.channel_name + f"\n")

    def read(self):
        read_msg = ''
        try:
            read_msg = self.recv(16384)
        except TimeoutError:
            print("timeout occurred")
        except ConnectionResetError:
            print("An existing connection was forcibly closed by the remote host")
        return read_msg
