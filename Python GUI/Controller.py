# MicroDev Project: Controller
# Date:
# Description: Controller Class

# Adjusting Globals:
# https://www.geeksforgeeks.org/python-globals-function/#:~:text=Syntax%3A%20globals%20%28%29%20Parameters%3A%20No%20parameters%20required.%20Code,%3D%20c%20%2B%20a%20globals%28%29%20%5B%27a%27%5D%20%3D%20d
# Low Power:
# https://controllerstech.com/low-power-modes-in-stm32/
# GPIO Interrupts
# https://medium.com/@rxseger/interrupt-driven-i-o-on-raspberry-pi-3-with-leds-and-pushbuttons-rising-falling-edge-detection-36c14e640fef#:~:text=Sounds%20complicated%2C%20fortunately%20the%20RPi.GPIO%20Python%20module%20included,%28%29%2C%20add%20a%20callback%20function%20using%20GPIO.add_event_detect%20%28%29.

#--

import serial

# serial example
try:
    ser = serial.Serial('/dev/ttyACM0', 115200)
    print(ser.portstr)      #check which port was really used
    print(ser.read(100))   #write a string
    ser.close()
except serial.SerialException as e:
    if e.errno == 13:
        raise e
    pass
except OSError:
    pass
finally:
    print("finally")


#STM32 ADC = 16 | GPIO = 5 ports * 16 pins | Sleep Modes = 3
ADC_PINS = 0
GPIO_PINS = 0
SLEEP_MODES = 0
BAUD_RATE = 0

#
def controller_init(model, view, driver):
    # print(string)
    # Grab Data from Pin Config File
    f = open("subject.config", "r")
    lines = f.readlines()

    num = lines[1].split("\n")
    globals()['GPIO_PINS'] = num[0]
    print(GPIO_PINS)

    num = lines[3].split("\n")
    globals()['ADC_PINS'] = num[0]
    print(ADC_PINS)

    num = lines[5].split("\n")
    globals()['SLEEP_MODES'] = num[0]
    print(SLEEP_MODES)

    num = lines[7].split("\n")
    globals()['BAUD_RATE'] = num[0]
    print(BAUD_RATE)



    # Update global variables with this data
    # GPIO Pin Amount
    # Analog Pin Amount
    # Sleep Modes Amount
    return "Something"

# ******************************** Subject Tests ************************************
def run_gpio_output_loading_test():
    print("test")


# ******************************** User Input Reads ************************************
#
def start_read():

    print("Something")


#
def arrow_up_read():
    print("Up")


#
def arrow_down_read():
    print("clear")


# ******************************** Subject Board I/O ************************************
#
def subject_read():
    try:
        ser_ = serial.Serial('/dev/ttyACM0', globals()['BAUD_RATE'])
        print(ser_.portstr)  # check which port was really used
        print(ser_.read(100))  # write a string
        # parse info for correct start and stop characters then send Acknowledge
        # write
        ser_.close()
    except serial.SerialException as e:
        if e.errno == 13:
            raise e
        pass
    except OSError:
        pass
    finally:
        print("read")


#
def subject_write(str_write):
    try:
        ser = serial.Serial('/dev/ttyACM0', globals()['BAUD_RATE'])
        print(ser.portstr)  # check which port was really used
        ser.write(str_write)  # write a string

        # read acknowledge byte to continue
        ser.close()
    except serial.SerialException as e:
        if e.errno == 13:
            raise e
        pass
    except OSError:
        pass
    finally:
        print("write")


#
def subject_flash():

    print("flash")


#
def subject_init(string):
    print(string)
    return "Something"


# Test Code
controller_init(1, 1, 1)


