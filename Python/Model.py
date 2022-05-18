# #################################################
# MicroDev Project: Model
# Date: May 2, 2022
# Description: Model Class
# Authors:
# Nathan Hanchey
# Dylan
# Connor
# Corey
# #################################################


# Adjusting Globals:
# https://www.geeksforgeeks.org/python-globals-function/#:~:text=Syntax%3A%20globals%20%28%29%20Parameters%3A%20No%20parameters%20required.%20Code,%3D%20c%20%2B%20a%20globals%28%29%20%5B%27a%27%5D%20%3D%20d
# Low Power:
# https://controllerstech.com/low-power-modes-in-stm32/
# GPIO Interrupts
# https://medium.com/@rxseger/interrupt-driven-i-o-on-raspberry-pi-3-with-leds-and-pushbuttons-rising-falling-edge-detection-36c14e640fef#:~:text=Sounds%20complicated%2C%20fortunately%20the%20RPi.GPIO%20Python%20module%20included,%28%29%2C%20add%20a%20callback%20function%20using%20GPIO.add_event_detect%20%28%29.
import time
import serial
import subprocess
import string

# STM32 ADC = 16 | GPIO = 5 ports * 16 pins | Sleep Modes = 3
from serial import to_bytes
ADC_PINS = 0
GPIO_PINS = 0
SLEEP_MODES = 0
BAUD_RATE = 0

view = None
model = None
driver = None


def __init__(self):
    print("controller")


#
def controller_init(self, model1, view1, driver1):
    # print(string)
    self.view = view1
    self.model = model1
    self.driver = driver1

    # Grab Data from Pin Config Files
    f = open("subject.config", "r")
    lines = f.readlines()

    # FIX CONFIGURATIONS
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


# ******************************** Subject Board I/O ************************************
#
def open_serial():
    ser = serial.Serial('/dev/ttyACM0', 115200)
    ser.flushInput()
    ser.flushOutput()
    return ser


def close_serial(ser):
    ser.close()


def subject_write(str_write, ser):
    try:
        # ser = serial.Serial('/dev/ttyACM0', 115200)
        # Writes byte array
        print(str_write)
        ser.write(str_write)  # write a string
        # read acknowledge byte to continue
        # ser.close()
    except serial.SerialException as e:
        if e.errno == 13:
            raise e
        pass
    except OSError:
        pass
    finally:
        print("write")


def subject_read(ser_):
    try:
        # ser_ = serial.Serial('/dev/ttyACM0', 115200)
        print(ser_.portstr)  # check which port was really used

        # Read Byte array
        data = bytearray(3)
        # Set Timeout
        ser_.timeout = 2

        # READ SERIAL
        data = ser_.read(3)

        # Debugging
        print(data)

       # parse info for correct start and stop characters then send Acknowledge
       # ser_.close()
    except serial.SerialException as e:
        if e.errno == 13:
            raise e
        pass
    except OSError:
        pass
    finally:
        print("read")

    return data


# CRC Decoding
def crc_decode(value, out_type):

    out = 0
    # Check CRC is correct first
    int_val = int.from_bytes(value, "big")
    if (int_val % 5) == 0:
        print("CRC Pass")
        # Conditional on which data point to decode
        # E.G. 1 = pin, 2 = test, 3 = results
        if out_type == 1:
            out = int(value[0])
            print("pin")
        elif out_type == 2:
            out = int(value[2])
            out = out & 0xF0
            out = out >> 4
            print("test")
        elif out_type == 3:
            out = int(value[1])
            print("results")

    else:
        print("CRC Fail")

    # return type value
    return out


# CRC Encoding
def crc_encode(test, pin, instruction):

    # CRC KEY => 0101 = 5
    # 1) Find Remainder
    # byte array to int
    packet = bytearray(3)
    crc_byte = test << 4

    packet[0] = pin
    packet[1] = instruction
    packet[2] = crc_byte

    crc_data = int.from_bytes(packet, 'big')
    remainder = crc_data % 5

    # 2) Subtract Key - Remainder
    crc = 5 - remainder

    # 3) Add value to data
    crc_byte = crc_byte + crc

    # 4) int converts to Byte array
    packet[2] = crc_byte

    # return byte array
    print("encode")
    return packet


# ******************************** Subject Tests ************************************
def run_gpio_output_loading_test():
    print("test")


# ******************************** User Input Reads ************************************
def start_read():
    print("Something")
    return None


#
def arrow_up_read():
    print("Up")


#
def arrow_down_read():
    print("clear")


# ******************************** Command Line Interface ************************************
#
def subject_flash(board):

    # ARDUINO UNO FLASH
    if board == "Arduino Uno Detected":
        res = subprocess.getstatusoutput(
            f'arduino-cli upload -b arduino:avr:uno -p /dev/ttyACM0 -i Flash/serial_com.ino.with_bootloader.hex')
        # Confirm Success with CLI output


    # STM32F411 FLASH

    # STM32F401 FLASH
    elif board == "STM32F401 Detected":
        res = subprocess.getstatusoutput(
            f'st-flash write Flash/stmf401.bin 0x08000000')

    print(res)


def board_list():

    # 1) ARDUINO DETECTION
    res_ardiuno = subprocess.getstatusoutput(f'arduino-cli board list')

    # PARSE DATA FOR ARDUINO
    # print(res_ardiuno[1])
    ARD = res_ardiuno[1].split("\n")
    boards = len(ARD)

    # No Board Detection
    if boards <= 2:
        return "No Boards Detected"

    # Arduino Uno Detection
    elif boards == 3 or boards == 4:
        board_type = ARD[1].split(" ")
        # print(board_type[4])
        if board_type[4] == "Serial":
            # print(board_type[8])
            if board_type[8] == "Uno":
                return "Arduino Uno Detected"
        elif board_type[4] == "Unknown":
            print(board_type)

    else:
        return "Overflow"

    # 2) STM DETECTION
    res_stm = subprocess.getstatusoutput(f'st-info --probe')
    # PARSE DATA FOR STM'S
    # print(res_stm[1])

    STM = res_stm[1].split("\n")
    boards1 = len(STM)

    # STM UNIQUE IDs
    # 0x0433: STM32F401xD/E
    # 0x0431: STM32F411xC/E
    if boards1 > 6:

        Chip_ID = STM[5].split(" ")
        Chip_ID = list(filter(None, Chip_ID))

        Family = STM[6].split(" ")
        Family = list(filter(None, Family))
        str(Family).replace("x", "")

        print(Chip_ID)
        print(Family)
        if Family[1] == "F4" and Chip_ID[1] == "0x0431":
            return "STM32F411 Detected"

        elif Family[1] == "F4" and Chip_ID[1] == "0x0433":
            return "STM32F401 Detected"

    # Use class globals for board file path and id info
    return "No Boards Detected"


#
def subject_init(string):
    print(string)
    return "Something"



