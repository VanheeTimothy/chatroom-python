import logging
import socket
from tkinter import *
from tkinter import messagebox
from classes.User import User
import jsonpickle
from threading import Thread
from queue import Queue
import datetime

logging.basicConfig(level=logging.INFO)


class Window(Frame):
    ACTIVE_USERS = []

    register = False

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(sticky=W + E + N + S)

        # set up gui frames
        self.Frame1 = Frame(master)
        self.Frame1.grid(row=0, column=0, rowspan=2, columnspan=1, sticky=W + E + N + S)
        self.Frame2 = Frame(master)
        self.Frame2.grid(row=2, column=0, rowspan=1, columnspan=1, sticky=W + E + N + S)
        self.Frame3 = Frame(master)
        self.Frame3.grid(row=0, column=1, rowspan=2, columnspan=2, sticky=W + E + N + S)



        self.init_window()
        self.makeConnectionWithServer()







    def init_window(self):
        self.master.title("Welcome to the chatroom.")
        self.labelIntro = Label(self.Frame1, text="Welcome to the chatroom! \nRegister now or login if you already have an account")
        self.labelIntro.grid(row=0)
        # self.pack(fill=BOTH, expand=1)
        self.buttonRegister = Button(self.Frame1, text="Register", command=self.Register)
        self.buttonRegister.grid(row=1,  column=0, columnspan=2, padx=(5, 5), sticky=N + S + E + W)
        self.buttonLogin = Button(self.Frame1, text="Login", command=self.login)
        self.buttonLogin.grid(row=2, column=0, columnspan=2, padx=(5, 5), sticky=N + S + E + W)
        root.geometry("300x100")

    def hide_init_window(self):
        self.buttonRegister.grid_forget()
        self.buttonLogin.grid_forget()
        self.labelIntro.grid_forget()



    def Register(self):
        root.geometry("350x170")
        self.master.title("Register a new user")
        self.hide_init_window()
        self.labelName = Label(self.Frame1, text="Name: ")
        self.labelName.grid(row=0)
        self.labelNick = Label(self.Frame1, text="Nickname: ")
        self.labelNick.grid(row=1)
        self.labelnewEmail = Label(self.Frame1, text="Email: ")
        self.labelnewEmail.grid(row=2)
        self.labelPassword1 = Label(self.Frame1, text="password: ")
        self.labelPassword1.grid(row=3)
        self.labelPassword2 = Label(self.Frame1, text="re-enter password")
        self.labelPassword2.grid(row=4)
        self.entryName = Entry(self.Frame1, width=40)
        self.entryName.grid(row=0, column=1, padx=(5,5))
        self.entryNick = Entry(self.Frame1, width=40)
        self.entryNick.grid(row=1, column=1, padx=(5, 5))
        self.entrynewEmail = Entry(self.Frame1, width=40)
        self.entrynewEmail.grid(row=2, column=1, padx=(5, 5))
        self.entryPassword1 = Entry(self.Frame1, width=40, show="*")
        self.entryPassword1.grid(row=3, column=1, padx=(5, 5))
        self.entryPassword2 = Entry(self.Frame1, width=40, show="*")
        self.entryPassword2.grid(row=4, column=1, padx=(5, 5))
        self.buttonReg = Button(self.Frame1, text="Go to chattroom", command=self.checkInputReg)
        self.buttonReg.grid(row=5, column=0, columnspan=2, padx=(5, 5), sticky=N + S + E + W)
        self.buttonCancel = Button(self.Frame1, text="Cancel", command=self.cancel)
        self.buttonCancel.grid(row=6, column=0, columnspan=2, padx=(5, 5), sticky=N + S + E + W)
        Grid.rowconfigure(self.Frame1, 8, weight=1)
        Grid.columnconfigure(self.Frame1, 2, weight=1)
        Window.register = True

    def hide_register_window(self):
        self.labelName.grid_forget()
        self.labelNick.grid_forget()
        self.labelnewEmail.grid_forget()
        self.labelPassword1.grid_forget()
        self.labelPassword2.grid_forget()
        self.entryName.grid_forget()
        self.entryNick.grid_forget()
        self.entrynewEmail.grid_forget()
        self.entryPassword1.grid_forget()
        self.entryPassword2.grid_forget()
        self.buttonReg.grid_forget()
        self.buttonCancel.grid_forget()


    def login(self):
        self.hide_init_window()
        self.labelNickname = Label(self.Frame1, text="Nickname: ")
        self.labelNickname.grid(row=0, column=0)
        self.entryNickname = Entry(self.Frame1, width=40)
        self.entryNickname.grid(row=0, column=1, padx=(5, 5))
        self.labelPassword = Label(self.Frame1, text="password: ")
        self.labelPassword.grid(row=1,column=0)
        self.entryPassword = Entry(self.Frame1, width=40, show="*")
        self.entryPassword.grid(row=1, column=1, padx=(5, 5))
        self.buttonChatroom = Button(self.Frame1,text="Go to chattroom", command=self.checkLogin)
        self.buttonChatroom.grid(row=2, column=0, columnspan=2, padx=(5, 5), sticky=N + S + E + W)
        self.buttonCancel = Button(self.Frame1, text="Cancel", command=self.cancel)
        self.buttonCancel.grid(row=3, column=0, columnspan=2, padx=(5, 5), sticky=N + S + E + W)
        Window.register = False

    def hide_login_window(self):
        self.labelNickname.grid_forget()
        self.entryNickname.grid_forget()
        self.labelPassword.grid_forget()
        self.entryPassword.grid_forget()
        self.buttonChatroom.grid_forget()
        self.buttonCancel.grid_forget()


    def checkInputReg(self):
        pwd1 = self.entryPassword1.get()
        pwd2 = self.entryPassword2.get()
        name = self.entryName.get()
        email = self.entrynewEmail.get()
        nickName = self.entryNick.get()
        if pwd1 == pwd2:
            user = User(name, nickName, email, pwd1)
            self.my_writer_obj.write("USERREG\n")  # command to let server know we are sending new user
            self.my_writer_obj.write(jsonpickle.encode(user) + "\n")  # send user as an object
            self.my_writer_obj.flush()

            # ToDO! check if email and nickname are unique
            answer = self.my_writer_obj.readline().rstrip("\n")

            if (answer != "VALID"):
                if (answer == "EMAILBUSY"):
                    messagebox.showwarning("Duplicate!", "Email is already in use\nPlease try again.")
                    self.hide_register_window()
                    self.Register()
                elif (answer == "NCKNAMEBUSY"):
                    messagebox.showwarning("Duplicate", "Nickname is already in use\nPlease try again.")
                    self.hide_register_window()
                    self.Register()
                return False
            else:
                Window.ACTIVE_USERS.append(nickName) #if reg is OK the user will be added to the chatroom
                self.chatwindow()

        else:
            messagebox.showinfo("Warning!", "password does not match.\nPlease try again.")

    def checkLogin(self):
        nickname = self.entryNickname.get()
        password = self.entryPassword.get()
        self.my_writer_obj.write("CHECKLOGIN\n")
        self.my_writer_obj.write(nickname+"\n")
        self.my_writer_obj.write(password+"\n")
        self.my_writer_obj.flush()
        # self.my_writer_obj.write("GO\n")

        # Todo! check if login is correct
        anwser = self.my_writer_obj.readline().rstrip("\n")
        if(anwser != "OK"):
            messagebox.showwarning("Wrong Credentials!", "your login credentials are incorrect\nPlease try again")
        else:
            Window.ACTIVE_USERS.append(nickname)
            self.chatwindow()





    def chatwindow(self, master=None):
        if Window.register: #if a new user register we first need to check database & password.
            self.hide_register_window()
        else:
            self.hide_login_window()
        # self.listening()

        # set up chat list
        self.gui_userlist = Listbox(self.Frame1)
        self.gui_userlist.pack(side="left", expand=3, fill="both")
        self.userlist_scrollbar = Scrollbar(self.Frame1, orient="vertical")
        self.userlist_scrollbar.config(command=self.gui_userlist.yview)
        self.userlist_scrollbar.pack(side="left", fill="both")
        self.gui_userlist.config(yscrollcommand=self.userlist_scrollbar.set)
        self.gui_userlist.insert(0,Window.ACTIVE_USERS)

        # Logout
        self.logOut = Button(self.Frame2, text="logOut", command=self.close_connection)

        self.logOut.grid(row=0, column=0, columnspan=2, sticky=N+S+E+W)


        # set up chat panel
        self.chat = Text(self.Frame3)
        self.chat.pack(side="left", expand=1, fill="both")
        self.chat_scrollbar = Scrollbar(self.Frame3, orient="vertical")
        self.chat_scrollbar.config(command=self.chat.yview)
        self.chat_scrollbar.pack(side="left", fill="both")
        self.chat.config(yscrollcommand=self.chat_scrollbar.set)

        # set up message input
        self.Frame4 = Frame(master)
        self.Frame4.grid(row=3, column=1, rowspan=1, columnspan=2, sticky=W + E + N + S)
        self.msg = Entry(self.Frame4)
        self.msg.bind("<Return>", self.enterPressed  )
        self.msg.pack(side="left", expand=1, fill="both")



    def enterPressed(self, event):
        # self.listening()
        self.send_msg(Window.ACTIVE_USERS[0],event.widget.get())
        # Todo! threading listing needs to start earlier
        t = Thread(target=self.listening)
        t.start()



    def cancel(self): # user want to go back to home screen
        if Window.register:
            self.labelName.grid_forget()
            self.entryName.grid_forget()
            self.labelNick.grid_forget()
            self.entryNick.grid_forget()
            self.labelnewEmail.grid_forget()
            self.entrynewEmail.grid_forget()
            self.labelPassword1.grid_forget()
            self.entryPassword1.grid_forget()
            self.labelPassword2.grid_forget()
            self.entryPassword2.grid_forget()
            self.buttonReg.grid_forget()
            self.buttonCancel.grid_forget()

            Window.register = False
        else:
            self.labelNickname.grid_forget()
            self.labelNickname.grid_forget()
            self.labelPassword.grid_forget()
            self.entryPassword.grid_forget()
            self.buttonChatroom.grid_forget()
            self.buttonCancel.grid_forget()

        self.init_window()


    def __del__(self):
        self.close_connection()

    def prompt(self, msg):
        self.chat.insert(END, msg+"\n" )



    def send_msg(self, usr, msg):

        self.my_writer_obj.write("MSG\n")
        self.my_writer_obj.write(usr+"\n")
        self.my_writer_obj.write(msg+"\n")
        self.my_writer_obj.flush()






    def makeConnectionWithServer(self):
        try:
            logging.info("Making connection with server...")
            host = socket.gethostname()
            port = 9999
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host,port))
            self.my_writer_obj = self.s.makefile(mode='rw')
            logging.info("open connection with server succesfully")
            # self.listening()
        except ConnectionRefusedError as C:
            logging.error("Connection refused: %s"%C)


    def close_connection(self):
        try:
            logging.info("Close connection with server...")
            self.my_writer_obj.write("%s\n"%"CLOSE")
            self.my_writer_obj.flush()
            self.s.close()
        except Exception as ex:
            logging.error("Exception occurd: %s" % ex)
            messagebox.showinfo("Chatroom", "Something has gone wrong...")


    def listening(self):
        # waiting for a anwser
        while 1:
            anwser = self.s.recv(1024)
            if anwser:
                self.prompt(anwser.decode())
            else:
                logging.warning("No data returned from the server")


root = Tk()
app = Window(root)
root.mainloop()