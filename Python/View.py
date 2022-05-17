# #################################################
# MicroDev Project: View
# Date: May 2, 2022
# Description: View Class
# Authors:
# Nathan Hanchey
# Dylan
# Connor
# Corey
# #################################################

import threading
import time
from tkinter import *


class View:
    def __init__(self):
        # Creates main GUI window and its subframe for data to be displayed
        self.root = Tk()
        self.root.wm_title("MicroDev Tester")
        self.frame = Frame(self.root)
        self.frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

    def setStandbyScreen(self):
        # Clears main window's subframe
        for widget in self.frame.winfo_children():
            if widget.winfo_exists():
                widget.destroy()
        self.frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

        # Initializes labels to display info to user
        self.standbyMsg = Label(self.frame, text="Place dev board onto header interface and connect cable", font=("Helvetica", 14))
        self.leftButton = Label(self.frame, text="", background='grey', font=("Helvetica", 14))
        self.middleButton = Label(self.frame, text="Shutdown", background='blue', font=("Helvetica", 14))
        self.rightButton = Label(self.frame, text="", background='grey', font=("Helvetica", 14))

        # Controls placement of labels that display info to user
        self.standbyMsg.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.8)
        self.leftButton.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.2)
        self.middleButton.place(relx=0.4, rely=0.7, relheight=0.2, relwidth=0.2)
        self.rightButton.place(relx=0.7, rely=0.7, relheight=0.2, relwidth=0.2)

        # Updates main window
        view.root.update()

    def setStartScreen(self):
        # Clears main window's subframe
        for widget in self.frame.winfo_children():
            if widget.winfo_exists():
                widget.destroy()
        self.frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

        # Initializes labels to display info to user
        self.standbyMsg = Label(self.frame, text="Your dev board has been detected", font=("Helvetica", 14))
        self.leftButton = Label(self.frame, text="", background='grey', font=("Helvetica", 14))
        self.middleButton = Label(self.frame, text="Start Test", background='green', font=("Helvetica", 14))
        self.rightButton = Label(self.frame, text="", background='grey', font=("Helvetica", 14))

        # Controls placement of labels that display info to user
        self.standbyMsg.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.8)
        self.leftButton.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.2)
        self.middleButton.place(relx=0.4, rely=0.7, relheight=0.2, relwidth=0.2)
        self.rightButton.place(relx=0.7, rely=0.7, relheight=0.2, relwidth=0.2)

        # Updates main window
        view.root.update()

    # def setRunningScreen(self):
    #
    # def setShutdownScreen(self):


# Used to run the View module independently for testing purposes
if __name__ == '__main__':
    view = View()
    view.setStandbyScreen()
    time.sleep(5)
    view.setStartScreen()
    while 1:
        continue

