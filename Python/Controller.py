# #################################################
# MicroDev Project: Controller
# Date: May 2, 2022
# Description: Controller Class
# Authors:
# Nathan Hanchey
# Dylan
# Connor
# Corey
# #################################################

from time import sleep
import Model
import View


###################################################################################
class Controller:
    driver = None
    view = None

    def __init__(self):
        print("init")

    #
    def init_model(self, view, driver):
        print("model")
        self.view = view
        self.driver = driver
        return None

    #
    def wait_model(self):
        print("wait")
        return None

    #
    def display_model(self):
        print("display")
        self
        return None


# ###############################################################################
# MAIN LOOP
# ###############################################################################
controller = Controller
view = View
model = Model


# Initialize
# controller.controller_init(controller, model, view, driver)
# model.init_model(model, view, driver)
while True:

    # Wait for Subject Board Connection / Shutdown Screen
    # Check Board Type | Save Variable
    cont = 1
    while cont == 1:
        board_type = model.board_list()
        if board_type == "No Boards Detected" or board_type == "Overflow":
            cont = 1
        else:
            cont = 0
            print(board_type)

    # Start Menu Screen Function
    start = True

    # Start Test Condition
    # Loop Through Config File
    # Test Conditions In Loop
    if start:
        if board_type == "Arduino Uno Detected":
            model.subject_flash(board_type)
            val = model.serial_setup()
            count = 0
            while val != 1 and count < 5:
                val = model.serial_setup()
                count = count + 1

            if count < 5:
                # Read Config | Loop Through Tests
                # Using readlines()
                file1 = open('unoTest.config', 'r')
                Lines = file1.readlines()
                print(Lines[1])



    # End of Test Screen
    # Save Condition States
    # Detailed Results State
    # Remove Board State

    # Loop
    print("Flash")
    sleep(5)


