import unittest
from unittest.mock import patch, Mock
from twitch_chat_recorder.twitchIRCConnector import *


class TestTwitchConnector(unittest.TestCase):

    def setUp(self) -> None:
        self.nickname = 'learndatasci'
        self.oauth = 'oauth:43rip6j6fgio8n5xly1oum1lph8ikl1'  # FAKE oauth: DON'T publish a real ONE

    def test_init(self):
        '''
        verify the following parameters present initialized: nickname, oauth, server address, port

        '''
        self.nickname = 'learndatasci'
        self.oauth = 'oauth:43rip6j6fgio8n5xly1oum1lph8ikl1'  # FAKE oauth: DON'T publish a real ONE
        connector_tw = TwitchConnector(self.nickname, self.oauth)
        self.assertEqual('learndatasci', connector_tw.nickname)  # add assertion here
        self.assertEqual('oauth:43rip6j6fgio8n5xly1oum1lph8ikl1', connector_tw.oauth)  # add assertion here

        self.nickname = 'learndatasci2'
        self.oauth = '83rip6j6fgio8n5xly1oum1lph8ikl1'  # FAKE oauth: DON'T publish a real ONE
        connector_tw = TwitchConnector(self.nickname, self.oauth)
        self.assertEqual('learndatasci2', connector_tw.nickname)  # add assertion here
        self.assertEqual('83rip6j6fgio8n5xly1oum1lph8ikl1', connector_tw.oauth)  # add assertion here

        # VERIFY the server address and the port
        self.assertEqual('irc.chat.twitch.tv', connector_tw._server)
        self.assertEqual(6667, connector_tw._port)

    def test_create_dictionary_channel_socket(self):
        connector_tw = TwitchConnector(self.nickname, self.oauth)

        channels = ['Ninja', 'auronplay', 'Rubius', 'ibai']
        channel_socks = {}
        channel_socks = connector_tw.create_dictionary_channel_socket(channels)
        print(channel_socks.keys())
        index = 0
        for key, value in channel_socks.items():
            self.assertEqual(channels[index], key)
            index += 1

    def test_connect_channels(self):
        connector_tw = TwitchConnector(self.nickname, self.oauth)
        channels = ['Ninja', 'auronplay', 'Rubius', 'ibai']
        connector_tw.connect_channels(channels)


class TestTwitchChatterbox(unittest.TestCase):
    def setUp(self):
        self.userName = 'userName'
        self.password = 'password'
        self.channel_name = 'channelName'
        self._server = 'irc.chat.twitch.tv'
        self._port = 6667

        @patch('TwitchChatterbox.send')
        def mockSocketSend(self, send_mock):
            print(send_mock)

        @patch('TwitchChatterbox.recv')
        def mockSocketRecv(self, recv_mock):
            self.return_value = recv_mock

        self.chatter = TwitchChatterbox(self._server, self._port, self.userName, self.password, self.channel_name)
        self.chatter.send = Mock(return_value=None)
        self.chatter.recv = Mock(return_value=None)
        self.chatter.recv.return_value = ""
        self.chatter.set_name(self.userName)
        self.chatter.set_password(self.password)
        self.chatter.set_channel_name(self.channel_name)

    def test_send_NICK(self):
        input_string = f'NICK {self.userName}\r\n'.encode('utf-8')
        self.chatter.send_nick()
        self.chatter.send.assert_called_with(input_string)

    def test_send_PASS(self):
        input_string = f'PASS {self.password}\r\n'.encode('utf-8')
        self.chatter.send_pass()
        self.chatter.send.assert_called_with(input_string)

    def test_send_JOIN(self):
        input_string = f'JOIN #{self.channel_name}\r\n'.encode('utf-8')
        self.chatter.send_join()
        self.chatter.send.assert_called_with(input_string)

    def test_send_PRIVMSG(self):
        message = "private message"
        input_string = f'PRIVMSG #{self.channel_name} :{message} \r\n'.encode('utf-8')
        self.chatter.send_privmsg(message)
        self.chatter.send.assert_called_with(input_string)

    def test_send_PONG(self):
        test_message = "test"
        input_string = f'PONG {test_message}\r\n'.encode('utf-8')
        self.chatter.send_pong(test_message)
        self.chatter.send.assert_called_with(input_string)

    def test_read(self):
        read_text = 'message to read'
        self.chatter.recv.return_value = read_text
        result = self.chatter.read()

        self.assertEqual(read_text, result)
