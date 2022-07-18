
class StreamInfo:
    def __init__(self, channel_name):
        self.channel_name = channel_name
        self.list_messages = [] #data type: [time.time(), str(userName), str(message)]

    def add_record(self, time, user_name, user_message):
        self.list_messages.append((time, user_name, user_message))
