from os.path import exists

class StreamInfo:
    def __init__(self, channel_name):
        self.channel_name = channel_name
        self.list_messages = [] #data type: [time.time(), str(userName), str(message)]

    # Add record to the Array list:
    #      Fields required are:
    #          time = time.ctime() of the message <- string
    #          user =  name of the user writing the message string
    #          user_massage = message string
    def add_record(self, time, user_name, user_message):
        self.list_messages.append((time, user_name, user_message))

    # Return the array list with the records in a tupla of three fields:
    #      Fields are:
    #          time = time.ctime() of the message <- string
    #          user =  name of the user writing the message string
    #          user_massage = message string
    def get_message_list(self):
        return self.list_messages

    # Get record of the array list. Will be a tupla of three fields:
    #       Parameter:
    #           index = index from 0 end of array list
    #      Fields returned are in a tuple:
    #          time = time.ctime() of the message <- string
    #          user =  name of the user writing the message string
    #          user_massage = message string
    #       If index is out of bound, return is None
    def get_record_by_index(self, index):
        if index >= len(self.list_messages) or index < 0:
            return None
        else:
            return self.list_messages[index]
