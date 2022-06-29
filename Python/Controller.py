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
# Returns: True only if serial communication is established
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


# Description: Opens Test Sequence File
# Returns: Test File
def test_config_file(_board_type):
    if _board_type == "Arduino Uno Detected":
        file = open('unoTest.config', 'r')
    elif _board_type == "STM32F411 Detected" or _board_type == "STM32F446 Detected":
        file = open('stm32f4Test.config', 'r')
    else:
        file = open('unoTest.config', 'r')

    return file


# Description: Preforms Test Comparisons
# Parameters: Test ID Int | Pin ID Int | Address Int | Enable Int | Board type String
# Returns: Boolean Pass or Fail
def subject_test(t, p, a, e, board, _ser):

    # Logic Level Config
    logic = 0

    # Gather Config Data from Config file of board type
    if board == "Arduino Uno Detected":
        file2 = open('unoThreshold.config', 'r')
        logic = 5
    elif board == "STM32F411 Detected" or board == "STM32F446 Detected":
        file2 = open('stm32f4Threshold.config', 'r')
        logic = 3.3
    else:
        return False

    lines2 = file2.readlines()

    # Run tests and compare based on test configured values
    if t == 1:
        print("Test 1")
        compare = lines2[1].split(",")

        # Read adc value of logic high from micro
        high = model.run_subject_test(p, e, a, t, 1, _ser)

        # Read adc value of logic low from micro
        low = model.run_subject_test(p, e, a, t, 0, _ser)

        # Compare to Config threshold and Return Pass or Fail Boolean
        if float(compare[1]) < high and float(compare[2]) > low:
            return True
        return False

    elif t == 2:
        print("Test 2")
        compare = lines2[2].split(",")

        # Read adc value of logic high from micro
        high = model.run_subject_test(p, e, a, t, 1, _ser)

        # Read adc value of logic low from micro
        low = model.run_subject_test(p, e, a, t, 0, _ser)

        # Compare to Config threshold and Return Pass or Fail Boolean
        if float(compare[1]) < high and float(compare[2]) > low:
            return True
        return False

    elif t == 3:
        print("Test 3")

        # Read adc value at threshold voltage
        # Instruction depends on logic level (controls dac)
        if logic == 5:
            adc3 = model.run_subject_test(p, e, a, t, 0x0F, _ser)
        else:
            adc3 = model.run_subject_test(p, e, a, t, 0x0A, _ser)

        # calculation with adc to pull down resistance value
        print("test adc: ")
        print(adc3)
        return False

    elif t == 4:
        print("Test 4")

        # Read adc value at threshold voltage
        if logic == 5:
            adc4 = model.run_subject_test(p, e, a, t, 0x0F, _ser)
        else:
            adc4 = model.run_subject_test(p, e, a, t, 0x0A, _ser)

        # calculation with adc to pull down resistance value
        print("test adc: ")
        print(adc4)
        return False

    elif t == 5:
        print("Test 5")

        # Read digital pin from subject board
        if logic == 5:
            subject_input_high = model.run_subject_test(p, e, a, t, 0x0F, _ser)
        else:
            subject_input_high = model.run_subject_test(p, e, a, t, 0x0A, _ser)

        # Read Digital Pin Low
        subject_input_low = model.run_subject_test(p, e, a, t, 0, _ser)
        print(subject_input_high)

        if 1 == subject_input_high and 0 == subject_input_low:
            return True
        return False

    elif t == 6:
        print("Test 6")
        compare = lines2[t].split(",")

        test_num = 1
        test_len = len(compare)
        print(test_len)

        condition_success = True

        # Read adc from subject board
        # Instruction is in config
        while test_num < test_len:
            instruct = compare[1]
            subject_adc_high = model.run_subject_test(p, e, a, t, instruct, _ser)
            print(subject_adc_high)

            # convert instruction to voltage

            # compare subject voltage to dac voltage

            test_num = test_num + 1

        if condition_success:
            return True
        return False

    elif t == 7:
        print("Test 7")

        # Reads current
        # Instruction is in config
        current = model.run_subject_test(p, e, a, t, 0, _ser)

        # compare subject current to threshold

        return False

    elif t == 8:
        print("Test 8")

        # Reads current
        # Instruction is in config
        current = model.run_subject_test(p, e, a, t, 0, _ser)

        # compare subject current to threshold

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
    board_type = model.board_wait()

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
            file1 = test_config_file(board_type)
            Lines = file1.readlines()
            test_count = len(Lines)
            loop_count = 1

            # Facade ?
            if Facade == 1:
                print("Facade")

            res = [False for i in range(test_count-1)]

            # Loop until end of file line array | Open Serial
            ser = model.open_serial()
            sleep(2)

            while loop_count < test_count:
                print(Lines[loop_count])
                test = Lines[loop_count].split(",")
                res[loop_count-1] = subject_test(int(test[0]), int(test[1]), int(test[2]), int(test[3]), board_type, ser)
                # print(res[loop_count-1])
                loop_count = loop_count + 1
                sleep(0.01)

            # Close Serial Port
            model.close_serial(ser)

    # End of Test Screen
    # Save Condition States
    # Detailed Results State
    # Remove Board State

    # Loop
    print("Flash")
    sleep(5)


