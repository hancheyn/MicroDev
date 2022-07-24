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
import subprocess
import Model
import View

view = View
model = Model


###################################################################################

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


# Description: Preforms Test on Supply Pins 3V3 and 5V
# Parameters:
# Returns: Boolean Pass or Fail
def supply_pin_voltages(board):
    # Gather Config Data from Config file of board type

    # FIX MOVE TO THRESHOLD FUNCTION
    if board == "Arduino Uno Detected":
        file2 = open('unoThreshold.config', 'r')
        logic = 5
    elif board == "STM32F411 Detected" or board == "STM32F446 Detected":
        file2 = open('stm32f4Threshold.config', 'r')
        logic = 3.3
    else:
        return False

    lines2 = file2.readlines()
    compare = lines2[9].split(",")

    if model.check_5V() < float(compare[1]) and model.check_3V3() < float(compare[2]):
        return True
    return False


# Description: Preforms Test Comparisons
# Parameters: Test ID Int | Pin ID Int | Address Int | Enable Int | Board type String
# Returns: Boolean Pass or Fail
def subject_test(t, p, a, e, board, _ser):
    # Logic Level Config
    logic = 0

    # Gather Config Data from Config file of board type

    # FIX MOVE TO THRESHOLD FUNCTION
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
        print("Test 1: Output without Load")
        compare = lines2[1].split(",")

        # Read adc value of logic high from micro
        print("Test Logic High")
        high = model.run_subject_test(p, e, a, t, 1, _ser)

        # Read adc value of logic low from micro
        print("Test Logic Low")
        low = model.run_subject_test(p, e, a, t, 0, _ser)

        # Compare to Config threshold and Return Pass or Fail Boolean
        if float(compare[1]) < high and float(compare[2]) > low:
            return True
        return False

    elif t == 2:
        print("Test 2: Output w/ Load")
        compare = lines2[2].split(",")

        # Read adc value of logic high from micro
        print("Test Logic High")
        high = model.run_subject_test(p, e, a, t, 1, _ser)

        # Read adc value of logic low from micro
        print("Test Logic Low")
        low = model.run_subject_test(p, e, a, t, 0, _ser)

        # Compare to Config threshold and Return Pass or Fail Boolean
        if float(compare[1]) < high and float(compare[2]) > low:
            return True
        return False

    elif t == 3:
        print("Test 3: Pull-Up Input")
        compare = lines2[t].split(",")
        adc2 = 0

        # Read adc value at threshold voltage Pull Up Test
        # Instruction depends on logic level (controls dac)
        adc1 = model.run_subject_test(p, e, a, t, 0x00, _ser)

        if logic == 5:
            adc2 = model.run_subject_test(p, e, a, t, 0x01, _ser)
            Rpu = (((390 * 5) / adc2) - 390)
        else:
            adc2 = model.run_subject_test(p, e, a, t, 0x01, _ser)
            Rpu = (((390 * 3.3) / adc2) - 390)

        # calculation with adc to pull down resistance value
        print("Test adc val: " + str(adc2))
        Rpu = (((390 * 5) / adc2) - 390)
        if Rpu > float(compare[1]) and Rpu < float(compare[2]) and adc1 > float(compare[3]):
            return True
        return False

    elif t == 4:
        print("Test 4: Pull-Down Input")
        compare = lines2[t].split(",")
        adc4 = 0

        # Read adc value at threshold voltage
        adc1 = model.run_subject_test(p, e, a, t, 0x00, _ser)

        if logic == 5:
            model.bigfoot.set_vout(5)
            adc4 = model.run_subject_test(p, e, a, t, 0x0F, _ser)
        else:
            model.bigfoot.set_vout(3.3)
            adc4 = model.run_subject_test(p, e, a, t, 0x0A, _ser)

        # calculation with adc to pull down resistance value
        print("Test adc val: " + str(adc4))
        Rpd = (2000 * adc4) / (3.3 - adc4)
        if Rpd > float(compare[1]) and Rpd < float(compare[2]) and adc1 < float(compare[3]):
            return True
        return False

    elif t == 5:
        print("Test 5: Input Logic")

        # Read digital pin from subject board
        if logic == 5:
            model.bigfoot.set_vout(5)
            subject_input_high = model.run_subject_test(p, e, a, t, 0x0F, _ser)
        else:
            model.bigfoot.set_vout(3.3)
            subject_input_high = model.run_subject_test(p, e, a, t, 0x0A, _ser)

        # Read Digital Pin Low
        model.bigfoot.set_vout(0)
        subject_input_low = model.run_subject_test(p, e, a, t, 0, _ser)
        print("Logic High Val: " + str(subject_input_high))
        print("Logic Low Val: " + str(subject_input_low))

        if 1 == subject_input_high and 0 == subject_input_low:
            return True
        return False

    elif t == 6:
        print("Test 6: ADC Check")
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
            subject_adc_high = model.run_subject_test(p, e, a, t, 0, _ser)
            print("ADC Return Value: " + str(test_num) + ": " + str(subject_adc_high))
            # convert instruction to voltage
            # compare subject voltage to dac voltage
            if subject_adc_high > instruct - 0.1 and condition_success:
                condition_success = True
            else:
                condition_success = False
            test_num = test_num + 1

        if condition_success:
            return True
        return False

    elif t == 7:
        print("Test 7: Set Power Mode")
        # Reads current 0
        current_0 = model.current_read()

        # Reads current
        # Instruction is in config
        compare = lines2[t].split(",")
        current = model.run_subject_test(p, e, a, t, 0, _ser)

        print("Current Val Null: " + str(current_0))
        print("Current Val: " + str(current))
        # compare subject current to threshold
        if float(compare[1]) < (current_0-current):
            return True
        return False

    elif t == 8:
        print("Test 8: Wakeup From Sleep")
        # Reads current 0
        current_0 = model.current_read()

        compare = lines2[t].split(",")
        # Instruction is in config
        model.bigfoot.set_vout(0)
        current = model.run_subject_test(p, e, a, t, 0, _ser)

        print("Current Val Null: " + str(current_0))
        print("Current Val: " + str(current))
        # compare subject current to threshold
        if float(compare[1]) < (current-current_0):
            return True
        return False

    return False


# ###############################################################################
# MAIN LOOP
# ###############################################################################
if __name__ == '__main__':
    # Facade Macro
    Facade = 0

    # Initializemodel.check_5V() < 4.0 and model.check_3V3() < 2.5
    # Fork | Pipe View
    pass_array = ["Basic Test Results"]
    detailed_array = ["Detailed Test Results"]

    # New test
    while True:

        # Button Interrupts
        model.bigfoot.b1_enable()
        model.bigfoot.b2_enable()
        model.bigfoot.b3_enable()

        detailed_array.clear()
        pass_array.clear()

        detailed_array.append("Detailed Test Results")

        # Assign -> View Standby Screen
        view.setStandbyScreen()

        # Wait for Subject Board Connection / Shutdown Screen
        # Check Board Type | Save Variable | Blocking Loop
        board_type = model.board_wait()

        # Assign -> View Start Test Screen
        view.setStartScreen()

        # Start Menu Screen Function
        # FIX: States Controlled by View -> button input
        print("Press Button 1 to Start New Test")
        start = False
        redo = False
        while start is False:
            state_buttons = model.bigfoot.get_button_state()
            if state_buttons & 2 == 2:
                view.setFlashScreen()
                # _board_type = model.board_list()
                if (supply_pin_voltages(board_type)):
                    redo = True
                start = True
                model.bigfoot.b2_disable()
            # if button 2 then shutdown
            elif state_buttons & 1 == 1:
                model.bigfoot.b1_disable()
                model.shutdown()

        # Assign -> View Testing Screen

        # Start Test Condition
        # Loop Through Config File
        # Test Conditions In Loop
        # FIX MOVE START TEST to FUNCTION?
        try:
            if start and not redo:
                model.subject_flash(board_type)
                view.setRunningScreen(pass_array)
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

                    while loop_count < test_count:
                        test = Lines[loop_count].split(",")
                        res[loop_count - 1] = subject_test(int(test[0]), int(test[1]), int(test[2]), int(test[3]),
                                                           board_type,
                                                           ser)
                        # print(res[loop_count-1])
                        print("Test#,PinID,Address,Enable: " + str(Lines[loop_count]))
                        test_num = int(test[0])
                        current_test = "Test #" + str(Lines[loop_count][0]) + " Pin #" + str(
                            test[1]) + " Result: " + str(res[loop_count - 1])
                        detailed_array.append(current_test)

                        # Show Progress of Tests
                        view.setRunningScreen(detailed_array[loop_count - 1])

                        if test_num == 1:
                            # print(res[loop_count - 1])
                            test1_occured = True
                            if test1_pass == True and res[loop_count - 1] == True:
                                test1_pass = res[loop_count - 1]
                            else:
                                test1_pass = False
                        elif test_num == 2:
                            test2_occured = True
                            if test2_pass == True and res[loop_count - 1] == True:
                                test2_pass = res[loop_count - 1]
                            else:
                                test2_pass = False
                        elif test_num == 3:
                            test3_occured = True
                            if test3_pass == True and res[loop_count - 1] == True:
                                test3_pass = res[loop_count - 1]
                            else:
                                test3_pass = False
                        elif test_num == 4:
                            test4_occured = True
                            if test4_pass == True and res[loop_count - 1] == True:
                                test4_pass = res[loop_count - 1]
                            else:
                                test4_pass = False
                        elif test_num == 5:
                            test5_occured = True
                            if test5_pass == True and res[loop_count - 1] == True:
                                test5_pass = res[loop_count - 1]
                            else:
                                test5_pass = False
                        elif test_num == 6:
                            test6_occured = True
                            if test6_pass == True and res[loop_count - 1] == True:
                                test6_pass = res[loop_count - 1]
                            else:
                                test6_pass = False
                        elif test_num == 7:
                            test7_occured = True
                            if test7_pass == True and res[loop_count - 1] == True:
                                test7_pass = res[loop_count - 1]
                            else:
                                test7_pass = False
                        elif test_num == 8:
                            test8_occured = True
                            if test8_pass == True and res[loop_count - 1] == True:
                                test8_pass = res[loop_count - 1]
                            else:
                                test8_pass = False

                        loop_count = loop_count + 1
                        sleep(0.01)

                    # Close Serial Port
                    model.close_serial(ser)

                    # Write Basic Test Results
                    if test1_occured:
                        mess_test = "Test #1 Result: " + str(test1_pass)
                        pass_array.append(mess_test)
                    if test2_occured:
                        mess_test = "Test #2 Result: " + str(test2_pass)
                        pass_array.append(mess_test)
                    if test3_occured:
                        mess_test = "Test #3 Result: " + str(test3_pass)
                        pass_array.append(mess_test)
                    if test4_occured:
                        mess_test = "Test #4 Result: " + str(test4_pass)
                        pass_array.append(mess_test)
                    if test5_occured:
                        mess_test = "Test #5 Result: " + str(test5_pass)
                        pass_array.append(mess_test)
                    if test6_occured:
                        mess_test = "Test #6 Result: " + str(test6_pass)
                        pass_array.append(mess_test)
                    if test7_occured:
                        mess_test = "Test #7 Result: " + str(test7_pass)
                        pass_array.append(mess_test)
                    if test8_occured:
                        mess_test = "Test #8 Result: " + str(test8_pass)
                        pass_array.append(mess_test)


        except Exception:
            pass_array.append("Testing has Failed to Finish")
            pass
        finally:
            print("Complete Test Cycle")

            model.bigfoot.b1_enable()
            model.bigfoot.b2_enable()

        # End of Test Menu
        view.setResultsScreen(pass_array)
        results_menu = True
        screen_wait = True
        details_wait = False
        save_wait = False

        # End of Test Screen
        while results_menu and not redo:
            while screen_wait and not redo:
                state_buttons = model.bigfoot.get_button_state()

                if state_buttons & 1 == 1:
                    view.setSaveScreen()
                    save_wait = True
                    screen_wait = False
                    model.bigfoot.b1_disable()

                elif state_buttons & 2 == 2:
                    model.bigfoot.b2_disable()
                    view.setDetailTestScreen(detailed_array)
                    details_wait = True
                    screen_wait = False

                elif state_buttons & 4 == 4:
                    model.bigfoot.b3_disable()
                    screen_wait = False
                    results_menu = False

            # Detailed Results State
            if details_wait:
                model.bigfoot.b2_enable()
            while details_wait and not redo:
                state_buttons = model.bigfoot.get_button_state()

                if state_buttons & 4 == 4:
                    model.bigfoot.b3_disable()
                    # model.bigfoot.b3_enable()
                    details_wait = False
                    results_menu = False
                elif state_buttons & 1 == 1:
                    view.setSaveScreen()
                    save_wait = True
                    model.bigfoot.b1_disable()
                    details_wait = False

            # Save Condition States
            if save_wait:
                model.bigfoot.b3_enable()
            while save_wait and not redo:
                state_buttons = model.bigfoot.get_button_state()
                # Add condition to save test results to usb
                if state_buttons & 4 == 4:
                    model.bigfoot.b3_disable()

                    save_wait = False
                    screen_wait = True
                    usb_filepath = model.usb_list()

                    if usb_filepath != "None":
                        usb_file = usb_filepath
                        usbf = open("MicroDevTest_Results.txt", "w")
                        for i in detailed_array:
                            usbf.write(i + "\n")
                        usbf.close()
                        h = subprocess.getstatusoutput("cp MicroDevTest_Results.txt " + usb_file)

                    print(usb_filepath)
                    view.setResultsScreen(pass_array)
                    model.bigfoot.b1_enable()
                    model.bigfoot.b2_enable()
                    model.bigfoot.b3_enable()

        # Remove Board State
        view.setRemovalScreen()

        # Loop
        # print("Flash")
        # print(detailed_array)
        # print(pass_array)
        time_i = 0
        while model.check_5V() > 4.0 and time_i < 10:
            sleep(1)

        # NEW LOOP
        # Assign -> View General Results Screen with 3 button inputs
