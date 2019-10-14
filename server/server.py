import logging
import socket
import threading

from clienthandler import Clienthandler

logging.basicConfig(level=logging.INFO)

class ChatroomServer(threading.Thread): #Thread class

    def __init__(self, host, port, message_queue):
        threading.Thread.__init__(self)
        self.__isconnected = False
        self.host = host
        self.port = port
        self.message_queue = message_queue

    @property
    def is_connected(self):
        return self.__isconnected

    def print_msg_GUI_server(self,msg):
        self.message_queue.put("Server:> %s"%msg)

    def init_server(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #make socket object
        self.serversocket.bind((self.host,self.port))
        self.serversocket.listen(5)
        self.__isconnected = True
        self.print_msg_GUI_server("SERVER ESTABLISHED")


    def close_server_socket(self):
        self.print_msg_GUI_server('CLOSE SERVER')
        self.serversocket.close()


    def run(self):
        number_of_received_msg = 0
        try:
            while 1:

                    self.print_msg_GUI_server("Waiting for a new client ...")
                    clientsocket, addr = self.serversocket.accept()
                    self.print_msg_GUI_server("Got a connection from: %s" %str(addr))
                    clh = Clienthandler(clientsocket, self.message_queue)
                    clh.start()
                    self.print_msg_GUI_server("Current Thread count %i" %threading.active_count())
        except Exception as ex:
            self.print_msg_GUI_server("Seversocket closed")
            logging.ERROR("Exception occurd: %s" %ex)



