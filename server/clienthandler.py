import threading
import jsonpickle
import logging
import datetime
from MSSQL import checkEmailAlreadyExists, checkNicknameAlreadyExists, checkLogin, addUser
logging.basicConfig(level=logging.INFO)



class Clienthandler(threading.Thread): #Thread class
    numbers_clienthandlers = 0
    clients = {}
    def __init__(self, socketclient, messages_queue):
        threading.Thread.__init__(self)
        self.s = socketclient
        self.messages_queue = messages_queue
        self.id = Clienthandler.numbers_clienthandlers
        self.in_out_clh = self.s.makefile(mode='rw')
        Clienthandler.numbers_clienthandlers += 1

    def decode_msg(self, msg):
        return msg.decode()


    def userReg(self):
        logging.info("command: USERREG")
        jsondata = self.in_out_clh.readline().rstrip('\n')
        print(jsondata)
        newUser = jsonpickle.decode(jsondata)
        # ToDo! check if user email and nickname are unique

        if (checkEmailAlreadyExists(newUser.email)):
            anwser = "EMAILBUSY"

        elif (checkNicknameAlreadyExists(newUser.nickname)):
            anwser = "NCKNAMEBUSY"
        else:
            anwser = "VALID"
            addUser(newUser)
            Clienthandler.clients[self.in_out_clh] = newUser.nickname

        self.in_out_clh.write(anwser + "\n")  # not unique Nickname
        self.in_out_clh.flush()


    def checkLogin(self):
        logging.info("Command: CHECKLOGIN ")
        nickname = self.in_out_clh.readline().rstrip('\n')
        pwd = self.in_out_clh.readline().rstrip('\n')
        if (checkLogin(nickname, pwd)):
            anwser = "OK"
            Clienthandler.clients[self.s] = nickname
        else:
            anwser = "NOK"
        self.in_out_clh.write(anwser + "\n")
        self.in_out_clh.flush()


    def run(self):
        self.send_msg_gui_server("Chatserver up and running")
        commando = self.in_out_clh.readline().rstrip('\n')
        while commando.rstrip() != "CLOSE":
            if(commando == "USERREG"):
                self.userReg()


            elif(commando == "CHECKLOGIN"):
                self.checkLogin()
            elif(commando == "MSG"):
                nickname = self.in_out_clh.readline().rstrip('\n')


                msg = self.in_out_clh.readline().rstrip("\n")
                self.send_msg_gui_server(msg, nickname)
                anwser = "[" + datetime.datetime.now().strftime('%H:%M:%S') + "] " + nickname + " > "+ msg
                # Todo! Save message in database with timestamp!
                self.broadCast(anwser)
                # self.in_out_clh.flush()
            commando = self.in_out_clh.readline().rstrip('\n')


    def broadCast(self, msg):
        for sock in Clienthandler.clients:
            sock.send(bytes(msg.encode()))







    def send_msg_gui_server(self, message, user=None):
        if user == None:
            user = self.id
            self.messages_queue.put("CLH %d:> %s" % (user, message))
        else:
            self.messages_queue.put("Nickname %s:> %s" % (user, message))