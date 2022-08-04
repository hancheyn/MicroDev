# ----------------------------------------------------------------------
# MicroDev Project: Controller
# Date: May 2, 2022
# Description: Controller Class
# This module contains opens and utilizes configuration files as well as
# compares configuration thresholds to tests to pass to the View GUI
# Authors:
# Nathan Hanchey
# Dylan Vetter
# Connor Inglet
# Corey Noura
# ----------------------------------------------------------------------

from time import sleep
import subprocess
import Model
import View

view = View
model = Model

"""
Debug File 
"""
Debug_file = open("Debug_MicroDevTest.txt", "w")
Debug_file.close()


"""
Test ID Mapping Key
"""
test_map = {1: 'Output Test', 2: 'Output Load Test', 3: 'Pull Up Test' 
    , 4: 'Pull Down Test', 5: 'Input Logic Test', 6: 'ADC Test', 
    7: 'Sleep Test', 8: 'Wakeup Pin Test', 9: 'Reset Board'}

"""
STM Nucleo Mapping Key
"""
stm_pinmap = {1: 'PD2', 2: 'PC12', 3: 'PC11', 4: 'PC10', 5: 'PB8'
    , 6: 'PC6', 7: 'PC9', 8: 'PC8', 9: 'IOREF', 10: 'BOOT0', 11: 'E5V'
    , 12: 'VDD', 13: 'AVDD', 14: 'U5V', 15: 'PB9', 16: 'PC5', 17: 'PA14'
    , 18: '3V3', 19: 'PA13', 20: 'RESET', 21: 'PA6', 22: 'PA11'
    , 23: 'PA5', 24: 'PA12', 25: 'PC13', 26: 'PB7', 27: 'PA15', 28: '5V'
    , 29: 'PB2', 30: 'PB6', 31: 'PB12', 32: 'PA7', 33: 'PC15', 34: 'PA0'
    , 35: 'PC14', 36: 'VIN', 37: 'PA8', 38: 'PB1', 39: 'PA9', 40: 'PC7'
    , 41: 'PH1', 42: 'PA4', 43: 'PH0', 44: 'PA1', 45: 'PB4', 46: 'PB14'
    , 47: 'PB10', 48: 'PB15', 49: 'PC2', 50: 'PC1', 51: 'VBAT',  52: 'PB0'
    , 53: 'PB3', 54: 'AGND', 55: 'PB5', 56: 'PB13', 57: 'PC3', 58: 'PC0'
    , 59: 'PA3', 60: 'PA2', 61: 'PA10', 62: 'PC4'}

"""
Arduino Uno Mapping Key
"""
arduino_pinmap = {1: 'None', 2: 'None', 3: 'None', 4: 'None', 5: 'SCL'
    , 6: 'None', 7: 'None', 8: 'None', 9: 'IOREF', 10: 'None', 11: 'None'
    , 12: 'VDD', 13: 'AVDD', 14: 'None', 15: 'SDA', 16: 'None', 17: 'None'
    , 18: '3V3', 19: 'None', 20: 'RESET', 21: 'D12', 22: 'None'
    , 23: 'D13', 24: 'None', 25: 'None', 26: 'None', 27: 'None', 28: '5V'
    , 29: 'None', 30: 'D10', 31: 'None', 32: 'D11', 33: 'None', 34: 'A0'
    , 35: 'None', 36: 'VIN', 37: 'D7', 38: 'None', 39: 'D8', 40: 'D9'
    , 41: 'None', 42: 'A2', 43: 'None', 44: 'A1', 45: 'D5', 46: 'None'
    , 47: 'D6', 48: 'None', 49: 'None', 50: 'A4', 51: 'VBAT',  52: 'A3'
    , 53: 'D3', 54: 'None', 55: 'D4', 56: 'None', 57: 'None', 58: 'A5'
    , 59: 'D0', 60: 'D1', 61: 'D2', 62: 'None'}

"""
NEW Subject Mapping Key
"""
new_pinmap = {1: 'None', 2: 'None', 3: 'None', 4: 'None', 5: 'None'
    , 6: 'None', 7: 'None', 8: 'None', 9: 'None', 10: 'None', 11: 'None'
    , 12: 'None', 13: 'None', 14: 'None', 15: 'None', 16: 'None', 17: 'None'
    , 18: '3V3', 19: 'None', 20: 'None', 21: 'None', 22: 'None'
    , 23: 'None', 24: 'None', 25: 'None', 26: 'None', 27: 'None', 28: '5V'
    , 29: 'None', 30: 'None', 31: 'None', 32: 'None', 33: 'None', 34: 'None'
    , 35: 'None', 36: 'None', 37: 'None', 38: 'None', 39: 'None', 40: 'None'
    , 41: 'None', 42: 'None', 43: 'None', 44: 'None', 45: 'None', 46: 'None'
    , 47: 'None', 48: 'None', 49: 'None', 50: 'None', 51: 'None',  52: 'None'
    , 53: 'None', 54: 'None', 55: 'None', 56: 'None', 57: 'None', 58: 'None'
    , 59: 'None', 60: 'None', 61: 'None', 62: 'None'}

"""
Configuration Getters:
The following functions grab important configuration data for 
the test cycle of the subject board.
"""


# ----------------------------------------------------------------------
# Description: For looping through serial check if communication works
# Returns: True only if serial communication is established
# ----------------------------------------------------------------------
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


# ----------------------------------------------------------------------
# Description: Opens Test Sequence File
# Returns: Test File
# ----------------------------------------------------------------------
def test_config_file(_board_type):
    """
    New Subject Config
    """
    if _board_type == "Arduino Uno Detected":
        file = open('unoTest.config', 'r')
    elif _board_type == "STM32F411 Detected" or _board_type == "STM32F401 Detected" or _board_type == "STM32F446 Detected":
        file = open('stm32f4Test.config', 'r')
    else:
        file = open('unoTest.config', 'r')
    
    Lines = file.readlines()

    return Lines


# ----------------------------------------------------------------------
# Description: Opens Test Threshold File
# Returns: Threshold File in array of lines
# ----------------------------------------------------------------------
def threshold_config_file(_board_type):
    """
    New Subject Config
    """
    if _board_type == "Arduino Uno Detected":
        file2 = open('unoThreshold.config', 'r')
    elif _board_type == "STM32F411 Detected" or _board_type == "STM32F401 Detected" or _board_type == "STM32F446 Detected":
        file2 = open('stm32f4Threshold.config', 'r')
    else:
        file2 = open('unoThreshold.config', 'r')
    
    lines2 = file2.readlines()
    return lines2
    
    
# ----------------------------------------------------------------------
# Description: Generates Pinmap for Subject Board
# Returns: Pinmap Key Array of Subject Board
# ----------------------------------------------------------------------
def pinmap_array(_board_type):
    """
    New Subject Config
    """
    if _board_type == "Arduino Uno Detected":
        map_pin = arduino_pinmap
    elif _board_type == "STM32F411 Detected" or _board_type == "STM32F401 Detected" or _board_type == "STM32F446 Detected":
        map_pin = stm_pinmap
    else:
        map_pin = stm_pinmap
    
    return map_pin
   
    
# ----------------------------------------------------------------------
# Description: Finds Subject Logic Level
# Returns: Logic Level
# ----------------------------------------------------------------------
def subject_logic(_board_type):
    """
    New Subject Config
    """
    if _board_type == "Arduino Uno Detected":
        logic = 5
    elif _board_type == "STM32F411 Detected" or _board_type == "STM32F401 Detected" or _board_type == "STM32F446 Detected":
        logic = 3.3
    else:
        logic = 5
    return logic
    

# ----------------------------------------------------------------------
# Description: Preforms Test on Supply Pins 3V3 and 5V
# Parameters: board - [type of subject board]
# Returns: Boolean Pass or Fail
# ----------------------------------------------------------------------
def supply_pin_voltages(board):
    # Gather Config Data from Config file of board type
    
    lines2 = threshold_config_file(board)
    logic = subject_logic(board)
    
    #lines2 = file2.readlines()
    compare = lines2[9].split(",")

    if model.check_5V() < float(compare[1]) and model.check_3V3() < float(compare[2]):
        return True
    return False


"""
Individual Pin Tests:
The following function runs a test on a given pin. To do this it must 
access configurations and return a pass fail boolean value.
"""


# ----------------------------------------------------------------------
# Description: Preforms Test Comparisons
# Parameters: Test ID Int | Pin ID Int | Address Int | Enable Int | Board type String
# Returns: Boolean Pass or Fail
# ----------------------------------------------------------------------
def subject_test(t, p, a, e, board, _ser):

    # Debug File
    #global Debug_file
    

    # Logic Level Config
    logic = 0

    # Gather Config Data from Config file of board type

    lines2 = threshold_config_file(board)
    logic = subject_logic(board)

    # Run tests and compare based on test configured values
    if t == 1:
        print("Test 1: Output without Load")
        Debug_file.write("Test 1: Output without Load\n")
        compare = lines2[1].split(",")

        # Read adc value of logic high from micro
        print("Test Logic High")
        high = round(model.run_subject_test(p, e, a, t, 1, _ser), 1)

        # Read adc value of logic low from micro
        print("Test Logic Low")
        low = round(model.run_subject_test(p, e, a, t, 0, _ser), 1)

        Debug_file.write("Test Logic High: " + str(high) + " V\n")
        Debug_file.write("Test Logic Low: " + str(low) + " V\n")
        # Compare to Config threshold and Return Pass or Fail Boolean
        if float(compare[1]) < high and float(compare[2]) > low:
            return True
        return False

    elif t == 2:
        print("Test 2: Output w/ Load")
        Debug_file.write("Test 2: Output w/ Load\n")
        compare = lines2[2].split(",")

        # Read adc value of logic high from micro
        print("Test Logic High")
        high = round(model.run_subject_test(p, e, a, t, 1, _ser), 1)

        # Read adc value of logic low from micro
        print("Test Logic Low")
        low = round(model.run_subject_test(p, e, a, t, 0, _ser), 1)

        Debug_file.write("Test Logic High: " + str(high) + " V\n")
        Debug_file.write("Test Logic Low: " + str(low) + " V\n")
        # Compare to Config threshold and Return Pass or Fail Boolean
        if float(compare[1]) < high and float(compare[2]) > low:
            return True
        return False

    elif t == 3:
        print("Test 3: Pull-Up Input")
        Debug_file.write("Test 3: Pull-Up Input\n")

        compare = lines2[t].split(",")
        adc2 = 0.0
        Rpu = 0.0

        # Read adc value at threshold voltage Pull Up Test
        # Instruction depends on logic level (controls dac)
        adc1 = model.run_subject_test(p, e, a, t, 0x00, _ser)

        if logic == 5:
            adc2 = model.run_subject_test(p, e, a, t, 0x01, _ser)
            if adc2 > 0:
                Rpu = int((((390 * 5) / float(adc2)) - 390))
        else:
            adc2 = model.run_subject_test(p, e, a, t, 0x01, _ser)
            if adc2 > 0:
                Rpu = int((((390 * 3.3) / float(adc2)) - 390))

        # calculation with adc to pull down resistance value
        print("Test adc val: " + str(adc2))
        Debug_file.write("Test Pull Up Resistance Value: " + str(Rpu-(Rpu%1000)) + "\n")
        #Rpu = (((390 * 5) / adc2) - 390)
        if Rpu > float(compare[1]) and Rpu < float(compare[2]) and adc1 > float(compare[3]):
            return True
        return False

    elif t == 4:
        print("Test 4: Pull-Down Input")
        Debug_file.write("Test 4: Pull-Down Input\n")
        compare = lines2[t].split(",")
        adc4 = 0
        Rpd = 0.0

        # Read adc value at threshold voltage
        adc1 = model.run_subject_test(p, e, a, t, 0x00, _ser)

        if logic == 5:
            model.bigfoot.set_vout(5)
            adc4 = round(model.run_subject_test(p, e, a, t, 0x0F, _ser), 1)
            if adc4 != 5:
                Rpd = int((2000 * adc4) / (5 - adc4))
        else:
            model.bigfoot.set_vout(3.3)
            adc4 = round(model.run_subject_test(p, e, a, t, 0x0A, _ser), 1)
            if adc4 != 3.3:
                Rpd = int((2000 * adc4) / (3.3 - adc4))

        # calculation with adc to pull down resistance value
        print("Test adc val: " + str(adc4))
        Debug_file.write("Test Pull Down Resistance Value: " + str(Rpd - (Rpd%1000)) + "\n")
        
        if Rpd > float(compare[1]) and Rpd < float(compare[2]) and adc1 < float(compare[3]):
            return True
        return False

    elif t == 5:
        print("Test 5: Input Logic")
        Debug_file.write("Test 5: Input Logic\n")

        # Read digital pin from subject board
        if logic == 5:
            model.bigfoot.set_vout(5)
            subject_input_high = round(model.run_subject_test(p, e, a, t, 0x0F, _ser), 1)
        else:
            model.bigfoot.set_vout(3.3)
            subject_input_high = round(model.run_subject_test(p, e, a, t, 0x0A, _ser), 1)
            

        # Read Digital Pin Low
        model.bigfoot.set_vout(0)
        subject_input_low = round(model.run_subject_test(p, e, a, t, 0, _ser), 1)
        print("Logic High Val: " + str(subject_input_high))
        Debug_file.write("Logic High: " + str(subject_input_high) + "\n")
        print("Logic Low Val: " + str(subject_input_low))
        Debug_file.write("Logic Low: " + str(subject_input_low) + "\n")

        if 1 == subject_input_high and 0 == subject_input_low:
            return True
        return False

    elif t == 6:
        print("Test 6: ADC Check")
        Debug_file.write("Test 6: ADC Check\n")
        compare = lines2[t].split(",")
        test_num = 1
        test_len = len(compare)
        # print(test_len)
        condition_success = True

        # Read adc from subject board
        # Instruction is in config
        while test_num < test_len:
            instruct = float(compare[test_num])
            model.bigfoot.set_vout(instruct)
            model.run_subject_test(p, e, a, t, 0, _ser)
            sleep(0.01)
            subject_adc_high = round(model.run_subject_test(p, e, a, t, 0, _ser), 1)
            print("ADC Return Value: " + str(test_num) + ": " + str(subject_adc_high) + "V \n")

            # convert instruction to voltage
            if logic == 5:
                subject_adc_high = round((subject_adc_high * 5.2) / 1024, 1)
            else:
                subject_adc_high = round((subject_adc_high * 3.3) / 1024, 1)

            Debug_file.write("ADC Return Value: " + str(test_num) + ": " + str(subject_adc_high) + "\n")
            print("ADC Return Value: " + str(test_num) + ": " + str(subject_adc_high) + "\n")
            # compare subject voltage to dac voltage
            if subject_adc_high > instruct - 0.4 and condition_success:
                condition_success = True
            else:
                condition_success = False
            test_num = test_num + 1

        if condition_success:
            return True
        return False

    elif t == 7:
        print("Test 7: Set Power Mode")
        Debug_file.write("Test 7: Set Power Mode\n")
        # Reads current 0
        current_0 = round(model.current_read(), 1)

        # Reads current
        # Instruction is in config
        compare = lines2[t].split(",")
        current = round(model.run_subject_test(p, e, a, t, p, _ser), 1)

        print("Current Val Null: " + str(current_0))
        print("Current Val: " + str(current))
        Debug_file.write("Current in mA Before Power Mode: " + str(current_0) + "\n")
        Debug_file.write("Current in mA After Power Mode: " + str(current) + "\n")
        # compare subject current to threshold
        if float(compare[1]) < (current_0-current):
            return True
        return False

    elif t == 8:
        print("Test 8: Wakeup From Sleep")
        Debug_file.write("Test 8: Wakeup From Sleep\n")
        # Reads current 0
        current_0 = round(model.current_read(), 1)

        compare = lines2[t].split(",")
        # Instruction is in config
        model.bigfoot.set_vout(0)
        current = round(model.run_subject_test(p, e, a, t, 0, _ser), 1)

        print("Current Val Null: " + str(current_0))
        print("Current Val: " + str(current))
        Debug_file.write("Current in mA Before Wakeup: " + str(current_0) + "\n")
        Debug_file.write("Current in mA After Wakeup: " + str(current) + "\n")
        # compare subject current to threshold
        if float(compare[1]) < (current-current_0):
            return True
        return False
        
    # Reset Pin Test
    elif t == 9:
        model.run_subject_test(p, e, a, 8, 0, _ser)
        sleep(0.2)
        return True

    return False


# ######################################################################
# MAIN LOOP
# ######################################################################
if __name__ == '__main__':
    # Facade Macro
    Facade = 0

    # Initialize model.check_5V() < 4.0 and model.check_3V3() < 2.5
    # Fork | Pipe View
    pass_array = ["Basic Test Results"]
    detailed_array = ["Detailed Test Results"]

    # New test
    while True:

        # Button Interrupts
        model.bigfoot.b1_disable()
        model.bigfoot.b2_disable()
        model.bigfoot.b3_disable()
        print(model.bigfoot.get_button_state())
                
        model.bigfoot.b1_enable()
        model.bigfoot.b2_enable()
        model.bigfoot.b3_enable()
        print(model.bigfoot.get_button_state())
        
        detailed_array.clear()
        pass_array.clear()

        detailed_array.append("Detailed Test Results")

        # Assign -> View Standby Screen
        view.setStandbyScreen()

        # Wait for Subject Board Connection / Shutdown Screen
        # Check Board Type | Save Variable | Blocking Loop
        try:
            board_type = model.board_wait()
        except Exception:
            
            sleep(2)
            setShutdownScreen()
            shutdown()
            pass

        # Assign -> View Start Test Screen
        view.setStartScreen(board_type)
    

        # Start Menu Screen Function
        # FIX: States Controlled by View -> button input
        print("Press Button 1 to Start New Test")
        start = False
        redo = False
        board_status = False
            
        while start is False:
            state_buttons = model.bigfoot.get_button_state()
            if supply_pin_voltages(board_type):
                view.setStartScreen("Please Place Dev Board\nonto Header Interface")
                redo = True
                start = True
                sleep(3)
            
            if state_buttons & 2 == 2:
                view.setFlashScreen()
                if supply_pin_voltages(board_type):
                    view.setStartScreen("Please Place Dev Board\nonto Header Interface")
                    redo = True
                    sleep(3)
                start = True
                model.bigfoot.b2_disable()

        # Subject Not Connecting
        if board_type == "No Boards Detected":
            redo = True
            sleep(2)

        # Assign -> View Testing Screen

        # Start Test Condition
        # Loop Through Config File
        # Test Conditions In Loop
        try:
            if start and not redo:
                board_status = model.subject_flash(board_type)
                print(board_status)
                
                if board_status:
                    view.setStartScreen("Flash Unsuccessful")
                    sleep(2)
                    redo = True
                else:
                    view.setRunningScreen(0)
               
                # While Loop Confirms Serial Connection
                if serial_check() and not redo:
                    # Read Config | Loop Through Tests
                    Lines = test_config_file(board_type)
                    test_count = len(Lines)
                    loop_count = 1
                    
                    # Pinmap Array
                    pinmap = pinmap_array(board_type)

                    res = [False for i in range(test_count - 1)]

                    # Loop until end of file line array | Open Serial
                    # Try Except Thing / Exception
                    ser = model.open_serial()
                    sleep(2)

                    # Test Booleans
                    test1_pass = True
                    test2_pass = True
                    test3_pass = True
                    test4_pass = True
                    test5_pass = True
                    test6_pass = True
                    test7_pass = True
                    test8_pass = True
                    test1_occured = False
                    test2_occured = False
                    test3_occured = False
                    test4_occured = False
                    test5_occured = False
                    test6_occured = False
                    test7_occured = False
                    test8_occured = False

                    # Open New Debug File
                    Debug_file = open("Debug_MicroDevTest.txt", "w")
                    Debug_file.close()

                    while loop_count < test_count and not redo:
                        
                        # Test Loop
                        test_loop = True
                        loop_limit = 0
                        while test_loop and loop_limit < 5:
                            Debug_file = open("Debug_MicroDevTest.txt", "a")

                            # Run Test Starts Here
                            try:
                                test = Lines[loop_count].split(",")
                                res[loop_count - 1] = subject_test(int(test[0]), int(test[1]), int(test[2]), int(test[3]),
                                                                   board_type,
                                                                   ser)
                                # print(res[loop_count-1])
                                print("Test#,PinID,Address,Enable: " + str(Lines[loop_count]))
                                Debug_file.write("Above results for Pin ID " + str(
                                            pinmap.get(int(test[1]))) + "\n\n")

                                test_num = int(test[0])
                                if res[loop_count - 1]:
                                    if test_num == 9:
                                        current_test = "Board Reset"
                                    elif test_num >= 7:
                                        current_test = "" + str(test_map.get(int(Lines[loop_count][0]))) + " Sleep Mode #" + str(
                                            test[1]) + " Result: Passed"
                                    else:
                                        current_test = "" + str(test_map.get(int(Lines[loop_count][0])))  + " Pin #" + str(
                                            pinmap.get(int(test[1]))) + " Result: Passed"
                                else:
                                    if test_num >= 7:
                                        current_test = "" + str(test_map.get(int(Lines[loop_count][0]))) + " Sleep Mode #" + str(
                                            test[1]) + " Result: Failed"
                                    else:
                                        current_test = "" + str(test_map.get(int(Lines[loop_count][0]))) + " Pin #" + str(
                                            pinmap.get(int(test[1]))) + " Result: Failed"
                                detailed_array.append(current_test)
                                test_loop = False
                            except Exception:
                                print("!!Test has Failed!!")
                                n = model.board_wait()
                                model.subject_flash(n)
                                loop_limit = loop_limit + 1
                                if loop_limit == 5:
                                    detailed_array.append("Not Able to Complete Testing")
                                pass
                                                                   
                        Debug_file.close()
                        # Show Progress of Tests
                        ratio_progress = int((float(loop_count)/float(test_count)) * 100)
                        print("Progress: " + str(ratio_progress) + "%")
                        view.setRunningScreen(ratio_progress)
                        
                        if test_num == 1:
                            # print(res[loop_count - 1])
                            test1_occured = True
                            if test1_pass and res[loop_count - 1]:
                                test1_pass = res[loop_count - 1]
                            else:
                                test1_pass = False
                        elif test_num == 2:
                            test2_occured = True
                            if test2_pass and res[loop_count - 1]:
                                test2_pass = res[loop_count - 1]
                            else:
                                test2_pass = False
                        elif test_num == 3:
                            test3_occured = True
                            if test3_pass and res[loop_count - 1]:
                                test3_pass = res[loop_count - 1]
                            else:
                                test3_pass = False
                        elif test_num == 4:
                            test4_occured = True
                            if test4_pass and res[loop_count - 1] == True:
                                test4_pass = res[loop_count - 1]
                            else:
                                test4_pass = False
                        elif test_num == 5:
                            test5_occured = True
                            if test5_pass and res[loop_count - 1] == True:
                                test5_pass = res[loop_count - 1]
                            else:
                                test5_pass = False
                        elif test_num == 6:
                            test6_occured = True
                            if test6_pass and res[loop_count - 1] == True:
                                test6_pass = res[loop_count - 1]
                            else:
                                test6_pass = False
                        elif test_num == 7:
                            test7_occured = True
                            if test7_pass and res[loop_count - 1] == True:
                                test7_pass = res[loop_count - 1]
                            else:
                                test7_pass = False
                        elif test_num == 8:
                            test8_occured = True
                            if test8_pass and res[loop_count - 1] == True:
                                test8_pass = res[loop_count - 1]
                            else:
                                test8_pass = False

                        loop_count = loop_count + 1
                        sleep(0.01)

                    # Close Serial Port
                    model.close_serial(ser)

                    # Write Basic Test Results
                    if test1_occured:
                        if test1_pass:
                            mess_test = "" + str(test_map.get(1)) + " Result: Passed"
                        else:
                            mess_test = "" + str(test_map.get(1)) + " Result: Failed"
                        pass_array.append(mess_test)
                    if test2_occured:
                        if test2_pass:
                            mess_test = "" + str(test_map.get(2)) + " Result: Passed"
                        else:
                            mess_test = "" + str(test_map.get(2)) + " Result: Failed"
                        pass_array.append(mess_test)
                    if test3_occured:
                        if test3_pass:
                            mess_test = "" + str(test_map.get(3)) + " Result: Passed"
                        else:
                            mess_test = "" + str(test_map.get(3)) + " Result: Failed"
                        pass_array.append(mess_test)
                    if test4_occured:
                        if test4_pass:
                            mess_test = "" + str(test_map.get(4)) + " Result: Passed"
                        else:
                            mess_test = "" + str(test_map.get(4)) + " Result: Failed"
                        pass_array.append(mess_test)
                    if test5_occured:
                        if test5_pass:
                            mess_test = "" + str(test_map.get(5)) + " Result: Passed"
                        else:
                            mess_test = "" + str(test_map.get(5)) + " Result: Failed"
                        pass_array.append(mess_test)
                    if test6_occured:
                        if test6_pass:
                            mess_test = "" + str(test_map.get(6)) + " Result: Passed"
                        else:
                            mess_test = "" + str(test_map.get(6)) + " Result: Failed"
                        pass_array.append(mess_test)
                    if test7_occured:
                        if test7_pass:
                            mess_test = "" + str(test_map.get(7)) + " Result: Passed"
                        else:
                            mess_test = "" + str(test_map.get(7)) + " Result: Failed"
                        pass_array.append(mess_test)
                    if test8_occured:
                        if test8_pass:
                            mess_test = "" + str(test_map.get(8)) + " Result: Passed"
                        else:
                            mess_test = "" + str(test_map.get(8)) + " Result: Failed"
                        pass_array.append(mess_test)


        except Exception:
            pass_array.append("Testing has Failed to Finish")
            pass
        finally:
            print("Complete Test Cycle")

            model.bigfoot.b1_enable()
            model.bigfoot.b2_enable()
            model.bigfoot.b3_enable()
            
        results_menu = True
        screen_wait = True
        details_wait = False
        save_wait = False

        # End of Test Sreen | Menu Booleans
        if not board_status and not redo:
            view.setResultsScreen(pass_array)

        # End of Test Screens
        while results_menu and not redo:
            
            # Loops back to Results Screen
            while screen_wait and not redo:
                state_buttons = model.bigfoot.get_button_state()
                if state_buttons & 1 == 1:
                    save_wait = True
                    screen_wait = False
                    model.bigfoot.b1_enable()
                    save_out = model.usb_save(detailed_array)
                    print(save_out)
                    view.setSaveScreen(save_out)
                elif state_buttons & 2 == 2:
                    model.bigfoot.b1_disable()
                    model.bigfoot.b2_disable()
                    model.bigfoot.b3_disable()
                    view.setDetailTestScreen(detailed_array)
                    print("continue")
                    details_wait = True
                    screen_wait = False
                    #sleep(1)
                elif state_buttons & 4 == 4:
                    model.bigfoot.b3_enable()
                    screen_wait = False
                    results_menu = False

            # Detailed Results State
            if details_wait:
                details_wait = False
                results_menu = True
                screen_wait = True
                
                model.bigfoot.b1_enable()
                model.bigfoot.b2_enable()
                model.bigfoot.b3_enable()
                view.setResultsScreen(pass_array)

            # Save Condition States
            if save_wait:
                model.bigfoot.b3_enable()
            while save_wait and not redo:
                state_buttons = model.bigfoot.get_button_state()
                # Add condition to save test results to usb
                if state_buttons & 4 == 4:
                    
                    model.bigfoot.b3_enable()
                    save_wait = False
                    screen_wait = True
                    view.setResultsScreen(pass_array)

        # Remove Board State | [After Screen Wait Loop]
        if not redo:
            view.setRemovalScreen()
        # Loop Removal Board Screen
        time_i = 0
        while model.check_5V() > 4.0 and time_i < 10:
            sleep(1)
            time_i = time_i + 1
            state_buttons = model.bigfoot.get_button_state()
            print(state_buttons)
        
        # NEW LOOP
        # Assign -> View General Results Screen with 3 button inputs
        Debug_file.close()
