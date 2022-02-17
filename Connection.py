
from socket import socket


class Connection:
    DEFAULT_MESSAGE_SIZE = 128
    
    #nickname
    #last message received (time)
    def __init__(self, socket_, address) -> None:
        self.socket = socket_
        self.address = address
        self.conection_status = False
        self.nextMessageSize = self.DEFAULT_MESSAGE_SIZE
        self.authetication = False

    def connect(self):
        self.conection_status = True

    def disconnect(self):
        self.conection_status = False

    def get_status(self):
        return self.conection_status

    def get_who_is_it(self):
        return self.address

    def get_socket(self):
        return self.socket

    def set_next_message_size(self,i):
        self.nextMessageSize = i
    
    def get_next_message_size(self):
        return self.nextMessageSize

    def get_default_message_size(self):
        return self.DEFAULT_MESSAGE_SIZE
        