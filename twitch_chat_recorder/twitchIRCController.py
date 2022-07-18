from twitch_chat_recorder.twitchIRCConnector import TwitchConnector
from twitch_chat_recorder.twitchIRCStreamReader import TwitchIRCStreamReader
from twitch_chat_recorder.twitchStoredInfo import StreamInfo
import threading
import time
import queue
import re


class TwitchMessageInterpreter:
    def __init__(self):
        self.re_exp_find_all_messages = r"(:\w*.*.\n)|(PING :\w*.*.\n)"
        self.pattern_find_messages = re.compile(self.re_exp_find_all_messages)

        self.reg_exp_twitch_messages = r":tmi.twitch.tv \d\d\d \w*.* :\w*.*\n"
        self.pattern_twitch_messages = re.compile(self.reg_exp_twitch_messages)

        self.reg_exp_ping_messages = r"PING :\w*.*.\n"
        self.pattern_ping_messages = re.compile(self.reg_exp_ping_messages)

        self.reg_exp_private_messages = r":\w*.*!\w*.*@\w*.*tmi.twitch.tv \w*.*\n"
        self.pattern_private_messages = re.compile(self.reg_exp_private_messages)

        self.reg_exp_private_messages_decode = r":(\w*.*)!\w*.*@\w*.*tmi.twitch.tv PRIVMSG #\w*.* :(\w*.*)\n"
        self.pattern_private_messages_decode = re.compile(self.reg_exp_private_messages_decode)

    def get_messages(self, raw_string):
        result = self.pattern_find_messages.findall(raw_string)
        return result

    def get_twitch_message(self, message):
        extracted = self.pattern_twitch_messages.findall(''.join(message))
        if len(extracted) > 0:
            return extracted
        else:
            return None

    def get_private_message(self, message):
        extracted = self.pattern_private_messages.findall(''.join(message))
        if len(extracted) > 0:
            return extracted
        else:
            return None

    def get_ping_message(self, message):
        extracted = self.pattern_ping_messages.findall(''.join(message))
        if len(extracted) > 0:
            return extracted
        else:
            return None

    def decode_private_message_data(self, message):
        extracted = self.pattern_private_messages_decode.findall(''.join(message))
        content = []
        for element in extracted:
            content.append((element[0], element[1]))
        return content


class TwitchIRCController:
    def __init__(self, nickname, oauth, list_channels_name):
        self.nickname = nickname
        self.oauth = oauth  # FAKE oauth: DON'T publish a real ONE
        self.list_channels_name = list_channels_name
        self.list_stream_reader = []
        self.list_streams_info = {}
        self.interpreter = TwitchMessageInterpreter()
        self.activities_req = queue.Queue()
        self._configure_reader()

    def run(self):
        self._start_activities()

    def _configure_reader(self):
        self.connector_tw = TwitchConnector(self.nickname, self.oauth)
        self.connector_tw.connect_channels(self.list_channels_name)

        index = 0
        for chatter_box in self.connector_tw.get_list_chatter_boxes():
            stream_reader = TwitchIRCStreamReader(index, "Reader #" + str(index), chatter_box)
            self.list_stream_reader.append(stream_reader)
            self.list_streams_info[chatter_box.channel_name] = StreamInfo(chatter_box.channel_name)
            index += 1

    def _start_activities(self):
        for stream_reader in self.list_stream_reader:
            stream_reader.start()
        new_thread = threading.Thread(target=self.reader)
        new_thread.start()
        new_thread.join()

    def reader(self):
        while True:
            for stream_reader in self.list_stream_reader:
                while not stream_reader.get_rx_queue().empty():
                    channel = stream_reader.get_chatter_box().channel_name
                    readings = stream_reader.get_rx_queue().get()
                    self.interpret_message(channel, readings[0], readings[1].decode("utf-8"))

            time.sleep(5)

    def interpret_message(self, channel, msg_timestamp, raw_string):
        messages = self.interpreter.get_messages(raw_string)

        for msg in messages:
            ping_msg = self.interpreter.get_ping_message(msg)
            if ping_msg is not None:
                self.activities_req.put(['PING', channel, ping_msg])
                print(msg_timestamp, "  PING: ", ping_msg)
            private_message = self.interpreter.get_private_message(msg)
            if private_message is not None:
                content = self.interpreter.decode_private_message_data(msg)
                for user_name, user_msg in content:
                    self.list_streams_info[channel].add_record(msg_timestamp, user_name, user_msg)

                print(msg_timestamp, "  private_msg: ", private_message)
            twitch_msg = self.interpreter.get_twitch_message(msg)
            if twitch_msg is not None:
                print("      TWITCH MESSAGE: ", twitch_msg)

        self._handle_activities()

        print("-----------------------------")

    def _handle_activities(self):
        while not self.activities_req.empty():
            try:
                activity = self.activities_req.get()
                if activity[0] == "PING":
                    channel = activity[1]
                    for stream_reader in self.list_stream_reader:
                        if channel is stream_reader.get_chatter_box().channel_name:
                            stream_reader.get_chatter_box().send_pong(activity[2])
                            print("PONG SENT")
            except Exception as err:
                print("|||||||||  ERROR: ", err)
