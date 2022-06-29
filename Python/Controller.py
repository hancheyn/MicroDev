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

view = View
model = Model

###################################################################################


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
    return None


# Description: For looping through serial check if communication works
# Returns True only if serial communication is established
def serial_check():
    # While Loop Confirms Serial Connection
    val = model.serial_setup()
    count = 0
    while val != 1 and count < 5:
        val = model.serial_setup()
        count = count + 1
    if count < 5:
        return True
    return False


# Description: Preforms Test Comparisons
# Parameters: Test ID Int | Pin ID Int | Address Int | Enable Int | Board type String
# Returns: Boolean Pass or Fail
def subject_test(t, p, a, e, board):

    # Gather Config Data from Config file of board type
    if board == "Arduino Uno Detected":
        file2 = open('unoThreshold.config', 'r')
    elif board == "STM32F446 Detected":
        file2 = open('stm32f4Threshold.config', 'r')
    else:
        return False

    lines2 = file2.readlines()

    # Run tests and compare based on test configured values
    if t == 1:
        print("Test 1")
        compare = lines2[1].split(",")

        # Read adc value of logic high from micro
        high = model.run_subject_test(p, e, a, t, 1)

        # Read adc value of logic low from micro
        low = model.run_subject_test(p, e, a, t, 0)

        # Compare to Config threshold and Return Pass or Fail Boolean
        if float(compare[1]) < high and float(compare[2]) > low:
            return True
        return False

    elif t == 2:
        print("Test 2")
        compare = lines2[2].split(",")

        # Read adc value of logic high from micro
        high = model.run_subject_test(p, e, a, t, 1)

        # Read adc value of logic low from micro
        low = model.run_subject_test(p, e, a, t, 0)

        # Compare to Config threshold and Return Pass or Fail Boolean
        if float(compare[1]) < high and float(compare[2]) > low:
            return True
        return False

    elif t == 3:
        print("Test 3")
        return False

    elif t == 4:
        print("Test 3")
        return False

    elif t == 5:
        print("Test 3")
        return False

    elif t == 6:
        print("Test 3")
        return False

    elif t == 7:
        print("Test 3")
        return False

    elif t == 8:
        print("Test 3")
        return False

    return False


# ###############################################################################
# MAIN LOOP
# ###############################################################################

# Facade Macro
Facade = 0

# Initialize
# controller.controller_init(controller, model, view, driver)
# model.init_model(model, view, driver)
while True:

    # Wait for Subject Board Connection / Shutdown Screen
    # Check Board Type | Save Variable | Blocking Loop
    # FIX: MOVE TO MODEL // OR ADD BUTTON CONDITION
    cont = 1
    board_type = model.board_list()
    while cont == 1:
        board_type = model.board_list()
        if board_type == "No Boards Detected" or board_type == "Overflow":
            cont = 1
        else:
            cont = 0
            print(board_type)
    #################

    # Start Menu Screen Function
    # FIX: States Controlled by View?
    start = True

    # Start Test Condition
    # Loop Through Config File
    # Test Conditions In Loop
    # FIX MOVE START TEST to FUNCTION?
    if start:

        model.subject_flash(board_type)

        # While Loop Confirms Serial Connection
        if serial_check():
            # Read Config | Loop Through Tests
            # Using readlines()
            if board_type == "Arduino Uno Detected":
                file1 = open('unoTest.config', 'r')
            elif board_type == "STM32F411 Detected" or board_type == "STM32F446 Detected":
                file1 = open('stm32f4Test.config', 'r')

            else:
                file1 = open('unoTest.config', 'r')
            Lines = file1.readlines()
            test_count = len(Lines)
            loop_count = 1

            # Facade ?
            if Facade == 1:
                print("Facade")

            res = [False for i in range(test_count-1)]
            # Loop until end of file line array
            while loop_count < test_count:
                print(Lines[loop_count])
                test = Lines[loop_count].split(",")
                # res[loop_count-1] = subject_test(int(test[0]), int(test[1]), int(test[2]), int(test[3]), board_type)
                # print(res[loop_count-1])
                loop_count = loop_count + 1

    # End of Test Screen
    # Save Condition States
    # Detailed Results State
    # Remove Board State

    # Loop
    print("Flash")
    sleep(5)


