import time
import unittest
from twitch_chat_recorder.twitchIRCConnector import *
from twitch_chat_recorder.twitchIRCStreamReader import *


class TestTwitchIRCStreamReader(unittest.TestCase):
    def setUp(self) -> None:
        self.nickname = 'learndatasci'
        self.oauth = 'oauth:43rip6j6fgio8n5xly1oum1lph8ikl1'  # FAKE oauth: DON'T publish a real ONE
        self.connector_tw = TwitchConnector(self.nickname, self.oauth)
        self.channel_name = ['Cerbero_Podcast']
        self.connector_tw.connect_channels(self.channel_name)

    def test_init(self):
        list_chatter_boxes = self.connector_tw.get_list_chatter_boxes()
        list_stream_reader = []
        index = 0
        for chatterBox in list_chatter_boxes:
            stream_reader = TwitchIRCStreamReader(index, "Reader #"+str(index), chatterBox)
            list_stream_reader.append(stream_reader)
            index += 1

        for streamReader in list_stream_reader:
            streamReader.start()
            # wait for thread to finish

        time.sleep(20)
        for streamReader in list_stream_reader:
            streamReader.terminate()

        for streamReader in list_stream_reader:
            streamReader.join()

        for streamReader in list_stream_reader:
            q = streamReader.get_rx_queue()
            self.assertIsNotNone(q)
