import unittest
import time
import Controller


# ###### Debugging Test Example ################# #
class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


# ###### Debugging Test Code for Serial ######### #
class SerialTests(unittest.TestCase):
    # Tests that serial communication is established and subject board can reply
    def test_basic(self):
        controller = Controller
        s = bytearray(3)
        s[0] = 0x01
        s[1] = 0x10
        s[2] = 0x03

        # s[3] = 0x0a
        # s[4] = 0x0D
        ser = controller.open_serial()
        time.sleep(2)
        controller.subject_write(str_write=s, ser=ser)
        #time.sleep(2)
        test_bytes = controller.subject_read(ser_=ser)
        controller.close_serial(ser)

        print(test_bytes)
        int_val = int.from_bytes(test_bytes, "big")
        print(int_val)
        #time.sleep(2)
        # Pin ID Echos Back
        self.assertEqual(test_bytes[0], s[0], "Basic Communication to Subject Board Failed.")

    # Tests Encoding CRC for data packet
    def test_crc_encode(self):
        controller = Controller
        s = bytearray(3)
        # .encode([test], [pin], [instruction])
        s = controller.crc_encode(0x00, 0x01, 0x10)

        self.assertEqual(s[0], 0x01, "Failed to Encode CRC")
        self.assertEqual(s[1], 0x10, "Failed to Encode CRC")
        self.assertEqual(s[2], 0x03, "Failed to Encode CRC")

    # Tests decoding CRC data packet to pin, result, and test id
    # E.G. 1 = pin, 2 = test, 3 = results
    def test_crc_decode(self):
        controller = Controller
        s = bytearray(3)
        s[0] = 0x01
        s[1] = 0x10
        s[2] = 0x03

        # controller.crc_decode([byte array], [value to return])
        # Returns pin value [Byte s[0]]
        output = controller.crc_decode(s, 1)
        self.assertEqual(output, 0x01, "Failed to Decode CRC")

        # Returns result value [Byte s[1]]
        output = controller.crc_decode(s, 3)
        self.assertEqual(output, 0x10, "Failed to Decode CRC")

        # Returns test value [Byte s[2]]
        output = controller.crc_decode(s, 2)
        self.assertEqual(output, 0x00, "Failed to Decode CRC")


# ###### Debugging Test Code for CLI ########## #
# CLI Functionality Tests
class CLITests(unittest.TestCase):

    # Test that No Board Info is Obtained
    def test_board_list_None(self):
        controller = Controller
        board_out = controller.board_list()
        print(board_out)
        # Test of Output (? Output "No Boards Detected" for no useful board)
        self.assertEqual(board_out, "No Boards Detected", "No board identification failed.")

    # Test that Uno ID Info is Obtained
    def test_board_list_Uno(self):
        controller = Controller
        board_out = controller.board_list()
        print(board_out)
        # Test of Output (? Output "Arduino Uno Detected" for Arduino Uno)
        self.assertEqual(board_out, "Arduino Uno Detected", "Arduino Uno Failed to be Detected.")

    # Test that STM ID Info is Obtained
    def test_board_list_STM32F411(self):
        controller = Controller
        board_out = controller.board_list()
        print(board_out)
        # Test of Output (? Output "STM32F411 Detected" for STM32F411)
        self.assertEqual(board_out, "STM32F411 Detected", "STM32F411 Failed to be Detected.")

    # ###################################################################
    # Additional Board Models can be added like below (?? Procedure in Document)
    # 1) Add Board List ID Process
    # 2) Add Flash .bin file of board to subject_flash process
    # ###################################################################

    # STM Board Addition Example
    def test_board_list_STM32F401(self):
        controller = Controller
        board_out = controller.board_list()
        print(board_out)
        # Test of Output (? Output "STM32F401 Detected" for STM32F401)
        self.assertEqual(board_out, "STM32F401 Detected", "STM32F401 Failed to be Detected.")

    # Test that Two or More boards Info is Obtained
    def test_board_list_Overflow(self):
        controller = Controller
        board_out = controller.board_list()
        print(board_out)
        # Test of Output (? Output "Overflow" for two+ board)
        self.assertEqual(board_out, "Overflow", "Two+ Boards Detected")

    # Flash Subject Board Test
    def test_board_flash(self):
        controller = Controller
        board_out = controller.board_list()
        controller.subject_flash(board_out)


if __name__ == '__main__':
    unittest.main()
