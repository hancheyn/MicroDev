import unittest
import time
import os
# import Controller as controller
import Model as model


def pause():
    input("Press the <ENTER> key to continue...")


def Reset_Pins():
    model.bigfoot.set_mux_add(0, 0, 0)
    model.bigfoot.adc_enable(0)
    model.bigfoot.dac_enable(0)
    model.bigfoot.adc_load(0)

   
# ###### Test # 1 | Output Test    ################# #
def Output_Test1(pin, enable, address, instruction):
    # Configure Bigfoot without load to adc
    model.bigfoot.high_current(0)
    model.bigfoot.low_current(0)
    model.bigfoot.adc_load(0)
    model.bigfoot.adc_enable(1)
    # State (on,off) | Enable # | Address #
    model.bigfoot.set_mux_add(1, enable, address)

    # .encode([test], [pin], [instruction])
    s = model.crc_encode(0x01, pin, instruction)
    ser = model.open_serial()
    time.sleep(2)

    model.subject_write(str_write=s, ser=ser)
    test_bytes = model.subject_read(ser_=ser)
    model.close_serial(ser)
    output = model.crc_decode(test_bytes, 2)

    # Read Bigfoot ADC
    time.sleep(0.02)
    if model.crc_decode(test_bytes, 0) == 0:
        adc = -1
    else:
        adc = model.bigfoot.rpi_i2c_adc()

# ###### Test # 2 | Output w/ Load ################# #
def OutputLoad_Test2(pin, enable, address, instruction):
    # Configure Bigfoot with load
    model.bigfoot.high_current(0)
    model.bigfoot.low_current(0)
    model.bigfoot.adc_enable(1)
    model.bigfoot.adc_load(1)

    # State (on,off) | Enable # | Address #
    model.bigfoot.set_mux_add(1, enable, address)

    # .encode([test], [pin], [instruction])
    s = model.crc_encode(0x02, pin, instruction)
    ser = model.open_serial()
    time.sleep(2)
    model.subject_write(str_write=s, ser=ser)
    test_bytes = model.subject_read(ser_=ser)
    model.close_serial(ser)
    output = model.crc_decode(test_bytes, 2)

    # Read Bigfoot ADC
    time.sleep(0.02)
    if model.crc_decode(test_bytes, 0) == 0:
        adc = -1
    else:
        adc = model.bigfoot.rpi_i2c_adc()


# ###### Test # 3 | Pull-Up Input  ################# #
def PullUp_Test3(pin, enable, address, instruction):
    # Configure Bigfoot w/
    model.bigfoot.high_current(0)
    model.bigfoot.low_current(0)
    model.bigfoot.adc_enable(1)
    model.bigfoot.adc_load(1)
    model.bigfoot.set_mux_add(1, enable, address)

    # .encode([test], [pin], [instruction])
    s = model.crc_encode(0x03, pin, instruction)
    ser = model.open_serial()
    time.sleep(2)
    model.subject_write(str_write=s, ser=ser)
    test_bytes = model.subject_read(ser_=ser)
    model.close_serial(ser)
    output = model.crc_decode(test_bytes, 2)
    print(output)


# ###### Test # 4 | Pull-Down Input ################# #
def PullDown_Test4(pin, enable, address, instruction):
    # Configure Bigfoot w/
    model.bigfoot.adc_enable(1)
    model.bigfoot.adc_load(0)
    model.bigfoot.dac_enable(1)
    model.bigfoot.set_mux_add(1, enable, address)

    # FIX: Configure DAC
    model.bigfoot.dac_enable(1)
    model.bigfoot.rpi_i2c_dac(instruction)

    # .encode([test], [pin], [instruction])
    s = model.crc_encode(0x04, pin, instruction)
    ser = model.open_serial()
    model.subject_write(str_write=s, ser=ser)
    test_bytes = model.subject_read(ser_=ser)
    model.close_serial(ser)
    output = model.crc_decode(test_bytes, 2)
    print(output)


# ###### Test # 5 & 6  | DAC Output ################# #
def DAC_Test(pin, enable, address, instruction, test):
    model.bigfoot.set_mux_add(0, 0, 0)
    model.bigfoot.adc_enable(0)
    model.bigfoot.dac_enable(1)
    model.bigfoot.adc_load(0)
    
    # Set DAC to first configuration instruction
    # .encode([test], [pin], [instruction])
    s = model.crc_encode(test, pin, instruction)
    ser = model.open_serial()
    time.sleep(2)
    model.subject_write(str_write=s, ser=ser)
    test_bytes = model.subject_read(ser_=ser)
    model.close_serial(ser)
    output = model.crc_decode(test_bytes, 3)

    print("ADC val: " + str(output))
    model.bigfoot.set_mux_add(1, enable, address)

    # Configure Bigfoot to high logic
    model.bigfoot.rpi_i2c_dac(instruction)


# ###### Test # 7  | Set Power Mode ################# #
def PowerMode_Test7(pin, instruction):
    # Configure Bigfoot
    model.bigfoot.dac_enable(0)
    model.bigfoot.high_current(0)
    model.bigfoot.low_current(1)
    # Always On

    # Communication to Subject Serial
    # .encode([test], [pin], [instruction])
    s = model.crc_encode(0x07, pin, instruction)
    ser = model.open_serial()
    model.subject_write(str_write=s, ser=ser)
    # test_bytes = subject_read(ser_=ser)
    model.close_serial(ser)

    # Read Bigfoot Low Current Sensor
    # TIME DELAY
    time.sleep(0.02)
    current = model.bigfoot.rpi_i2c_ina219(1)
    print(current)


# ###### Test # 8  | Wake up    ################# #
def WakeUp_Test8(enable, address, instruction):
    # Configure Bigfoot
    # Set Wakeup pin
    model.bigfoot.set_mux_add(1, enable, address)
    model.bigfoot.dac_enable(1)
    model.bigfoot.high_current(0)
    model.bigfoot.low_current(1)

    # Configure Bigfoot to high logic
    model.bigfoot.rpi_i2c_dac(instruction)

    # Red Bigfoot Low Current Sensor
    time.sleep(0.1)
    current = model.bigfoot.rpi_i2c_ina219(1)
    print(current)


# ##############################################################
# ##################### Hardware Tests #########################

# ###### Validation Test 2.05.1      ################# #
def Validation_2051():

    l = input("Press the <y> to begin Test 2.05.1")
    Reset_Pins()
    model.bigfoot.low_current(0)
    model.bigfoot.adc_enable(1)
    while l == "y":
        adc = model.bigfoot.rpi_i2c_adc()
        print(adc)
        l = input("Press the <y> to begin Test 2.05.1")
    input("Press the <ENTER> to Exit")
    Reset_Pins()


# ###### Validation Test 2.06.1      ################# #
def Validation_2061():

    l = input("Press the <y> to begin Test 2.06.1")
    Reset_Pins()
    model.bigfoot.dac_enable(0)
    model.bigfoot.high_current(0)
    model.bigfoot.low_current(0)
    while l == "y":
        current = model.bigfoot.rpi_i2c_ina219(0)
        l = input("Press the <y> to begin Test 2.06.1")
    input("Press the <ENTER> to Exit")
    Reset_Pins()


# ###### Validation Test 2.06.2      ################# #
def Validation_2062():

    l = input("Press the <y> to begin Test 2.06.2")
    Reset_Pins()
    model.bigfoot.dac_enable(0)
    model.bigfoot.high_current(0)
    model.bigfoot.low_current(1)
    while l == "y":
        current = model.bigfoot.rpi_i2c_ina219(1)
        l = input("Press the <y> to begin Test 2.06.2")
    input("Press the <ENTER> to Exit")
    Reset_Pins()


# ##############################################################
# ################## Integration Tests #########################
# ###### Validation Test 3.02.1    Pull-Up  ################# #
def Validation_3021(pin, e, a):
    input("Press the <ENTER> to begin Test 3.04.1")
    Output_Test1(pin, e, a, 0x0A)
    input("Press the <ENTER> to Exit")
    Reset_Pins()

# ###### Validation Test 3.03.1    Pull-Up  ################# #
def Validation_3031(pin, e, a):
    input("Press the <ENTER> to begin Test 3.04.1")
    OutputLoad_Test2(pin, e, a, 0x0A)
    input("Press the <ENTER> to Exit")
    Reset_Pins()

# ###### Validation Test 3.04.1    Pull-Up  ################# #
def Validation_3041(pin, e, a):
    input("Press the <ENTER> to begin Test 3.04.1")
    PullUp_Test3(pin, e, a, 0x00)
    input("Press the <ENTER> to Exit")
    Reset_Pins()


# ###### Validation Test 3.05.1    Pull-Down ################# #
def Validation_3051(pin, e, a):
    input("Press the <ENTER> to begin Test 3.05.1")
    PullDown_Test4(pin, e, a, 0)
    input("Press the <ENTER> to Exit")
    Reset_Pins()


# ###### Validation Test 3.06.1  Input Logic  ################# #
def Validation_3061_3V3_Logic(pin, e, a):
    input("Press the <ENTER> to begin Test 3.06.1")
    DAC_Test(pin, e, a, 0x00, 0x05)
    pause()
    DAC_Test(pin, e, a, 0x01, 0x05)
    pause()
    DAC_Test(pin, e, a, 0x02, 0x05)
    pause()
    DAC_Test(pin, e, a, 0x08, 0x05)
    pause()
    DAC_Test(pin, e, a, 0x09, 0x05)
    pause()
    DAC_Test(pin, e, a, 0x0A, 0x05)
    input("Press the <ENTER> to Exit")
    Reset_Pins()


# ###### Validation Test 3.07.1 for 5V Logic ################# #
def Validation_3071_5V_Logic(pin, e, a):
    input("Press the <ENTER> to begin Test 3.07.1")
    DAC_Test(pin, e, a, 0x0F, 0x06)
    pause()
    DAC_Test(pin, e, a, 0x0A, 0x06)
    pause()
    DAC_Test(pin, e, a, 0x05, 0x06)
    pause()
    DAC_Test(pin, e, a, 0x00, 0x06)
    input("Press the <ENTER> to Exit")
    Reset_Pins()


# ###### Validation Test 3.07.1 for 3.3 Logic ################# #
def Validation_3071_3V3_Logic(pin, e, a):
    input("Press the <ENTER> to begin Test 3.07.1")
    DAC_Test(pin, e, a, 0x0A, 0x06)
    pause()
    DAC_Test(pin, e, a, 0x08, 0x06)
    pause()
    DAC_Test(pin, e, a, 0x05, 0x06)
    pause()
    DAC_Test(pin, e, a, 0x00, 0x06)
    input("Press the <ENTER> to Exit")
    Reset_Pins()


# ###### Validation Test 3.08.1              ################# #
def Validation_3081(pin, instruction):
    input("Press the <ENTER> to begin Test 3.08.1")
    PowerMode_Test7(pin, instruction)
    input("Press the <ENTER> to Exit")
    Reset_Pins()


# ###### Validation Test 3.09.1              ################# #
def Validation_3091_3V3_Logic(pin, e, a):
    input("Press the <ENTER> to begin Test 3.09.1")
    WakeUp_Test8(e, a, 0x0A)
    input("Press the <ENTER> to Exit")
    Reset_Pins()


if __name__ == '__main__':
    # PullUp_Test3(23,6,3,0)
    # DAC_Test(34, 5, 1, 0x08, 0x06)
    Validation_2051()


