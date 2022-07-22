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

import os
import threading
import time
from tkinter import *

# Creates main GUI window and its subframe for data to be displayed
root = Tk()
root.wm_title("MicroDev Tester")
frame = Frame(root)
root.attributes('-fullscreen', True)
frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)


def __init__():
    # Creates main GUI window and its subframe for data to be displayed
    root = Tk()
    root.wm_title("MicroDev Tester")
    frame = Frame(root)
    frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)


def setStandbyScreen():
    # Clears main window's subframe
    for widget in frame.winfo_children():
        if widget.winfo_exists():
            widget.destroy()
    frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

    # Initializes labels to display info to user
    standbyMsg = Label(frame, text="Place dev board onto header", font=("Helvetica", 40))
    standbyMsg2 = Label(frame, text="interface and connect cable", font=("Helvetica", 40))
    leftButton = Label(frame, text="", background='grey', font=("Helvetica", 40))
    middleButton = Label(frame, text="Shutdown", background='red', font=("Helvetica", 40))
    rightButton = Label(frame, text="", background='grey', font=("Helvetica", 40))

    # Controls placement of labels that display info to user
    standbyMsg.place(relx=0.1, rely=0.3, relheight=0.1, relwidth=0.8)
    standbyMsg2.place(relx=0.1, rely=0.4, relheight=0.1, relwidth=0.8)
    leftButton.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.2)
    middleButton.place(relx=0.4, rely=0.7, relheight=0.2, relwidth=0.2)
    rightButton.place(relx=0.7, rely=0.7, relheight=0.2, relwidth=0.2)

    # Updates main window
    root.update()


def setStartScreen():
    # Clears main window's subframe
    for widget in frame.winfo_children():
        if widget.winfo_exists():
            widget.destroy()
    frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

    # Initializes labels to display info to user
    standbyMsg = Label(frame, text="Your dev board has been detected", font=("Helvetica", 40))
    leftButton = Label(frame, text="", background='grey', font=("Helvetica", 40))
    middleButton = Label(frame, text="Start Test", background='green', font=("Helvetica", 40))
    rightButton = Label(frame, text="", background='grey', font=("Helvetica", 40))

    # Controls placement of labels that display info to user
    standbyMsg.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.8)
    leftButton.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.2)
    middleButton.place(relx=0.4, rely=0.7, relheight=0.2, relwidth=0.2)
    rightButton.place(relx=0.7, rely=0.7, relheight=0.2, relwidth=0.2)

    # Updates main window
    root.update()


def setFlashScreen():
    # Clears main window's subframe
    for widget in frame.winfo_children():
        if widget.winfo_exists():
            widget.destroy()
    frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

    # Initializes labels to display info to user
    standbyMsg = Label(frame, text="Flashing Software to Subject Board", font=("Helvetica", 40))
    leftButton = Label(frame, text="", background='grey', font=("Helvetica", 40))
    middleButton = Label(frame, text="", background='grey', font=("Helvetica", 40))
    rightButton = Label(frame, text="", background='grey', font=("Helvetica", 40))

    # Controls placement of labels that display info to user
    standbyMsg.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.8)
    leftButton.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.2)
    middleButton.place(relx=0.4, rely=0.7, relheight=0.2, relwidth=0.2)
    rightButton.place(relx=0.7, rely=0.7, relheight=0.2, relwidth=0.2)

    # Updates main window
    root.update()


def setRunningScreen(pass_array):
    # Clears main window's subframe
    for widget in frame.winfo_children():
        if widget.winfo_exists():
            widget.destroy()
    frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

    # Initializes labels to display info to user
    standbyMsg = Label(frame, text=pass_array, font=("Helvetica", 40))

    leftButton = Label(frame, text="", background='grey', font=("Helvetica", 40))
    middleButton = Label(frame, text="", background='grey', font=("Helvetica", 40))
    rightButton = Label(frame, text="", background='grey', font=("Helvetica", 40))

    # Controls placement of labels that display info to user
    standbyMsg.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.8)
    leftButton.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.2)
    middleButton.place(relx=0.4, rely=0.7, relheight=0.2, relwidth=0.2)
    rightButton.place(relx=0.7, rely=0.7, relheight=0.2, relwidth=0.2)

    # Updates main window
    root.update()


def setResultsScreen(pass_array):
    # Clears main window's subframe
    for widget in frame.winfo_children():
        if widget.winfo_exists():
            widget.destroy()
    frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

    # Initializes labels to display info to user

    standbyMsg = Label(frame, text=pass_array, font=("Helvetica", 14))
    leftButton = Label(frame, text="Save", background='green', font=("Helvetica", 40))
    middleButton = Label(frame, text="Details", background='red', font=("Helvetica", 40))
    rightButton = Label(frame, text="New Test", background='blue', font=("Helvetica", 40))

    # Controls placement of labels that display info to user
    standbyMsg.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.8)
    leftButton.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.2)
    middleButton.place(relx=0.4, rely=0.7, relheight=0.2, relwidth=0.2)
    rightButton.place(relx=0.7, rely=0.7, relheight=0.2, relwidth=0.2)

    # Updates main window
    root.update()


def setDetailTestScreen(detailed_array):
    # Clears main window's subframe
    for widget in frame.winfo_children():
        if widget.winfo_exists():
            widget.destroy()
    frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

    # Initializes labels to display info to user
    standbyMsg = Label(frame, text=detailed_array, font=("Helvetica", 40))

    leftButton = Label(frame, text="Save", background='green', font=("Helvetica", 40))
    middleButton = Label(frame, text="", background='grey', font=("Helvetica", 40))
    rightButton = Label(frame, text="Back", background='red', font=("Helvetica", 40))

    # Controls placement of labels that display info to user
    standbyMsg.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.8)
    leftButton.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.2)
    middleButton.place(relx=0.4, rely=0.7, relheight=0.2, relwidth=0.2)
    rightButton.place(relx=0.7, rely=0.7, relheight=0.2, relwidth=0.2)

    # Updates main window
    root.update()


def setSaveScreen():
    # Clears main window's subframe
    for widget in frame.winfo_children():
        if widget.winfo_exists():
            widget.destroy()
    frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

    # Initializes labels to display info to user
    standbyMsg = Label(frame, text="Saved Test Results to USB", font=("Helvetica", 40))

    leftButton = Label(frame, text="", background='grey', font=("Helvetica", 40))
    middleButton = Label(frame, text="", background='grey', font=("Helvetica", 40))
    rightButton = Label(frame, text="Back", background='green', font=("Helvetica", 40))

    # Controls placement of labels that display info to user
    standbyMsg.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.8)
    leftButton.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.2)
    middleButton.place(relx=0.4, rely=0.7, relheight=0.2, relwidth=0.2)
    rightButton.place(relx=0.7, rely=0.7, relheight=0.2, relwidth=0.2)

    # Updates main window
    root.update()


#
def setShutdownScreen():
    # Clears main window's subframe
    for widget in frame.winfo_children():
        if widget.winfo_exists():
            widget.destroy()
    frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

    # Initializes labels to display info to user
    standbyMsg = Label(frame, text="Shutdown in Progress", font=("Helvetica", 40))
    leftButton = Label(frame, text="", background='grey', font=("Helvetica", 40))
    middleButton = Label(frame, text="", background='grey', font=("Helvetica", 40))
    rightButton = Label(frame, text="", background='grey', font=("Helvetica", 40))

    # Controls placement of labels that display info to user
    standbyMsg.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.8)
    leftButton.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.2)
    middleButton.place(relx=0.4, rely=0.7, relheight=0.2, relwidth=0.2)
    rightButton.place(relx=0.7, rely=0.7, relheight=0.2, relwidth=0.2)

    # Updates main window
    root.update()


#
def setRemovalScreen():
    # Clears main window's subframe
    for widget in frame.winfo_children():
        if widget.winfo_exists():
            widget.destroy()
    frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)

    # Initializes labels to display info to user
    standbyMsg = Label(frame, text="Please remove your DevBoard", font=("Helvetica", 40))
    leftButton = Label(frame, text="", background='grey', font=("Helvetica", 40))
    middleButton = Label(frame, text="", background='grey', font=("Helvetica", 40))
    rightButton = Label(frame, text="", background='grey', font=("Helvetica", 40))

    # Controls placement of labels that display info to user
    standbyMsg.place(relx=0.1, rely=0.3, relheight=0.2, relwidth=0.8)
    leftButton.place(relx=0.1, rely=0.7, relheight=0.2, relwidth=0.2)
    middleButton.place(relx=0.4, rely=0.7, relheight=0.2, relwidth=0.2)
    rightButton.place(relx=0.7, rely=0.7, relheight=0.2, relwidth=0.2)

    # Updates main window
    root.update()


# Used to run the View module independently for testing purposes
if __name__ == '__main__':
    os.fork()
    while True:
        continue
