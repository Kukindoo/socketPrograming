import json
import socket
import threading
import time

from Connection import Connection


class Server:
    HEADER = 128 #initial message information. how long is 1st message
    FORMAT="UTF-8"

    def __init__(self, server_ip, port) -> None:
        '''
        Creates  and binds server to IP and PORT of the machine. The it start it.
        :param server_ip : str (IPv4)
        :param port: int
        return: none
        '''
        self.SERVER = server_ip
        self.PORT = port
        self.ADDR = (self.SERVER, self.PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.start()

    def handle_client(self, conn, addr):

        print(f"[NEW CONNECTION] {addr} conected.")
        connection_info = Connection(conn, addr)
        connection_info.connect()
        #connection object here?with connection, conn, addr?

        while connection_info.get_status():
            # self.sendToClient(json.dumps({"time" : time.ctime(), "opCode": "007", "text": "Authenticate yourself"}))
            #This happen at the start of connection
            msg = conn.recv(connection_info.get_next_message_size()).decode(self.FORMAT)
            if msg:
                self.doAction(json.loads(msg), connection_info)
                
                # #send ACK 
                # msg = conn.recv(msg_length).decode(self.FORMAT)
                # #send ACK
                # self.doAction(json.loads(msg), connection_info)

        conn.close()

    def ack_HEADER_size_b(self):
        '''
        Prepare Header sized message of Ackwnowledge
        '''
        message = "ACK".encode(self.FORMAT)        
        message += b" " * (self.HEADER - len(message))
        return message

    def sendToClient(self,msg, connection_info):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b" " * (self.HEADER - len(send_length))
        connection_info.get_socket().send(send_length)
        connection_info.get_socket().send(message)


    def doAction(self, action, connection_info):
        '''
        Decide what action to do regarding what opcode is sent
        :param action: dict
        :param connection_info: Connection
        '''
        #TODO: add log file here
        time = action.get("time")
        opCode = action.get("opCode")
        text = action.get("text")
        who = connection_info.get_who_is_it()
        
        if opCode == "000": # Print message to server            
            self.printMessageToServer(time, connection_info, text)
        elif opCode == "500": # Extract next message size 
            return self.handleHeader(text, connection_info)
        elif opCode == "999": # desconnect from server
            text = "[Disconnected] " + text
            self.printMessageToServer(time, connection_info, text, ack=False)
            return connection_info.disconnect()
        else:
            print("Not recognised opCode")
        connection_info.set_next_message_size(connection_info.get_default_message_size()) 
            
    def handleHeader(self, text, connection_info):
        '''
        Send acknowledge message to client and set expected message to it's size
        :param text: str
        :param connection_info: Connection
        return: none 
        '''        
        connection_info.set_next_message_size(int(text)) 
        connection_info.get_socket().send(self.ack_HEADER_size_b())

    def printMessageToServer(self, time, connection_info, text, ack = True):
        '''
        Print message to server console
        :param time: str
        :param connection_info: Connection
        :param text: str
        :param ack : Bool
        :return Bool
        '''
        print(f"[{time}] {connection_info.get_who_is_it()}: {text}")
        if ack:
            connection_info.get_socket().send(self.ack_HEADER_size_b())
        return True

    def start(self):
        '''
        Physicly starts the server and start to listen for new connections. When get one, he creates thread for it.
        '''
        print("[STARTING] server is starting...")
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.SERVER}")
        while True:
            conn, addr = self.server.accept()
            self.thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            self.thread.start()
            print(f"[ACTIVE TREAD] {threading.active_count() - 1}.")

if __name__ == "__main__":
    Server("192.168.1.11", 5050)



