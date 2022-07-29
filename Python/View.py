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
import RPi.GPIO as GPIO

# Creates main GUI window and its subframe for data to be displayed
root = Tk()
root.wm_title("MicroDev Tester")
root.attributes('-fullscreen', True)
root.configure(background="black")
frame = Frame(root)
frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
frame.configure(background="black")


def setStandbyScreen():
    # Clears main window's subframe
    for widget in frame.winfo_children():
        if widget.winfo_exists():
            widget.destroy()
    frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
    
    subframe = Frame(frame)
    subframe.configure(background="black", highlightbackground="white", highlightcolor="white", highlightthickness=5)
    report = Text(subframe, width=100, height=100, wrap=NONE, background='black', font=("Helvetica", 40), fg="green", padx=10, pady=10)
    report.insert(END, "Place dev board onto header\n")
    report.insert(END, "interface and connect cable\n")

    leftButton = Label(frame, text="", background='black', font=("Helvetica", 40), fg="green", highlightthickness=5)
    leftButton.config(highlightbackground="white", highlightcolor="white")
    middleButton = Label(frame, text="Shutdown", background='black', font=("Helvetica", 40), fg="green", highlightthickness=5)
    middleButton.config(highlightbackground="white", highlightcolor="white")
    rightButton = Label(frame, text="", background='black', font=("Helvetica", 40), fg="green", highlightthickness=5)
    rightButton.config(highlightbackground="white", highlightcolor="white")
    
    subframe.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=0.75)
    report.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)

    leftButton.place(relx=0.025, rely=0.775, relheight=0.2, relwidth=0.3)
    middleButton.place(relx=0.35, rely=0.775, relheight=0.2, relwidth=0.3)
    rightButton.place(relx=0.675, rely=0.775, relheight=0.2, relwidth=0.3)

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
    leftButton = Label(frame, text="", background='black', font=("Helvetica", 40))
    middleButton = Label(frame, text="", background='black', font=("Helvetica", 40))
    rightButton = Label(frame, text="", background='black', font=("Helvetica", 40))

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


def setDetailTestScreen(detailed_report):
    # Clears main window's subframe
    for widget in frame.winfo_children():
        if widget.winfo_exists():
            widget.destroy()
    frame.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
    
    # Creates scrolling subframe and button icons
    subframe = Frame(frame)
    subframe.configure(background="black", highlightbackground="white", highlightcolor="white", highlightthickness=5)
    leftButton = Label(frame, text="Page Down", background='black', font=("Helvetica", 40), fg="green", highlightthickness=5)
    leftButton.config(highlightbackground="white", highlightcolor="white")
    middleButton = Label(frame, text="Next", background='black', font=("Helvetica", 40), fg="green", highlightthickness=5)
    middleButton.config(highlightbackground="white", highlightcolor="white")
    rightButton = Label(frame, text="Page Up", background='black', font=("Helvetica", 40), fg="green", highlightthickness=5)
    rightButton.config(highlightbackground="white", highlightcolor="white")
    
    subframe.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=0.75)
    leftButton.place(relx=0.025, rely=0.775, relheight=0.2, relwidth=0.3)
    middleButton.place(relx=0.35, rely=0.775, relheight=0.2, relwidth=0.3)
    rightButton.place(relx=0.675, rely=0.775, relheight=0.2, relwidth=0.3)
    
     # Initializes variables used for indexing through array for scrolling
    button_press = None
    current_page = 0
    page_size = 5
    num_pages = int(len(detailed_report) / page_size)
    if((len(detailed_report) % page_size) == 0):
        num_pages -= 1
        
     # Displays first page worth of entries
    report = Text(subframe, width=100, height=100, wrap=NONE, background='black', font=("Helvetica", 40), fg="green", padx=10, pady=10)
    for i in range(len(detailed_report)):
        if i < current_page * page_size:
            continue
        elif i > ((current_page * page_size) + page_size) - 1:
            continue
        else:
            report.insert(END, str(detailed_report[i]))
    report.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
    
    # Updates main window
    root.update()
    
     # Continues to allow for scrolling by polling buttons until center button is pressed
    while button_press != "center":
        
        # Blocking call that waits for next button press and stores it
        button_press = pollButtons()
        
         # Increments variables used to index for scrolling
        if button_press == "right" and current_page < num_pages:
            current_page += 1
        elif button_press == "left" and current_page > 0:
            current_page -= 1
        else:
            continue
            
         # Wipes out previous entires from subframe
        for widget in subframe.winfo_children():
            if widget.winfo_exists():
                widget.destroy()
        subframe.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=0.75)
        
         # Creates new entries to go in subframe that acts like scrolling to next page
        report = Text(subframe, width=100, height=100, wrap=NONE, font=("Helvetica", 40), background='black', fg="green", padx=10, pady=10)
        for i in range(len(detailed_report)):
            if i < current_page * page_size:
                continue
            elif i > ((current_page * page_size) + page_size) - 1:
                continue
            else:
                report.insert(END, detailed_report[i])
        report.place(relx=0.0, rely=0.0, relwidth=1.0, relheight=1.0)
        
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


def pollButtons():
    
    # Initializes GPIO button for polling
    BTN_L = 14
    BTN_C = 15
    BTN_R = 18
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup([BTN_L, BTN_C, BTN_R], GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Waits until user presses button
    while GPIO.input(BTN_L) and GPIO.input(BTN_C) and GPIO.input(BTN_R):
        continue
        
     # Returns string for which button was pressed and waits until the user lets go
    if not GPIO.input(BTN_L):
        while not GPIO.input(BTN_L):
            continue
        return "left"
    elif not GPIO.input(BTN_C):
        while not GPIO.input(BTN_C):
            continue
        return "center"
    elif not GPIO.input(BTN_R):
        while not GPIO.input(BTN_R):
            continue
        return "right"
    else:    
        return None