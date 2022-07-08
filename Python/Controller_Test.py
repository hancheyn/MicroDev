import unittest
import time
import os
# import Controller as controller
import Model as model


# ###### Debugging Test Example ################# #
class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


def pause():
    programPause = input("Press the <ENTER> key to continue...")

def Reset_Pins():
    model.bigfoot.set_mux_add(0, 0, 0)
    model.bigfoot.adc_enable(0)
    model.bigfoot.dac_enable(0)
    model.bigfoot.adc_load(0)

   
# ###### Test # 1 | Output Test    ################# #
def Output_Test1(pin, enable, address, instruction):
    # Configure Bigfoot without load to adc
    bigfoot.high_current(0)
    bigfoot.low_current(0)
    bigfoot.adc_load(0)
    bigfoot.adc_enable(1)
    # State (on,off) | Enable # | Address #
    bigfoot.set_mux_add(1, enable, address)

    # Communication to Subject Serial
    # Configures output low on subject board
    # .encode([test], [pin], [instruction])
    s = crc_encode(0x01, pin, instruction)
    ser = open_serial()
    time.sleep(2)

    subject_write(str_write=s, ser=ser)
    test_bytes = subject_read(ser_=ser)
    close_serial(ser)
    output = crc_decode(test_bytes, 2)
    # print(output)

    # Read Bigfoot ADC
    # adc = bigfoot.rpi_i2c_adc()
    time.sleep(0.02)
    if crc_decode(test_bytes, 0) == 0:
        adc = -1
    else:
        adc = bigfoot.rpi_i2c_adc()

# ###### Test # 2 | Output w/ Load ################# #
def OutputLoad_Test2(pin, enable, address, instruction):
    # Configure Bigfoot with load
    bigfoot.high_current(0)
    bigfoot.low_current(0)
    bigfoot.adc_enable(1)
    bigfoot.adc_load(1)

    # State (on,off) | Enable # | Address #
    bigfoot.set_mux_add(1, enable, address)

    # Communication to Subject Serial
    # Configures output low on subject board
    # .encode([test], [pin], [instruction])
    s = crc_encode(0x02, pin, instruction)
    ser = open_serial()
    time.sleep(2)
    subject_write(str_write=s, ser=ser)
    test_bytes = subject_read(ser_=ser)
    close_serial(ser)
    output = crc_decode(test_bytes, 2)
    # print(output)

    # Read Bigfoot ADC
    # adc = bigfoot.rpi_i2c_adc()
    time.sleep(0.02)
    if crc_decode(test_bytes, 0) == 0:
        adc = -1
    else:
        adc = bigfoot.rpi_i2c_adc()


# ###### Test # 3 | Pull-Up Input  ################# #
def PullUp_Test3(pin, enable, address, instruction):
    # Configure Bigfoot w/
    model.bigfoot.high_current(0)
    model.bigfoot.low_current(0)
    model.bigfoot.adc_enable(1)
    model.bigfoot.adc_load(1)
    model.bigfoot.set_mux_add(1, enable, address)

    # Communication to Subject Serial
    # Configure input pull-ups
    # Returns Subject Input Read
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


# ###### Test # 5 & 6  | DAC Output ################# #
def DAC_Test6(pin, enable, address, instruction):
    model.bigfoot.set_mux_add(0, 0, 0)
    model.bigfoot.adc_enable(0)
    model.bigfoot.dac_enable(1)
    model.bigfoot.adc_load(0)
    
    # Set DAC to first configuration instruction
    # .encode([test], [pin], [instruction])
    s = model.crc_encode(0x06, pin, instruction)
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


# ###### Validation Test 3.07.1 for 5V Logic ################# #
def Validation_3071_5V_Logic(pin, e, a):
    input("Press the <ENTER> to begin Test 3.07.1")
    DAC_Test6(pin, e, a, 0x0F)
    pause()
    DAC_Test6(pin, e, a, 0x0A)
    pause()
    DAC_Test6(pin, e, a, 0x04)
    pause()
    DAC_Test6(pin, e, a, 0x00)
    input("Press the <ENTER> to Exit")

# ###### Validation Test 3.07.1 for 3.3 Logic ################# #
def Validation_3071_3V3_Logic(pin, e, a):
    input("Press the <ENTER> to begin Test 3.07.1")
    DAC_Test6(pin, e, a, 0x0A)
    pause()
    DAC_Test6(pin, e, a, 0x08)
    pause()
    DAC_Test6(pin, e, a, 0x03)
    pause()
    DAC_Test6(pin, e, a, 0x00)
    input("Press the <ENTER> to Exit")



if __name__ == '__main__':
    # PullUp_Test3(23,6,3,0)
    DAC_Test6(34, 5, 1, 0x08)
  
    # unittest.main()

