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


from tkinter import *

class View:
    def __init__(self):
        self.root = Tk()
        self.root.wm_title("MicroDev Tester")
        self.root.mainloop()

# Used to run the View module independently for testing purposes
if __name__ == '__main__':
    view = View()

