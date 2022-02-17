import json
from operator import length_hint
import socket
import time

from Connection import Connection

class Client():



    HEADER = 128 #initial message information. how long is 1st message
    PORT = 5050
    SERVER = "192.168.1.11"
    ADDR = (SERVER, PORT)
    FORMAT="UTF-8"

    def __init__(self) -> None:
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        self.connection_info = Connection(self.client, self.ADDR)



    def send(self,msg):
        socket_ = self.connection_info.get_socket()
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = json.dumps({"time" : time.ctime(), "opCode": "500", "text" : str(msg_length) } ).encode(self.FORMAT)
        send_length += b" " * (self.HEADER - len(send_length))
        socket_.send(send_length)
        socket_.recv(self.HEADER).decode(self.FORMAT)
        #wait for ACK

        socket_.send(message)

        #Wait for ACK

    def __del__(self):
        self.send(json.dumps({"time" : time.ctime(), "opCode": "999", "text": "Client closed"}))

if __name__ == "__main__":
    c = Client()
    c.send(json.dumps({"time" : time.ctime(), "opCode": "000", "text": "Hello"}))