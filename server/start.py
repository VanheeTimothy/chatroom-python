from tkinter import *
from gui_server import ServerWindow

def callback():
    print("callback")
    gui_server.afsluiten_server()
    root.destroy()

root = Tk()
root.geometry("600x500")
gui_server = ServerWindow(root)
root.protocol("WM_DELETE_WINDOW", callback)
root.mainloop()
