# MicroDev Project: Controller
#
#

# Adjusting Globals:
# https://www.geeksforgeeks.org/python-globals-function/#:~:text=Syntax%3A%20globals%20%28%29%20Parameters%3A%20No%20parameters%20required.%20Code,%3D%20c%20%2B%20a%20globals%28%29%20%5B%27a%27%5D%20%3D%20d
ADC_PINS = 0
GPIO_PINS = 0
SLEEP_MODES = 0


#
def controller_init(string):
    print(string)
    # Grab Data from Pin Config File
    f = open("subject.config", "r")
    lines = f.readlines()
    globals()['GPIO_PINS'] = lines[1]
    print(GPIO_PINS)
    globals()['ADC_PINS'] = lines[3]
    print(ADC_PINS)
    globals()['SLEEP_MODES'] = lines[4]
    print(SLEEP_MODES)

    # Update global variables with this data
    # GPIO Pin Amount
    # Analog Pin Amount
    # Sleep Modes Amount
    return "Something"

# ******************************** Subject Tests ************************************


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
    print("read")


#
def subject_write():
    print("read")


#
def subject_flash():
    print("flash")


#
def subject_init(string):
    print(string)
    return "Something"


controller_init("Hello")
