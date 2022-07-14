from twitch_chat_recorder.twitchIRCConnector import TwitchChatterbox
import threading
import time
import queue


class TwitchIRCStreamReader(threading.Thread):
    def __init__(self, thread_id, name, chatter_box):
        threading.Thread.__init__(self)
        self.chatterBox_connection = chatter_box
        if not isinstance(self.chatterBox_connection, TwitchChatterbox):
            raise ValueError('Argument object is not a TwitchChatterbox object')

        self.threadID = thread_id
        self.name = name
        self.keepAlive = True
        self.rx_queue = queue.Queue()

    def terminate(self):
        self.keepAlive = False

    def run(self):
        while self.keepAlive:
            try:
                self.rx_queue.put(self.chatterBox_connection.read())
            except Exception as e:
                print(" ERR--->", e)
            #time.sleep(3)

    def get_rx_queue(self):
        return self.rx_queue