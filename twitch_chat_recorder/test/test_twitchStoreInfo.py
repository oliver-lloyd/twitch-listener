import unittest
import time
from twitch_chat_recorder.twitchStoredInfo import StreamInfo


class TestTwitchStoreInfo(unittest.TestCase):

    def test_init(self):
        name1 = "test1_streamer_name"
        self.streamer_messages = StreamInfo(name1)
        self.assertEqual(self.streamer_messages.channel_name, name1)

    def test_add_record(self):
        name1 = "test1_streamer_name"
        self.streamer_messages = StreamInfo(name1)

        user_name1_1 = "user1"
        time1_1_1 = time.ctime()
        user_message1_1_1 = "message1"
        time1_1_2 = time.ctime()
        user_message1_1_2 = "message2"
        user_name1_2 = "user2"
        time1_2_1 = time.ctime()
        user_message1_2_1 = "message3"
        time1_2_2 = time.ctime()
        user_message1_2_2 = "message4"
        self.streamer_messages.add_record(time1_1_1, user_name1_1, user_message1_1_1)
        self.streamer_messages.add_record(time1_1_2, user_name1_1, user_message1_1_2)
        self.streamer_messages.add_record(time1_2_1, user_name1_2, user_message1_2_1)
        self.streamer_messages.add_record(time1_2_2, user_name1_2, user_message1_2_2)

        self.assertEqual(self.streamer_messages.channel_name, name1)
        self.assertEqual(self.streamer_messages.list_messages[0][0], time1_1_1)
        self.assertEqual(self.streamer_messages.list_messages[0][1], user_name1_1)
        self.assertEqual(self.streamer_messages.list_messages[0][2], user_message1_1_1)
        self.assertEqual(self.streamer_messages.list_messages[1][0], time1_1_2)
        self.assertEqual(self.streamer_messages.list_messages[1][1], user_name1_1)
        self.assertEqual(self.streamer_messages.list_messages[1][2], user_message1_1_2)

        self.assertEqual(self.streamer_messages.list_messages[2][0], time1_2_1)
        self.assertEqual(self.streamer_messages.list_messages[2][1], user_name1_2)
        self.assertEqual(self.streamer_messages.list_messages[2][2], user_message1_2_1)
        self.assertEqual(self.streamer_messages.list_messages[3][0], time1_2_2)
        self.assertEqual(self.streamer_messages.list_messages[3][1], user_name1_2)
        self.assertEqual(self.streamer_messages.list_messages[3][2], user_message1_2_2)

    def test_get_message_list(self):
        name1 = "test1_streamer_name"
        self.streamer_messages = StreamInfo(name1)

        user_name1_1 = "user1"
        time1_1_1 = time.ctime()
        user_message1_1_1 = "message1"
        time1_1_2 = time.ctime()
        user_message1_1_2 = "message2"
        user_name1_2 = "user2"
        time1_2_1 = time.ctime()
        user_message1_2_1 = "message3"
        time1_2_2 = time.ctime()
        user_message1_2_2 = "message4"
        self.streamer_messages.add_record(time1_1_1, user_name1_1, user_message1_1_1)
        self.streamer_messages.add_record(time1_1_2, user_name1_1, user_message1_1_2)
        self.streamer_messages.add_record(time1_2_1, user_name1_2, user_message1_2_1)
        self.streamer_messages.add_record(time1_2_2, user_name1_2, user_message1_2_2)

        list_returned = self.streamer_messages.get_message_list()

        self.assertEqual(self.streamer_messages.channel_name, name1)
        self.assertEqual(list_returned[0][0], time1_1_1)
        self.assertEqual(list_returned[0][1], user_name1_1)
        self.assertEqual(list_returned[0][2], user_message1_1_1)

        self.assertEqual(list_returned[1][0], time1_1_2)
        self.assertEqual(list_returned[1][1], user_name1_1)
        self.assertEqual(list_returned[1][2], user_message1_1_2)

        self.assertEqual(list_returned[2][0], time1_2_1)
        self.assertEqual(list_returned[2][1], user_name1_2)
        self.assertEqual(list_returned[2][2], user_message1_2_1)

        self.assertEqual(list_returned[3][0], time1_2_2)
        self.assertEqual(list_returned[3][1], user_name1_2)
        self.assertEqual(list_returned[3][2], user_message1_2_2)

    def test_get_record_by_index(self):
        name1 = "test1_streamer_name"
        self.streamer_messages = StreamInfo(name1)

        user_name1_1 = "user1"
        time1_1_1 = time.ctime()
        user_message1_1_1 = "message1"
        time1_1_2 = time.ctime()
        user_message1_1_2 = "message2"
        user_name1_2 = "user2"
        time1_2_1 = time.ctime()
        user_message1_2_1 = "message3"
        time1_2_2 = time.ctime()
        user_message1_2_2 = "message4"
        self.streamer_messages.add_record(time1_1_1, user_name1_1, user_message1_1_1)
        self.streamer_messages.add_record(time1_1_2, user_name1_1, user_message1_1_2)
        self.streamer_messages.add_record(time1_2_1, user_name1_2, user_message1_2_1)
        self.streamer_messages.add_record(time1_2_2, user_name1_2, user_message1_2_2)

        keep_going = True
        index = 0
        list_returned = []
        while keep_going:
            record = self.streamer_messages.get_record_by_index(index)
            if record is None:
                keep_going = False
            else:
                list_returned.append(record)
                index += 1

        list_returned = self.streamer_messages.get_message_list()

        self.assertEqual(self.streamer_messages.channel_name, name1)
        self.assertEqual(list_returned[0][0], time1_1_1)
        self.assertEqual(list_returned[0][1], user_name1_1)
        self.assertEqual(list_returned[0][2], user_message1_1_1)

        self.assertEqual(list_returned[1][0], time1_1_2)
        self.assertEqual(list_returned[1][1], user_name1_1)
        self.assertEqual(list_returned[1][2], user_message1_1_2)

        self.assertEqual(list_returned[2][0], time1_2_1)
        self.assertEqual(list_returned[2][1], user_name1_2)
        self.assertEqual(list_returned[2][2], user_message1_2_1)

        self.assertEqual(list_returned[3][0], time1_2_2)
        self.assertEqual(list_returned[3][1], user_name1_2)
        self.assertEqual(list_returned[3][2], user_message1_2_2)
