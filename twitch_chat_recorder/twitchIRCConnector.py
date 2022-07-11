from socket import socket


class TwitchConnector:
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
        self._passString = f"PASS " + self.oauth + f"\n"
        self._nameString = f"NICK " + self.nickname + f"\n"

    def create_channel_connections(self, channels):
        _sockets = {}

        # Establish socket connections
        for channel in channels:
            _sockets[channel] = socket()
            _sockets[channel].connect((self._server, self._port))
            _sockets[channel].send(self._passString.encode('utf-8'))
            _sockets[channel].send(self._nameString.encode('utf-8'))

        return _sockets
