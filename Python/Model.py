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
import Bigfoot as bigfoot

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


# Description:
# Accepts:
# Returns:
def controller_init(self, model1, view1, driver1):
    # print(string)
    self.view = view1
    self.model = model1
    self.driver = driver1

    # Grab Data from Pin Config Files
    f = open("subject.config", "r")
    lines = f.readlines()

    # FIX CONFIGURATIONS
    # Enable Current to Subject Board
    bigfoot.high_current(1)
    bigfoot.low_current(1)
    # Reset GPIO Pins
    bigfoot.set_mux_add(0, 0, 0)

    # Will the
    # GPIO Pin Amount
    # Analog Pin Amount
    # Sleep Modes Amount
    return "Something"


# ******************************** Subject Board I/O ************************************
#
# Description:
# Accepts:
# Returns:
def open_serial():
    ser = serial.Serial('/dev/ttyACM0', 115200)
    ser.flushInput()
    ser.flushOutput()
    return ser


# Description:
# Accepts:
# Returns:
def close_serial(ser):
    ser.close()


# Description:
# Accepts:
# Returns:
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


# Description:
# Accepts:
# Returns:
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
# Description:
# Accepts:
# Returns:
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
# Description:
# Accepts:
# Returns:
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


# Serial Setup
# Opens and Closes Serial to Double-Check Com.
def serial_setup():

    s = bytearray(3)
    s[0] = 0x01
    s[1] = 0x10
    s[2] = 0x03

    ser = open_serial()
    time.sleep(2)
    subject_write(str_write=s, ser=ser)
    test_bytes = subject_read(ser_=ser)
    close_serial(ser)

    print("serial setup complete")


# ******************************** Subject Tests ************************************
# GENERIC TEST FUNCTION
# Description: Runs test based on test and pin IDs
# Accepts: pin ID # | enable # | address # | enable ID # | instruction
# Returns: Test Results (voltage, logic, etc.)
def run_subject_test(pin, enable, address, test, instruction):

    # Call Test function
    # Conditional for Test
    if test == 1:
        run_gpio_output_test(pin, enable, address, instruction)
    elif test == 2:
        run_gpio_output_loading_test(pin, enable, address, instruction)
    elif test == 3:
        run_gpio_output_loading_test(pin, enable, address, instruction)
    elif test == 4:
        run_gpio_output_loading_test(pin, enable, address, instruction)
    elif test == 5:
        run_gpio_output_loading_test(pin, enable, address, instruction)
    elif test == 6:
        run_gpio_output_loading_test(pin, enable, address, instruction)
    elif test == 7:
        run_gpio_output_loading_test(pin, enable, address, instruction)
    elif test == 8:
        run_power_mode_test(pin, instruction)

    # return results for specified pin
    return 1


# Description: Test ID #1 | GPIO Output Test
# Send Logic Voltage as Parameter (sets logic based on BIT0 of instruction)
# HIGH = 1 | LOW = 0
# instruction BIT7 controls facade test
# Spec: 3.00 Output Logic
# Accepts: pin ID # | enable # | address # | enable ID # | instruction
# Returns: Bigfoot adc voltage
def run_gpio_output_test(pin, enable, address, instruction):

    # Configure Bigfoot without load to adc
    bigfoot.adc_load(0)
    bigfoot.adc_enable(1)
    # State (on,off) | Enable # | Address #
    bigfoot.set_mux_add(1, enable, address)

    # Communication to Subject Serial
    # Configures output low on subject board
    # .encode([test], [pin], [instruction])
    s = crc_encode(0x01, pin, instruction)
    ser = open_serial()
    #time.sleep(2)
    subject_write(str_write=s, ser=ser)
    test_bytes = subject_read(ser_=ser)
    close_serial(ser)
    output = crc_decode(test_bytes, 2)
    print(output)

    # Read Bigfoot ADC
    adc = bigfoot.rpi_i2c_adc()

    # reset & return pass or fail of test
    bigfoot.adc_enable(0)
    bigfoot.set_mux_add(0, 0, 0)
    print("test 1")
    return adc


# Description: Test ID #2 | GPIO Output Test /w Load
# Send Logic Voltage as Parameter (sets voltage based on BIT3-BIT0 of instruction)
# (Approximate Values) 0.311 = 0x01 | 0.619	= 0x02 | ... | 3.08	= 0x0A | ... | 4.59	= 0x0F
# instruction BIT7 controls facade test
# Spec: 3.02 Voltage Under Load
# Accepts: pin ID # | enable # | address # | enable ID # | instruction
# Returns: Bigfoot adc
def run_gpio_output_loading_test(pin, enable, address, instruction):
    # Configure Bigfoot with load
    bigfoot.adc_enable(1)
    bigfoot.adc_load(1)

    # State (on,off) | Enable # | Address #
    bigfoot.set_mux_add(1, enable, address)

    # Communication to Subject Serial
    # Configures output low on subject board
    # .encode([test], [pin], [instruction])
    s = crc_encode(0x02, pin, instruction)
    ser = open_serial()
    subject_write(str_write=s, ser=ser)
    test_bytes = subject_read(ser_=ser)
    close_serial(ser)
    output = crc_decode(test_bytes, 2)
    print(output)

    # Read Bigfoot ADC
    adc = bigfoot.rpi_i2c_adc()

    # return pass or fail of test
    bigfoot.adc_enable(0)
    bigfoot.adc_load(0)
    bigfoot.set_mux_add(0, 0, 0)
    print("test 2")
    return adc


# Description: Test ID #3 | Input Pull Up Resister Test
# instruction BIT7 controls facade test
# Spec: 3.03 Input Resistance Value & 3.04 Pull Up Test
# ADC Load Resistor
# Accepts: pin ID # | enable # | address # | enable ID # | instruction
# Returns: Bigfoot adc
def run_gpio_input_pull_up_test(pin, enable, address, instruction):

    # Configure Bigfoot w/
    bigfoot.adc_enable(1)
    bigfoot.adc_load(1)
    bigfoot.set_mux_add(1, enable, address)

    # Communication to Subject Serial
    # Configure input pull-ups
    # Returns Subject Input Read
    # .encode([test], [pin], [instruction])
    s = crc_encode(0x03, pin, instruction)
    ser = open_serial()
    subject_write(str_write=s, ser=ser)
    test_bytes = subject_read(ser_=ser)
    close_serial(ser)
    output = crc_decode(test_bytes, 2)
    print(output)

    # Configure Bigfoot w/
    bigfoot.adc_enable(1)

    # Read Bigfoot ADC Voltage
    adc = bigfoot.rpi_i2c_adc()

    # return pass or fail of test
    bigfoot.adc_enable(0)
    bigfoot.set_mux_add(0, 0, 0)
    print("test 3")
    return adc


# Description: Test ID #4 | Input Pull Down Test
# Send Voltage as Parameter (sets voltage based on BIT3-BIT0 of instruction)
# (Approximate Values) 0.311 = 0x01 | 0.619	= 0x02 | ... | 3.08	= 0x0A | ... | 4.59	= 0x0F
# instruction BIT7 controls facade test
# Spec: 3.03 Input Resistance Value & 3.05 Pull Down Test
# Configure DAC to Supply Voltage (To Test Internal Resistance)
# Accepts: pin ID # | enable # | address # | enable ID # | instruction
# Returns: Bigfoot adc
def run_gpio_input_pull_down_test(pin, enable, address, instruction):

    # Configure Bigfoot w/
    bigfoot.adc_enable(1)
    bigfoot.adc_load(0)
    bigfoot.dac_enable(1)
    bigfoot.set_mux_add(1, enable, address)

    # Communication to Subject Serial
    # Configure input pull-downs
    # Returns Subject Input Read
    # .encode([test], [pin], [instruction])
    s = crc_encode(0x04, pin, instruction)
    ser = open_serial()
    subject_write(str_write=s, ser=ser)
    test_bytes = subject_read(ser_=ser)
    close_serial(ser)
    output = crc_decode(test_bytes, 2)
    print(output)

    # Read Bigfoot ADC Voltage
    adc = bigfoot.rpi_i2c_adc()

    # return pass or fail of test
    bigfoot.adc_enable(0)
    bigfoot.dac_enable(0)
    bigfoot.set_mux_add(0, 0, 0)
    print("test 4")
    return adc


# Description: Test ID #5 | Input Logic Level Test
# Send Voltage as Parameter (sets voltage based on BIT3-BIT0 of instruction)
# (Approximate Values) 0.311 = 0x01 | 0.619	= 0x02 | ... | 3.08	= 0x0A | ... | 4.59	= 0x0F
# instruction BIT7 controls facade test
# Spec: 3.06 Input Logic Test
# Accepts: pin ID # | enable # | address # | enable ID # | instruction
# Returns: Bigfoot adc
def run_gpio_input_logic_level_test(pin, enable, address, instruction):

    # Reset/Configure Bigfoot to Low Logic
    bigfoot.dac_enable(1)
    bigfoot.adc_load(0)
    bigfoot.rpi_i2c_dac(1)
    bigfoot.set_mux_add(1, enable, address)

    # Configure Bigfoot to high logic
    bigfoot.rpi_i2c_dac(instruction)

    # Communication to Subject Serial
    # .encode([test], [pin], [instruction])
    s = crc_encode(0x05, pin, instruction)
    ser = open_serial()
    subject_write(str_write=s, ser=ser)
    test_bytes = subject_read(ser_=ser)
    close_serial(ser)
    output = crc_decode(test_bytes, 2)
    print(output)

    # ADC
    adc = int(test_bytes[1])

    # return pass or fail of test
    bigfoot.dac_enable(0)
    bigfoot.set_mux_add(0, 0, 0)
    print("test")
    return adc


# Description: Test ID #6 | ADC Test
# Send Voltage as Parameter (sets voltage based on BIT3-BIT0 of instruction)
# (Approximate Values) 0.311 = 0x01 | 0.619	= 0x02 | ... | 3.08	= 0x0A | ... | 4.59	= 0x0F
# instruction BIT7 controls facade test
# Spec: 3.07 ADC Test
# Pass in the voltage to use also
# Accepts: pin ID # | enable # | address # | enable ID # | instruction
# Returns: Subject adc
def run_adc_test(pin, enable, address, instruction):

    # Communication to Subject Serial to configure
    # Configure to ADC Input
    bigfoot.adc_enable(0)
    bigfoot.adc_load(0)
    bigfoot.set_mux_add(1, enable, address)

    # Configure Bigfoot to reset Subject ADC pins
    # Enable DAC
    bigfoot.dac_enable(1)
    # Set DAC to first configuration instruction
    # .encode([test], [pin], [instruction])
    s = crc_encode(0x06, pin, instruction)
    ser = open_serial()
    subject_write(str_write=s, ser=ser)
    test_bytes = subject_read(ser_=ser)
    close_serial(ser)
    output = crc_decode(test_bytes, 2)
    print(output)

    # Communication to Subject Serial to read ADC
    # ADC
    adc = int(test_bytes[1])

    # return pass or  fail of test
    bigfoot.set_mux_add(0, 0, 0)
    print("test 6")
    return adc


# Description: Test ID #7 | Power Mode Test
# Sleep Mode sent as 'instruction' to serial com.
# instruction BIT7 controls facade test
# Wakeup Pin Set through 'pin' ID
# Spec: 3.08 Power Modes
# Accepts: pin ID # | instruction (sleep_mode)
# Returns: Bigfoot current
def run_power_mode_test(pin, instruction):

    # Configure Bigfoot
    bigfoot.dac_enable(0)
    bigfoot.high_current(1)
    bigfoot.low_current(0)
    # Always On

    # Communication to Subject Serial
    # .encode([test], [pin], [instruction])
    s = crc_encode(0x07, pin, instruction)
    ser = open_serial()
    subject_write(str_write=s, ser=ser)
    # test_bytes = subject_read(ser_=ser)
    close_serial(ser)
    # output = crc_decode(test_bytes, 2)
    # print(output)

    # Read Bigfoot Low Current Sensor
    # TIME DELAY
    time.sleep(1)
    current = bigfoot.rpi_i2c_ina219()

    # return pass or fail of test
    bigfoot.dac_enable(0)
    bigfoot.set_mux_add(0, 0, 0)
    print("test 7")
    return current


# Description: Test ID #8 | Runs wake up test
# Accepts: pin ID # | enable # | address # | enable ID # | instruction
# Spec: 3.08 Wakeup
# Returns: Bigfoot current
def run_wakeup_test(pin, enable, address, instruction):
    # Configure Bigfoot
    # Set Wakeup pin
    bigfoot.set_mux_add(1, enable, address)
    bigfoot.dac_enable(1)
    bigfoot.high_current(0)
    bigfoot.low_current(0)  # Always On

    # Configure Bigfoot to high logic
    bigfoot.rpi_i2c_dac(instruction)
    # TIME DELAY?

    # Red Bigfoot Low Current Sensor
    current = bigfoot.rpi_i2c_ina219()

    # return pass or fail of test
    bigfoot.set_mux_add(0, 0, 0)
    print("test 8")
    return current


# MAY DELETE INPUTS FROM MODEL
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
# Description:
# Accepts:
# Returns:
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


# Description: Uses CLI to read for subject board connections
# Accepts: NA
# Returns: [string] board type
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
        Family = str(Family[1]).replace("x", "")

        print(Chip_ID)
        print(Family)
        if Family == "F4" and Chip_ID[1] == "0x0431":
            return "STM32F411 Detected"

        elif Family == "F4" and Chip_ID[1] == "0x0433":
            return "STM32F401 Detected"

        elif Family == "F446" and Chip_ID[1] == "0x0421":
            return "STM32F446 Detected"

    # Use class globals for board file path and id info
    return "No Boards Detected"


# Description: Uses CLI to read for subject board connections
# Accepts: NA
# Returns: [string] usb file path or "None"
def usb_list():

    # CLI call
    user = subprocess.getstatusoutput(f'whoami')
    mess = "ls /media/" + str(user[1])
    # res_usb = subprocess.getstatusoutput(f'lsusb')
    res_usb = subprocess.getstatusoutput(mess)

    # Find USB Drives (Not STM Board)
    for i in res_usb:
        if i != 0:
            if "NOD" not in i:
                print(i)
                return "/media" + str(user[1]) + "/" + i

    print("usb lists")
    return "None"





